import re
from typing import Tuple, Dict, Any
from functools import wraps
from flask import jsonify

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"

def validate_vehicle(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate vehicle data"""
    required_fields = ['vehicle_id', 'make', 'model', 'year', 'engine_type',
                      'transmission_type', 'vin']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate VIN (17 characters, alphanumeric)
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', str(data.get('vin', ''))):
        return False, "Invalid VIN format (must be 17 alphanumeric characters)"
    
    # Validate year
    year = data.get('year')
    if not isinstance(year, int) or year < 1900 or year > 2100:
        return False, "Invalid year (must be between 1900 and 2100)"
    
    # Validate engine type
    valid_engines = ['petrol', 'diesel', 'hybrid', 'electric']
    if data.get('engine_type') not in valid_engines:
        return False, f"Invalid engine type. Must be one of: {', '.join(valid_engines)}"
    
    # Validate transmission type
    valid_transmissions = ['manual', 'automatic', 'cvt', 'dct']
    if data.get('transmission_type') not in valid_transmissions:
        return False, f"Invalid transmission type. Must be one of: {', '.join(valid_transmissions)}"
    
    return True, "Vehicle data is valid"

def validate_profile(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate remapping profile data"""
    if not data.get('profile_name'):
        return False, "Profile name is required"
    
    valid_levels = ['stock', 'eco', 'standard', 'sport', 'extreme']
    if data.get('performance_level') not in valid_levels:
        return False, f"Invalid performance level. Must be one of: {', '.join(valid_levels)}"
    
    return True, "Profile data is valid"

def validate_ecu_parameter(param_name: str, value: float, min_val: float, 
                          max_val: float) -> Tuple[bool, str]:
    """Validate ECU parameter value"""
    try:
        value = float(value)
        if value < min_val or value > max_val:
            return False, f"Parameter '{param_name}' out of range [{min_val}, {max_val}]. Got: {value}"
        return True, "Parameter value is valid"
    except (ValueError, TypeError):
        return False, f"Parameter '{param_name}' must be numeric"

def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function
