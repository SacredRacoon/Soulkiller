from typing import Dict, List
from dataclasses import dataclass
from systems.hormonal.hormone import HormoneTrigger

@dataclass
class TriggerEvent:
    name:str
    category: str
    intensity: float
    description: str = ""
    
class TriggerManager:
    def __init__(self):
        self.trigger_database:Dict[str,Dict[str, List[HormoneTrigger]]] ={
            "dopamine": {
                "achievement": [
                    HormoneTrigger("достижение_цели", 25.0, 5.0, 0.15),
                    HormoneTrigger("маленькая_победа", 10.0, 2.0, 0.20),
                ],
                "novelty": [
                    HormoneTrigger("новое_переживание", 15.0, 3.0, 0.18),
                    HormoneTrigger("неожиданность", 8.0, 1.5, 0.25),
                ],
                "social": [
                    HormoneTrigger("социальное_одобрение", 20.0, 4.0, 0.15),
                    HormoneTrigger("похвала", 15.0, 3.0, 0.18),
                ],
                "pleasure": [
                    HormoneTrigger("вкусная_еда", 10.0, 2.0, 0.25),
                    HormoneTrigger("развлечения", 15.0, 3.0, 0.18),
                ]
            },
            "serotonin": {
                "environmental": [
                    HormoneTrigger("солнечный_свет", 10.0, 5.0, 0.10),
                    HormoneTrigger("природа", 12.0, 4.0, 0.12),
                ],
                "physical": [
                    HormoneTrigger("физическая_активность", 15.0, 3.0, 0.15),
                    HormoneTrigger("медитация", 20.0, 5.0, 0.10),
                ],
                "social": [
                    HormoneTrigger("теплый_контакт", 10.0, 3.0, 0.18),
                ],
                "negative": [
                    HormoneTrigger("стресс", -15.0, 4.0, 0.12),
                    HormoneTrigger("одиночество", -8.0, 10.0, 0.08),
                ]
            },
            "cortisol": {
                "threat": [
                    HormoneTrigger("опасность", 35.0, 3.0, 0.08),
                    HormoneTrigger("конфликт", 25.0, 5.0, 0.10),
                ],
                "pressure": [
                    HormoneTrigger("дедлайн", 20.0, 8.0, 0.12),
                    HormoneTrigger("неопределенность", 15.0, 6.0, 0.15),
                ],
                "physical": [
                    HormoneTrigger("недосып", 15.0, 12.0, 0.08),
                    HormoneTrigger("голод", 10.0, 8.0, 0.10),
                ],
                "relief": [
                    HormoneTrigger("безопасность", -20.0, 5.0, 0.15),
                    HormoneTrigger("решение_проблемы", -25.0, 4.0, 0.18),
                ]
            },
            "adrenaline": {
                "excitement": [
                    HormoneTrigger("азарт", 25.0, 2.0, 0.20),
                    HormoneTrigger("риск", 30.0, 3.0, 0.15),
                ],
                "physical": [
                    HormoneTrigger("физическая_нагрузка", 20.0, 4.0, 0.18),
                    HormoneTrigger("кофеин", 25.0, 3.0, 0.12),
                ],
                "emotional": [
                    HormoneTrigger("гнев", 30.0, 2.5, 0.15),
                    HormoneTrigger("страх", 35.0, 2.0, 0.12),
                ]
            },
            "oxytocin": {
                "social": [
                    HormoneTrigger("физический_контакт", 25.0, 3.0, 0.15),
                    HormoneTrigger("доверительный_разговор", 20.0, 4.0, 0.12),
                    HormoneTrigger("помощь_другим", 15.0, 3.0, 0.18),
                ],
                "negative": [
                    HormoneTrigger("предательство", -40.0, 10.0, 0.05),
                    HormoneTrigger("конфликт", -20.0, 5.0, 0.10),
                    HormoneTrigger("изоляция", -10.0, 8.0, 0.08),
                ]
            } 
        }

    def get_triggers_for_event(self, hormone_name: str, event_category: str) -> List[HormoneTrigger]:
        if hormone_name in self.trigger_database:
            if event_category in self.trigger_database[hormone_name]:
                return self.trigger_database[hormone_name][event_category].copy()
        return []

    def apply_event(self, event: TriggerEvent, hormones: Dict[str, 'Hormone']) ->  Dict[str, List[HormoneTrigger]]:
        applied_triggers = {}

        for hormone_name in hormones:
            triggers= self.get_triggers_for_event(hormone_name, event.category)
            if triggers:
                scaled_triggers = []
                for trigger in triggers:
                    scaled_trigger = HormoneTrigger(
                        name=trigger.name,
                        intensity=trigger.intensity  * event.intensity,
                        duration_minutes=trigger.duration_minutes,
                        decay_rate=trigger.decay_rate
                    )
                    scaled_triggers.append(scaled_trigger)
                    hormones[hormone_name].apply_trigger(scaled_trigger)
                applied_triggers[hormone_name] = scaled_triggers

        return applied_triggers
    
    def register_custom_trigger(self, hormone_name: str, category: str, trigger: HormoneTrigger):
        if hormone_name not in self.trigger_database:
            self.trigger_database[hormone_name] = {}

        if category not in self.trigger_database[hormone_name]:
            self.trigger_database[hormone_name][category]=[]

        self.trigger_database[hormone_name][category].append(trigger)