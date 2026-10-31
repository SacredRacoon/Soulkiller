from typing import Union

def format_hormone_level(level: float) -> str:
    if level >= 80:
        return "very high"
    elif level >= 60:
        return "high"
    elif level >= 40:
        return "normal"
    elif level >= 20:
        return "low"
    else:
        return "very low"

def get_hormone_state(level: float) -> dict:
    if level >= 80:
        return {
            "state": "critical_high",
            "description": "critical high",
            "effects": ["euphoria", "hyperactivity","risk"]
        }
    elif level >= 60:
        return {
            "state": "high",
            "description": "high",
            "effects": ["activity", "motivation"]
        }
    elif level >= 40:
        return {
            "state": "normal",
            "description": "normal",
            "effects": ["stability", "balance"]
        }
    elif level >= 20:
        return {
            "state": "low",
            "description": "low",
            "effects": ["apathy", "fatigue"]
        }
    else:
        return {
            "state": "very low",
            "description": "very low",
            "effects": ["depression", "exhaustion"]
        }

def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(value, max_val))

def calculate_change(current: float, target: float, rate: float, time_delta: float) -> float:
    change = (target - current) * rate * time_delta
    return current + change