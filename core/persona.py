from typing import Dict, Optional
from core.state import PersonaState
from core.config import PersonaConfig
from utils.random_gen import SeededRandom
from utils.logger import PersonaLogger


class Persona:
    def __init__(self, config: PersonaConfig):
        self.config = config
        self.logger = PersonaLogger(config.persona_id, config.log_dir)
        self.random_gen = SeededRandom(config.seed)

        self.logger.info(
            "Персона создана",
            persona_id=config.persona_id,
            seed=self.random_gen.get_seed()
        )

        self.state = PersonaState(config, self.random_gen, self.logger)

    def update(self, time_delta_minutes: float):
        self.state.update(time_delta_minutes)

    def get_hormonal_state(self) -> dict:
        return self.state.hormonal_system.get_all_values()

    def to_dict(self) -> dict:
        return {
            "persona_id": self.config.persona_id,
            "seed": self.random_gen.get_seed(),
            "state": self.state.to_dict()
        }