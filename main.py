from core.persona import Persona
from core.config import PersonaConfig, HormonalSystemConfig, HormoneConfig
from systems.hormonal.triggers import TriggerEvent

def main():
    config = PersonaConfig(
        persona_id="test_persona_001",
        seed=42,
        log_dir="logs",
        debug_mode=True
    )

    persona = Persona(config)
    print("main init")
    print(f"id {config.persona_id}")
    print(f"seed {persona.random_gen.get_seed()}")

    print("starting state")
    initial_state = persona.get_hormonal_state()
    for hormone, value in initial_state.items():
        print(f"    {hormone:12s}: {value:6.2f}")

    print("\n симуляция 10 минут без событий")
    persona.update(10.0)

    state_after = persona.get_hormonal_state()
    print("\n состояние после 10 минут")
    for hormone, value in state_after.items():
        change= value - initial_state[hormone]
        direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
        print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")

    print("\n достижение цели")
    achievement_event = TriggerEvent(
        name="достиг_цели",
        category="achievement",
        intensity=0.8,
        description="Персона успешно завершила важный проект"
    )

    persona.state.hormonal_system.apply_event(achievement_event)

    state_after_event =persona.get_hormonal_state()
    print("\n состояние после события")
    for hormone, value in state_after_event.items():
            change= value - state_after[hormone]
            direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
            print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")
    
    print("\n симуляция 5 минут после события")
    persona.update(5.0)

    final_state = persona.get_hormonal_state()
    print("\n финальное состояние")
    for hormone, value in final_state.items():
        change = value - state_after_event[hormone]  
        direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
        print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")

    print("Симуляция завершена")
    print(f"Логи сохранены в директории {config.log_dir}")
if __name__ == "__main__":
    main()