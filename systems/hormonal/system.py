from typing import Dict, Optional
from systems.hormonal.hormone import Hormone, HormoneTrigger
from systems.hormonal.triggers import TriggerManager, TriggerEvent
from utils.random_gen import SeededRandom
from utils.logger import PersonaLogger
from core.config import HormonalSystemConfig

class HormonalSystem:
    def __init__(self, config: HormonalSystemConfig, logger: PersonaLogger, random_gen: SeededRandom):
        self.config = config
        self.logger = logger
        self.random_gen = random_gen
        self.hormones: Dict[str, Hormone] = {}
        for name, hormone_config in config.hormones.items():
            self.hormones[name] = Hormone(
                name=hormone_config.name,
                baseline=hormone_config.baseline,
                recovery_rate=hormone_config.recovery_rate,
                sensitivity=hormone_config.sensitivity,
                min_value=hormone_config.min_value,
                max_value=hormone_config.max_value,
                logger=logger
            )

        self.trigger_manager = TriggerManager()

        if self.logger:
            self.logger.info(
                "Hormonal system init",
                hormones_count = len(self.hormones),
                interaction_strength=config.interaction_strength 
            )

    def update(self,time_delta_minutes:float):
        self.logger.debug(
            "Starting update hormonal system",
            time_delta=time_delta_minutes
        )

        for hormone_name,hormone in self.hormones.items():
            hormone.update(time_delta_minutes)

        if self.config.cross_influence_enabled:
            self._apply_hormone_interactions()

        if self.config.fluctuation_enabled:
            self._apply_random_fluctuations()

        self.logger.debug("Ending update hormonal system")
    def _apply_hormone_interactions(self):
        interactions_applied = []
        
        if (self.hormones["dopamine"].current_value > 70 and 
            self.hormones["adrenaline"].current_value > 70):
            boost = self.config.interaction_strength * 15
            self.hormones["dopamine"].apply_fluctuation(boost)
            self.hormones["adrenaline"].apply_fluctuation(boost)
            interactions_applied.append("dopamine_adrenaline_boost")
        
        if (self.hormones["cortisol"].current_value > 60 and 
            self.hormones["serotonin"].current_value < 40):
            original_rate = self.hormones["cortisol"].recovery_rate
            self.hormones["cortisol"].recovery_rate *= 0.7
            interactions_applied.append("cortisol_slow_recovery")
            self.hormones["cortisol"].recovery_rate = original_rate
        
        if self.hormones["oxytocin"].current_value > 60:
            reduction = self.config.interaction_strength * 20
            self.hormones["cortisol"].apply_fluctuation(-reduction)
            interactions_applied.append("oxytocin_cortisol_reduction")
        
        if interactions_applied:
            self.logger.debug(
                "Applied hormones interactions",
                interactions=interactions_applied
            )

    def _apply_random_fluctuations(self):
        fluctuations_applied = []

        for hormone_name, hormone in self.hormones.items():
            if self.random_gen.probability(self.config.fluctuation_probability):
                min_change, max_change = self.config.fluctuation_range
                change = self.random_gen.uniform(min_change, max_change)
                old_value = hormone.current_value
                hormone.apply_fluctuation(change)

                if abs(hormone.current_value - old_value) > 0.01:
                    fluctuations_applied.append(hormone_name)
        if fluctuations_applied:
            self.logger.debug(
                "Applied random fluctuations",
                hormones=fluctuations_applied
            )

    def apply_event(self, event: TriggerEvent):
        self.logger.info(
            "Applied event to hormonal system",
            event_name = event.name,
            category=event.category,
            intensity=event.intensity
        )

        applied_triggers = self.trigger_manager.apply_event(event, self.hormones)
        self.logger.info(
            "Event applied",
            affected_hormones=list(applied_triggers.keys())
        )

    def get_hormone(self, name:str) -> Optional[Hormone]:
        return self.hormones.get(name)

    def get_all_values(self) ->Dict[str, float]:
        return {name: hormone.current_value
                for name, hormone in self.hormones.items()}

    def get_state_summary(self) -> Dict[str, dict]:
        return  {name: hormone.get_state_description() 
                for name, hormone in self.hormones.items()
                }

    def to_dict(self) -> dict:
        return {
            "hormones": {name: hormone.to_dict()
                         for name, hormone in self.hormones.items()},
            "config": {
                "interaction_strength": self.config.interaction_strength,
                "fluctuation_enabled": self.config.fluctuation_enabled
            }
        }