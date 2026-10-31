from dataclasses import dataclass
from typing import List, Optional, Callable
from utils.helpers import clamp, calculate_change
from utils.logger import PersonaLogger
from datetime import datetime

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
                f"Hormone [{self.name}] init",
                baseline=baseline,
                recovery_rate=recovery_rate,
                sensitivity=sensitivity
            )
    def get_value(self) -> float:
        return self.current_value

    def set_value(self, new_value: float, reason: str = "direct order"):
        old_value = self.current_value
        self.current_value = clamp(new_value, self.min_value, self.max_value)

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.hormone_change(
                self.name, old_value, self.current_value, reason
            )

    def apply_trigger(self, trigger: HormoneTrigger):
        old_value = self.current_value

        immediate_effect = trigger.intensity * self.sensitivity
        self.current_value = clamp(
            self.current_value + immediate_effect,
            self.min_value,
            self.max_value
        )

        self.active_triggers.append(trigger)
        if self.logger:
            self.logger.debug(
                f"Hormon [{self.name}] applied trigger",
                trigger_name = trigger.name,
                intensity = trigger.intensity,
                duration = trigger.duration_minutes
            )

            if abs(self.current_value - old_value) > 0.01:
                self.logger.hormone_change(
                    self.name, old_value, self.current_value,
                    f"trigger [{trigger.name}]"
                )

    def update(self, time_delta_minutes: float):
        old_value = self.current_value
        expired_triggers = []

        for trigger in self.active_triggers:
            trigger.intensity *= (1 - trigger.decay_rate * time_delta_minutes)
            trigger.duration_minutes -= time_delta_minutes

            if trigger.duration_minutes <= 0 or abs(trigger.intensity) < 0.01:
                expired_triggers.append(trigger)

        for trigger in expired_triggers:
            self.active_triggers.remove(trigger)
            if self.logger:
                self.logger.debug(
                    f"Hormone [{self.name}] trigger expired",
                    trigger_name = trigger.name
                )

        self.current_value = calculate_change(
            self.current_value, self.baseline,
            self.recovery_rate * 0.01, time_delta_minutes
        )

        self.current_value = clamp(self.current_value, self.min_value, self.max_value)

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.hormone_change(
                self.name, old_value, self.current_value,
                f"update for {time_delta_minutes} min"
            )

    def apply_fluctuation(self, change: float):
        old_value = self.current_value
        self.current_value = clamp(
            self.current_value + change,
            self.min_value, self.max_value
        )

        if self.logger and abs(self.current_value - old_value) > 0.01:
            self.logger.debug(
                f"Hormone [{self.name}] micro fluctuation",
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

    def get_full_report(self) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "hormones": {
                name: {
                    "value": hormone.current_value,
                    "baseline": hormone.baseline,
                    "deviation": hormone.current_value - hormone.baseline,
                    "state": hormone.get_state_description(),
                    "active_triggers": len(hormone.active_triggers)
                }
                for name, hormone in self.hormones.items()
            },
            "random_gen_stats": self.random_gen.get_stats()
        }