from typing import Dict, Optional
from systems.hormonal.system import HormonalSystem
from utils.random_gen import SeededRandom
from utils.logger import PersonaLogger
from core.config import PersonaConfig

class PersonaState:
    def __init__(self, config: PersonaConfig, random_gen: SeededRandom, logger: PersonaLogger):
        self.config = config
        self.random_gen = random_gen
        self.logger = logger

        self.hormonal_system = HormonalSystem(
            config.hormonal, logger, random_gen
        )

        self.logger.info("Состояние персоны инит")

    def update(self, time_delta_minutes:float):
        self.logger.debug(
            "Начало обновления состояния персоны",
            time_delta = time_delta_minutes
        )

        self.hormonal_system.update(time_delta_minutes)

        self.logger.debug("Завершение обновления состояния персоны")

    def to_dict(self) -> dict:
        return {
            "hormonal_system": self.hormonal_system.to_dict()
        }