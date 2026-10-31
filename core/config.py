from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class HormoneConfig:
    name:str
    baseline: float = 50.0
    recory_rate: float = 1.0
    sensitivity: float = 1.0
    min_value: float = 0.0
    max_value: float = 100.0

@dataclass
class HormonalSystemConfig:
    hormones: Dict[str, HormoneConfig] = field(default_factory=dict)
    interaction_strength: float = 0.15
    cross_influence_enabled: bool = True
    update_interval_minutes: float = 1.0
    fluctuation_enabled: bool = True
    fluctuation_probability: float = 0.30
    fluctuation_range: tuple = (-0.02, 0.02)

    def __post__init__(self):
        if not self.hormones:
            self.hormones = {
                "dopamine": HormoneConfig(
                    name="dopamine",
                    baseline=55.0,
                    recovery_rate=1.2,
                    sensitivity=1.0
                ),
                "serotonin": HormoneConfig(
                    name="serotonin",
                    baseline=50.0,
                    recovery_rate=1.0,
                    sensitivity=1.0
                ),
                "cortisol": HormoneConfig(
                    name="cortisol",
                    baseline=45.0,
                    recovery_rate=0.8,
                    sensitivity=1.1
                ),
                "adrenaline": HormoneConfig(
                    name="adrenaline",
                    baseline=40.0,
                    recovery_rate=1.5,
                    sensitivity=0.9
                ),
                "oxytocin": HormoneConfig(
                    name="oxytocin",
                    baseline=50.0,
                    recovery_rate=1.0,
                    sensitivity=1.0
                )
            }

@dataclass
class PersonaConfig:
    persona_id: str
    seed: Optional[int] = None
    log_dir: str = "logs"

    hormonal: HormonalSystemConfig = field(default_factory=HormonalSystemConfig)

    debug_mode: bool = False
    verbose_logging: bool = True
