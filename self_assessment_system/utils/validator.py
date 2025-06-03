from typing import Any, Dict, List, Optional, Union
import re

class DataValidator:
    def __init__(self):
        self.errors = []

    def validate_string(self, value: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
        if not isinstance(value, str):
            self.errors.append(f"Expected string, got {type(value)}")
            return False
        if len(value) < min_length:
            self.errors.append(f"String length must be at least {min_length}")
            return False
        if max_length and len(value) > max_length:
            self.errors.append(f"String length must not exceed {max_length}")
            return False
        return True

    def validate_number(self, value: Union[int, float], min_val: Optional[float] = None, 
                       max_val: Optional[float] = None) -> bool:
        if not isinstance(value, (int, float)):
            self.errors.append(f"Expected number, got {type(value)}")
            return False
        if min_val is not None and value < min_val:
            self.errors.append(f"Value must be greater than or equal to {min_val}")
            return False
        if max_val is not None and value > max_val:
            self.errors.append(f"Value must be less than or equal to {max_val}")
            return False
        return True

    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            self.errors.append("Invalid email format")
            return False
        return True

    def validate_dict(self, data: Dict, required_fields: List[str]) -> bool:
        if not isinstance(data, dict):
            self.errors.append(f"Expected dictionary, got {type(data)}")
            return False
        for field in required_fields:
            if field not in data:
                self.errors.append(f"Missing required field: {field}")
                return False
        return True

    def get_errors(self) -> List[str]:
        return self.errors

    def clear_errors(self) -> None:
        self.errors = []