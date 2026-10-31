import logging
import os
from datetime import datetime
from typing import Optional

class PersonaLogger:
    def __init__(self,persona_id: str, log_dir: str = "logs"):
        self.persona_id = persona_id
        self.log_dir = log_dir

        os.makedirs(log_dir, exist_ok=True)

        self.logger = logging.getLogger(f"persona_{persona_id}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = logging.FileHandler(
            os.path.join(log_dir, f"persona_{persona_id}_full.log"),
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        important_handler = logging.FileHandler(
            os.path.join(log_dir, f"persona_{persona_id}_important.log"),
            mode='a',
            encoding='utf-8'
        )
        important_handler.setLevel(logging.INFO)
        important_handler.setFormatter(formatter)
        self.logger.addHandler(important_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, **kwargs):
        formatted = self._format_message(message,**kwargs)
        self.logger.debug(formatted)

    def info(self, message: str, **kwargs):
        formatted = self._format_message(message,**kwargs)
        self.logger.info(formatted)

    def warning(self, message: str, **kwargs):
        formatted = self._format_message(message,**kwargs)
        self.logger.warning(formatted)

    def error(self, message: str, **kwargs):
        formatted = self._format_message(message,**kwargs)
        self.logger.error(formatted)

    def hormone_change(self, hormone_name: str, old_value: float, new_value: float, reason: str, **kwargs):
        change = new_value - old_value
        direction = "UP" if change > 0 else "DOWN" if change < 0 else "="

        message = (f"Гормон [{hormone_name}]"
                   f"{old_value:.2f} changed to {new_value:.2f}"
                   f"({direction}{abs(change):.2f}), причина {reason}")

        self.info(message, **kwargs)

    def _format_message(self, message: str, **kwargs) -> str:
        if kwargs:
            params = ", ".join(f"{k}={v}" for k,v in kwargs.items())
            return f"{message} | {params}"
        return message