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
                    HormoneTrigger("goal_achievement", 25.0, 5.0, 0.15),
                    HormoneTrigger("little_win", 10.0, 2.0, 0.20),
                ],
                "novelty": [
                    HormoneTrigger("new_experiences", 15.0, 3.0, 0.18),
                    HormoneTrigger("surprise", 8.0, 1.5, 0.25),
                ],
                "social": [
                    HormoneTrigger("social_approval", 20.0, 4.0, 0.15),
                    HormoneTrigger("praise", 15.0, 3.0, 0.18),
                ],
                "pleasure": [
                    HormoneTrigger("tasty_food", 10.0, 2.0, 0.25),
                    HormoneTrigger("entertainments", 15.0, 3.0, 0.18),
                ]
            },
            "serotonin": {
                "environmental": [
                    HormoneTrigger("sun_light", 10.0, 5.0, 0.10),
                    HormoneTrigger("nature", 12.0, 4.0, 0.12),
                ],
                "physical": [
                    HormoneTrigger("physical_activity", 15.0, 3.0, 0.15),
                    HormoneTrigger("meditation", 20.0, 5.0, 0.10),
                ],
                "social": [
                    HormoneTrigger("warm_contact", 10.0, 3.0, 0.18),
                ],
                "negative": [
                    HormoneTrigger("stress", -15.0, 4.0, 0.12),
                    HormoneTrigger("loneliness", -8.0, 10.0, 0.08),
                ]
            },
            "cortisol": {
                "threat": [
                    HormoneTrigger("danger", 35.0, 3.0, 0.08),
                    HormoneTrigger("conflict", 25.0, 5.0, 0.10),
                ],
                "pressure": [
                    HormoneTrigger("deadline", 20.0, 8.0, 0.12),
                    HormoneTrigger("uncertainty", 15.0, 6.0, 0.15),
                ],
                "physical": [
                    HormoneTrigger("lack_sleep", 15.0, 12.0, 0.08),
                    HormoneTrigger("hunger", 10.0, 8.0, 0.10),
                ],
                "relief": [
                    HormoneTrigger("safety", -20.0, 5.0, 0.15),
                    HormoneTrigger("problem_solving", -25.0, 4.0, 0.18),
                ]
            },
            "adrenaline": {
                "excitement": [
                    HormoneTrigger("gamble", 25.0, 2.0, 0.20),
                    HormoneTrigger("risk", 30.0, 3.0, 0.15),
                ],
                "physical": [
                    HormoneTrigger("physical_activity", 20.0, 4.0, 0.18),
                    HormoneTrigger("caffeine", 25.0, 3.0, 0.12),
                ],
                "emotional": [
                    HormoneTrigger("anger", 30.0, 2.5, 0.15),
                    HormoneTrigger("fear", 35.0, 2.0, 0.12),
                ]
            },
            "oxytocin": {
                "social": [
                    HormoneTrigger("physical_contact", 25.0, 3.0, 0.15),
                    HormoneTrigger("confidential_conversation", 20.0, 4.0, 0.12),
                    HormoneTrigger("helping_    others", 15.0, 3.0, 0.18),
                ],
                "negative": [
                    HormoneTrigger("betrayal", -40.0, 10.0, 0.05),
                    HormoneTrigger("conflict", -20.0, 5.0, 0.10),
                    HormoneTrigger("isolation", -10.0, 8.0, 0.08),
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