from dataclasses import dataclass
from typing import List, Optional, Callable
from utils.helpers import clamp, calculate_change
from utils.logger import PersonaLogger
    
@dataclass
class HormoneTrigger:
    name: str
    intensity: float
    duration_minutes: float = 1.0
    decay_rate: float = 0.1

class Hormone:
    def __init__(self, name: str, baseline: float, recovery_rate: float, 
                 sensitivity: float, logger: Optional[PersonaLogger] = None,
                 min_value: float = 0.0, max_value: float = 100.0):
        self.name = name
        self.baseline = baseline
        self.min_value = min_value
        self.max_value = max_value
        self.sensitivity = sensitivity
        self.recovery_rate = recovery_rate

        self.current_value = baseline
        self.active_triggers: List[HormoneTrigger] =[]
        self.logger = logger
        if self.logger:
            self.logger.debug(
                f"Гормон[{self.name}] инициализирован",
                baseline=baseline,
                recovery_rate=recovery_rate,
                sensitivity=sensitivity
            )
    def get_value(self) -> float:
        return self.current_value

    def set_value(self, new_value: float, reason: str = "прямая установка"):
        old_value = self.current_value
        self.current_value = clamp(new_value, self.min_value, self.max_value)

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.hormone_change(
                self.name, old_value, self.current_value, reason
            )

    def apply_trigger(self, trigger: HormoneTrigger):
        self.active_triggers.append(trigger)
        if self.logger:
            self.logger.debug(
                f"Гормон [{self.name}] применен триггер",
                trigger_name = trigger.name,
                intensity = trigger.intensity,
                duration = trigger.duration_minutes
            )

    def update(self, time_delta_minutes: float):
        old_value = self.current_value
        trigger_effect = 0.0
        expired_triggers = []

        for trigger in self.active_triggers:
            effect = trigger.intensity * self.sensitivity
            trigger_effect += effect
            trigger.intensity *= (1 - trigger.decay_rate * time_delta_minutes)
            trigger.duration_minutes -= time_delta_minutes
            if trigger.duration_minutes <= 0 or abs(trigger.intensity) < 0.01:
                expired_triggers.append(trigger)

        for trigger in expired_triggers:
            self.active_triggers.remove(trigger)
            if self.logger:
                self.logger.debug(
                    f"Гормон [{self.name}] триггер истек",
                    trigger_name=trigger.name
                )

        if trigger_effect != 0:
            self.current_value += trigger_effect * time_delta_minutes

        self.current_value = calculate_change(
            self.current_value, self.baseline,
            self.recovery_rate * 0.01, time_delta_minutes
        )

        self.current_value = clamp(self.current_value, self.min_value, self.max_value)

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.hormone_change(
                self.name, old_value, self.current_value,
                f"обновление за {time_delta_minutes} мин"
            )

    def apply_fluctuation(self, change: float):
        old_value = self.current_value
        self.current_value = clamp(
            self.current_value + change,
            self.min_value, self.max_value
        )

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.debug(
                f"Гормон [{self.name}] микро флуктуация",
                old_value = old_value,
                new_value = self.current_value,
                change = change
            )

    def get_state_description(self) -> dict:
        from utils.helpers import get_hormone_state
        return get_hormone_state(self.current_value)

    def to_dict(self) -> dict:
        return{
            "name": self.name,
            "current_value": self.current_value,
            "baseline": self.baseline,
            "recovery_rate": self.recovery_rate,
            "sensitivity": self.sensitivity,
            "active_trigger_count": len((self.active_triggers))
        }