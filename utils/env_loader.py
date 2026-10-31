import os
from pathlib import Path
from dotenv import load_dotenv

class EnvLoader:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, env_file: str = ".env"):
        if not self._initialized:
            env_path = Path(env_file)
            if env_path.exists():
                load_dotenv(env_path)
            else:
                print(f"Warning {env_file} not found, using env variables")

            self._initialized = True

    @classmethod
    def get_instance(cls, env_file: str =".env") -> 'EnvLoader':
        if cls._instance is None:
            cls._instance = cls(env_file)
        return cls._instance

    def get(self, key: str, default: int = 0) -> int:
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        value = self.get(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default

    def getbool(self, key: str, default: bool = False) -> bool:
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    def get_required(self, key: str) -> str:
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required env variable {key} not found")
        return value