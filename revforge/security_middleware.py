import re
from django.http import HttpResponseForbidden
from django.conf import settings


class SecurityMiddleware:
    """
    Security middleware to protect against common attack vectors
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Patterns for potentially malicious content
        self.malicious_patterns = [
            # SQL Injection patterns - more specific to avoid false positives
            r'(\b(union\s+select|select\s+.*\s+from|insert\s+into|update\s+.*\s+set|delete\s+from|drop\s+table|create\s+table|alter\s+table)\b)',
            r'(\b(or\s+1\s*=\s*1|and\s+1\s*=\s*1|or\s+\'\'=\'\'|and\s+\'\'=\'\')\b)',
            r'(\b(union\s+select|exec\s+xp_|execute\s+xp_)\b)',
            
            # XSS patterns
            r'<script[^>]*>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
            r'onmouseover\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>',
            
            # Directory traversal
            r'\.\./',
            r'\.\.\\',
            
            # Command injection - more specific
            r'(\b(cmd\s+/c|command\s+/c|exec\s+cmd|system\s+cmd|eval\s*\(|shell_exec)\b)',
            
            # File inclusion - more specific
            r'(\b(include\s*\(|require\s*\(|include_once\s*\(|require_once\s*\()\b)',
            
            # PHP code
            r'<\?php',
            r'<\?=',
            
            # HTML entities for script tags
            r'&lt;script',
            r'&#60;script',
            r'&#x3c;script',
        ]
        
        # Compile patterns for better performance
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.malicious_patterns] #Compiles the patterns for better performance
    
    def __call__(self, request):
        # Check request parameters for malicious content
        if self._contains_malicious_content(request):
            return HttpResponseForbidden("Request contains potentially malicious content.") #Returns a forbidden response if the request contains potentially malicious content
        
        response = self.get_response(request) #Gets the response from the get_response function
        
        # Add security headers
        response = self._add_security_headers(response) #Adds security headers to the response
        
        return response #Returns the response
    
    def _contains_malicious_content(self, request):
        """Check if request contains malicious content"""
        
        # Check GET parameters
        for key, value in request.GET.items():
            if self._check_value_for_malicious_content(value):
                return True #Returns True if the value contains malicious content
        
        # Check POST parameters
        for key, value in request.POST.items():
            if self._check_value_for_malicious_content(value):
                return True #Returns True if the value contains malicious content
        
        # Check headers (basic check)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self._check_value_for_malicious_content(user_agent):
            return True #Returns True if the user agent contains malicious content
        
        return False #Returns False if the request does not contain malicious content
    
    def _check_value_for_malicious_content(self, value):
        """Check if a value contains malicious content"""
        if not value:
            return False
        
        value_str = str(value).lower()
        
        # Check against compiled patterns
        for pattern in self.compiled_patterns:
            if pattern.search(value_str):
                return True #Returns True if the value contains malicious content
        
        # Additional checks for excessive length
        if len(value_str) > 10000:  # 10KB limit
            return True
        
        # Check for excessive repetition (potential DoS)
        if len(value_str) > 100:
            # Check for repeated characters
            for char in value_str:
                if value_str.count(char) > len(value_str) * 0.8:  # 80% repetition
                    return True
        
        return False
    
    def _add_security_headers(self, response):
        """Add security headers to response"""
        
        # Content Security Policy - Allow external CDN resources
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        # X-Frame-Options
        response['X-Frame-Options'] = 'DENY'
        
        # X-Content-Type-Options
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-XSS-Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response


class InputSanitizationMiddleware:
    """
    Middleware to sanitize user input
    """
    
    def __init__(self, get_response): #Initializes the middleware
        self.get_response = get_response #Gets the response from the get_response function
    
    def __call__(self, request): #Calls the middleware
        # Sanitize GET parameters
        request.GET = self._sanitize_querydict(request.GET) #Sanitizes the GET parameters
        
        # Sanitize POST parameters
        request.POST = self._sanitize_querydict(request.POST) #Sanitizes the POST parameters
        
        response = self.get_response(request) #Gets the response from the get_response function
        return response #Returns the response
    
    def _sanitize_querydict(self, querydict): #Sanitizes the QueryDict values
        """Sanitize QueryDict values"""
        from django.http import QueryDict
        
        sanitized = QueryDict(mutable=True) #Creates a mutable QueryDict
        
        for key, value in querydict.items(): #Iterates over the items in the QueryDict
            if isinstance(value, list): #Checks if the value is a list
                sanitized.setlist(key, [self._sanitize_value(v) for v in value]) #Sanitizes the list
            else: #If the value is not a list
                sanitized[key] = self._sanitize_value(value) #Sanitizes the value
        
        return sanitized #Returns the sanitized QueryDict
    
    def _sanitize_value(self, value): #Sanitizes a single value
        """Sanitize a single value"""
        if not value:
            return value
        
        value_str = str(value) #Converts the value to a string
        
        # Remove null bytes
        value_str = value_str.replace('\x00', '') #Removes null bytes
        
        # Remove control characters except newlines and tabs
        value_str = ''.join(char for char in value_str if ord(char) >= 32 or char in '\n\t') #Removes control characters except newlines and tabs
        
        # Limit length
        if len(value_str) > 10000: #Checks if the value is greater than 10000
            value_str = value_str[:10000] #Limits the value to 10000 characters
        
        return value_str #Returns the sanitized value


class RateLimitingMiddleware:
    """
    Basic rate limiting middleware
    """
    
    def __init__(self, get_response): #Initializes the middleware
        self.get_response = get_response #Gets the response from the get_response function
        self.request_counts = {} #Initializes the request counts
    
    def __call__(self, request): #Calls the middleware
        # Get client IP
        client_ip = self._get_client_ip(request) #Gets the client IP address from the request
        
        # Check rate limit
        if self._is_rate_limited(client_ip): #Checks if the client is rate limited
            return HttpResponseForbidden("Too many requests. Please try again later.") #Returns a forbidden response if the client is rate limited
        
        # Increment request count
        self._increment_request_count(client_ip) #Increments the request count for the client
        
        response = self.get_response(request) #Gets the response from the get_response function
        return response #Returns the response
    
    def _get_client_ip(self, request): #Gets the client IP address
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') #Gets the client IP address from the request
        if x_forwarded_for: #If the client IP is in the request
            ip = x_forwarded_for.split(',')[0]
        else: #If the client IP is not in the request
            ip = request.META.get('REMOTE_ADDR')
        return ip #Returns the client IP address
    
    def _is_rate_limited(self, client_ip): #Checks if the client is rate limited
        """Check if client is rate limited"""
        import time
        
        current_time = time.time()
        
        # Clean old entries (older than 1 minute)
        self.request_counts = {
            ip: count for ip, count in self.request_counts.items()
            if current_time - count['timestamp'] < 60
        }
        
        # Check current count
        if client_ip in self.request_counts:
            count_info = self.request_counts[client_ip]
            if count_info['count'] > 100:  # 100 requests per minute
                return True
        
        return False
    
    def _increment_request_count(self, client_ip): #Increments the request count for the client
        """Increment request count for client"""
        import time
        
        current_time = time.time() #Gets the current time
        
        if client_ip in self.request_counts: #Checks if the client IP is in the request counts
            self.request_counts[client_ip]['count'] += 1 #Increments the request count for the client
        else: #If the client IP is not in the request counts
            self.request_counts[client_ip] = { #Sets the request counts for the client
                'count': 1, #Sets the request count to 1
                'timestamp': current_time #Sets the timestamp to the current time
            } 