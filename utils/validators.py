"""
Utility validators
"""
import re
from typing import Tuple

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Validate password (min 8 characters)"""
    return len(password) >= 8

def validate_vehicle(data: dict) -> Tuple[bool, str]:
    """Validate vehicle data"""
    required_fields = ['vehicle_id', 'make', 'model', 'year', 'engine_type', 
                      'transmission_type', 'vin', 'license_plate']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate VIN (17 characters)
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', data.get('vin', '')):
        return False, "Invalid VIN format (must be 17 alphanumeric characters)"
    
    # Validate year
    year = data.get('year')
    if not isinstance(year, int) or year < 1900 or year > 2100:
        return False, "Invalid year"
    
    # Validate engine type
    valid_engines = ['petrol', 'diesel', 'hybrid', 'electric']
    if data.get('engine_type') not in valid_engines:
        return False, f"Invalid engine type. Must be one of: {', '.join(valid_engines)}"
    
    # Validate transmission type
    valid_transmissions = ['manual', 'automatic', 'cvt', 'dct']
    if data.get('transmission_type') not in valid_transmissions:
        return False, f"Invalid transmission type. Must be one of: {', '.join(valid_transmissions)}"
    
    return True, "Vehicle data is valid"

def validate_ecu_parameter(param_name: str, value: float, min_val: float, max_val: float) -> Tuple[bool, str]:
    """Validate ECU parameter"""
    try:
        value = float(value)
        if value < min_val or value > max_val:
            return False, f"Parameter '{param_name}' out of range [{min_val}, {max_val}]. Got: {value}"
        return True, "Parameter value is valid"
    except ValueError:
        return False, f"Parameter '{param_name}' must be numeric"
