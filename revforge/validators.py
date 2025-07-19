import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.html import strip_tags


def validate_safe_text(value, field_name="Text"):
    """Generic safe text validation"""
    if not value:
        return value
    
    value = str(value).strip()
    
    # Check for minimum length
    if len(value) < 2:
        raise ValidationError(f'{field_name} must be at least 2 characters long.')
    
    # Check for maximum length (default 255)
    if len(value) > 255:
        raise ValidationError(f'{field_name} cannot exceed 255 characters.')
    
    # Check for potentially harmful characters
    harmful_pattern = r'[<>"\']'
    if re.search(harmful_pattern, value):
        raise ValidationError(f'{field_name} cannot contain <, >, ", or \' characters.')
    
    # Check for excessive spaces
    if '  ' in value:
        raise ValidationError(f'{field_name} cannot contain multiple consecutive spaces.')
    
    # Check for common spam patterns - more specific to avoid false positives
    spam_patterns = [
        r'\b(click here|buy now|free|discount|sale|offer|limited time)\b',
        r'\b(www\.|http://|https://)\b',
        # Only flag if entire field is all caps (not just individual words)
        r'^[A-Z\s]{10,}$',  # Entire field in caps with 10+ chars
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(f'{field_name} contains invalid content.')
    
    return value


def validate_product_name(value):
    """Validate product name specifically"""
    if not value:
        return value
    
    value = str(value).strip()
    
    # Check for minimum length
    if len(value) < 3:
        raise ValidationError('Product name must be at least 3 characters long.')
    
    # Check for maximum length (40 characters as requested)
    if len(value) > 40:
        raise ValidationError('Product name cannot exceed 40 characters.')
    
    # Check for potentially harmful characters
    harmful_pattern = r'[<>"\']'
    if re.search(harmful_pattern, value):
        raise ValidationError('Product name cannot contain <, >, ", or \' characters.')
    
    # Check for excessive spaces
    if '  ' in value:
        raise ValidationError('Product name cannot contain multiple consecutive spaces.')
    
    # Check for common spam patterns - more specific
    spam_patterns = [
        r'\b(click here|buy now|free|discount|sale|offer|limited time)\b',
        r'\b(www\.|http://|https://)\b',
        # Only flag if entire field is all caps (not just individual words)
        r'^[A-Z\s]{10,}$',  # Entire field in caps with 10+ chars
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Product name contains invalid content.')
    
    return value


def validate_product_description(value):
    """Validate product description specifically"""
    if not value:
        return value
    
    value = str(value).strip()
    
    # Check for minimum length
    if len(value) < 10:
        raise ValidationError('Product description must be at least 10 characters long.')
    
    # Check for maximum length
    if len(value) > 1200:
        raise ValidationError('Product description cannot exceed 1200 characters.')
    
    # Check for potentially harmful content - more specific
    harmful_patterns = [
        r'<script|javascript:|vbscript:|onload=|onerror=',
        # Only flag obvious spam, not legitimate product descriptions
        r'\b(click here to buy|buy now|free shipping|limited time offer)\b',
        r'\b(www\.|http://|https://)\b',
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Product description contains invalid content.')
    
    return value


def validate_username(value):
    """Validate username specifically"""
    if not value:
        return value
    
    value = str(value).strip()
    
    if len(value) < 3:
        raise ValidationError('Username must be at least 3 characters long.')
    
    if len(value) > 20:
        raise ValidationError('Username cannot exceed 20 characters.')
    
    # Allow only letters, numbers, and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError('Username can only contain letters, numbers, and underscores.')
    
    # Check for common spam patterns - more specific
    spam_patterns = [
        r'\b(admin|root|test|guest|user|demo)\b',
        r'\b(www\.|http://|https://)\b',
        # Only flag if entire username is all caps
        r'^[A-Z]{5,}$',  # Entire username in caps with 5+ chars
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Username contains invalid content.')
    
    return value


def validate_password(value):
    """Validate password strength"""
    if not value:
        return value
    
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    
    if len(value) > 128:
        raise ValidationError('Password cannot exceed 128 characters.')
    
    # Check for common weak passwords
    weak_patterns = [
        r'^123456',
        r'^password',
        r'^qwerty',
        r'^abc123',
        r'^admin',
        r'^test',
    ]
    
    for pattern in weak_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Password is too common. Please choose a stronger password.')
    
    return value


def validate_phone_number(value):
    """Validate phone number format"""
    if not value:
        return value
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', str(value))
    
    if len(digits_only) < 10:
        raise ValidationError('Phone number must have at least 10 digits.')
    
    if len(digits_only) > 15:
        raise ValidationError('Phone number cannot exceed 15 digits.')
    
    return value


def validate_postal_code(value):
    """Validate postal code format"""
    if not value:
        return value
    
    value = str(value).strip()
    
    # Allow alphanumeric characters, spaces, and hyphens
    if not re.match(r'^[A-Za-z0-9\s\-]+$', value):
        raise ValidationError('Postal code can only contain letters, numbers, spaces, and hyphens.')
    
    if len(value) < 3:
        raise ValidationError('Postal code must be at least 3 characters long.')
    
    if len(value) > 10:
        raise ValidationError('Postal code cannot exceed 10 characters.')
    
    return value


def validate_address(value):
    """Validate address fields"""
    if not value:
        return value
    
    value = str(value).strip()
    
    if len(value) < 5:
        raise ValidationError('Address must be at least 5 characters long.')
    
    if len(value) > 255:
        raise ValidationError('Address cannot exceed 255 characters.')
    
    # Check for potentially harmful content
    harmful_patterns = [
        r'<script|javascript:|vbscript:|onload=|onerror=',
        r'\b(www\.|http://|https://)\b',
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Address contains invalid content.')
    
    return value


def validate_sku(value):
    """Validate SKU format"""
    if not value:
        return value
    
    value = str(value).strip()
    
    if len(value) < 3:
        raise ValidationError('SKU must be at least 3 characters long.')
    
    if len(value) > 50:
        raise ValidationError('SKU cannot exceed 50 characters.')
    
    # Allow alphanumeric characters, hyphens, and underscores only
    if not re.match(r'^[A-Za-z0-9_-]+$', value):
        raise ValidationError('SKU can only contain letters, numbers, hyphens, and underscores.')
    
    return value.upper()


def validate_price(value):
    """Validate price - must be positive and reasonable"""
    if value is None:
        raise ValidationError('Price is required.')
    
    if value <= 0:
        raise ValidationError('Price must be greater than 0.')
    
    if value > 999999.99:
        raise ValidationError('Price cannot exceed $999,999.99.')
    
    return value


def validate_stock_quantity(value):
    """Validate stock quantity"""
    if value is None:
        raise ValidationError('Stock quantity is required.')
    
    if value < 0:
        raise ValidationError('Stock quantity cannot be negative.')
    
    if value > 999999:
        raise ValidationError('Stock quantity cannot exceed 999,999.')
    
    return value


def validate_file_name(value):
    """Validate file name for security"""
    if not value:
        return value
    
    filename = str(value.name)
    
    # Check for potentially harmful file names
    harmful_patterns = [
        r'\.\./',  # Directory traversal
        r'<script',  # Script tags
        r'javascript:',  # JavaScript protocol
        r'vbscript:',  # VBScript protocol
        r'data:',  # Data URI
        r'file:',  # File protocol
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            raise ValidationError('Invalid file name detected.')
    
    return value


def sanitize_html(value):
    """Sanitize HTML content"""
    if not value:
        return value
    
    # Remove HTML tags
    clean_value = strip_tags(str(value))
    
    # Remove any remaining script-like content
    script_patterns = [
        r'javascript:',
        r'vbscript:',
        r'onload=',
        r'onerror=',
        r'onclick=',
    ]
    
    for pattern in script_patterns:
        clean_value = re.sub(pattern, '', clean_value, flags=re.IGNORECASE)
    
    return clean_value


def validate_email_safe(value):
    """Validate email for safe content"""
    if not value:
        return value
    
    value = str(value).strip().lower()
    
    # Basic email format check
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        raise ValidationError('Please enter a valid email address.')
    
    # Check for potentially harmful content
    harmful_patterns = [
        r'<script',
        r'javascript:',
        r'vbscript:',
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Email contains invalid content.')
    
    return value


# Common validators for forms
SAFE_TEXT_VALIDATOR = RegexValidator(
    regex=r'^[^<>"\']+$',
    message='Text cannot contain <, >, ", or \' characters.'
)

USERNAME_VALIDATOR = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message='Username can only contain letters, numbers, and underscores.'
)

PHONE_VALIDATOR = RegexValidator(
    regex=r'^[\d\s\-\(\)\+]+$',
    message='Phone number can only contain digits, spaces, hyphens, parentheses, and plus signs.'
)

POSTAL_CODE_VALIDATOR = RegexValidator(
    regex=r'^[A-Za-z0-9\s\-]+$',
    message='Postal code can only contain letters, numbers, spaces, and hyphens.'
)

SKU_VALIDATOR = RegexValidator(
    regex=r'^[A-Za-z0-9_-]+$',
    message='SKU can only contain letters, numbers, hyphens, and underscores.'
) 