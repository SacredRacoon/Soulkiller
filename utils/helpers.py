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
            "effects": ["эйфория", "гиперактивность","риск"]
        }
    elif level >= 60:
        return {
            "state": "high",
            "description": "high",
            "effects": ["активность", "мотивцаия"]
        }
    elif level >= 40:
        return {
            "state": "normal",
            "description": "normal",
            "effects": ["стабильность", "баланс"]
        }
    elif level >= 20:
        return {
            "state": "low",
            "description": "low",
            "effects": ["апатия", "усталость"]
        }
    else:
        return {
            "state": "very low",
            "description": "very low",
            "effects": ["депрессия", "истощение"]
        }

def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(max_val), value)

def calculate_change(current: float, target: float, rate: float, time_delta: float) -> float:
    change = (target - current) * rate * time_delta
    return current + change