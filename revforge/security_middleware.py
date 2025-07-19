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
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.malicious_patterns]
    
    def __call__(self, request):
        # Check request parameters for malicious content
        if self._contains_malicious_content(request):
            return HttpResponseForbidden("Request contains potentially malicious content.")
        
        response = self.get_response(request)
        
        # Add security headers
        response = self._add_security_headers(response)
        
        return response
    
    def _contains_malicious_content(self, request):
        """Check if request contains malicious content"""
        
        # Check GET parameters
        for key, value in request.GET.items():
            if self._check_value_for_malicious_content(value):
                return True
        
        # Check POST parameters
        for key, value in request.POST.items():
            if self._check_value_for_malicious_content(value):
                return True
        
        # Check headers (basic check)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if self._check_value_for_malicious_content(user_agent):
            return True
        
        return False
    
    def _check_value_for_malicious_content(self, value):
        """Check if a value contains malicious content"""
        if not value:
            return False
        
        value_str = str(value).lower()
        
        # Check against compiled patterns
        for pattern in self.compiled_patterns:
            if pattern.search(value_str):
                return True
        
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
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Sanitize GET parameters
        request.GET = self._sanitize_querydict(request.GET)
        
        # Sanitize POST parameters
        request.POST = self._sanitize_querydict(request.POST)
        
        response = self.get_response(request)
        return response
    
    def _sanitize_querydict(self, querydict):
        """Sanitize QueryDict values"""
        from django.http import QueryDict
        
        sanitized = QueryDict(mutable=True)
        
        for key, value in querydict.items():
            if isinstance(value, list):
                sanitized.setlist(key, [self._sanitize_value(v) for v in value])
            else:
                sanitized[key] = self._sanitize_value(value)
        
        return sanitized
    
    def _sanitize_value(self, value):
        """Sanitize a single value"""
        if not value:
            return value
        
        value_str = str(value)
        
        # Remove null bytes
        value_str = value_str.replace('\x00', '')
        
        # Remove control characters except newlines and tabs
        value_str = ''.join(char for char in value_str if ord(char) >= 32 or char in '\n\t')
        
        # Limit length
        if len(value_str) > 10000:
            value_str = value_str[:10000]
        
        return value_str


class RateLimitingMiddleware:
    """
    Basic rate limiting middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
    
    def __call__(self, request):
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limit
        if self._is_rate_limited(client_ip):
            return HttpResponseForbidden("Too many requests. Please try again later.")
        
        # Increment request count
        self._increment_request_count(client_ip)
        
        response = self.get_response(request)
        return response
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _is_rate_limited(self, client_ip):
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
    
    def _increment_request_count(self, client_ip):
        """Increment request count for client"""
        import time
        
        current_time = time.time()
        
        if client_ip in self.request_counts:
            self.request_counts[client_ip]['count'] += 1
        else:
            self.request_counts[client_ip] = {
                'count': 1,
                'timestamp': current_time
            } 