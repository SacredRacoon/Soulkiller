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

    print("\n 10 minutes simulation without events")
    persona.update(10.0)

    state_after = persona.get_hormonal_state()
    print("\n state after 10 minutes")
    for hormone, value in state_after.items():
        change= value - initial_state[hormone]
        direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
        print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")

    print("\n goal completed")
    achievement_event = TriggerEvent(
        name="goal_achievement",
        category="achievement",
        intensity=0.8,
        description="Persona succesfuly complete important project"
    )

    persona.state.hormonal_system.apply_event(achievement_event)

    state_after_event =persona.get_hormonal_state()
    print("\n state after event")
    for hormone, value in state_after_event.items():
            change= value - state_after[hormone]
            direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
            print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")
    
    print("\n 5 minutes simulation after event")
    persona.update(5.0)

    final_state = persona.get_hormonal_state()
    print("\n final state")
    for hormone, value in final_state.items():
        change = value - state_after_event[hormone]  
        direction = "UP " if change > 0 else "DOWN " if change < 0 else "="
        print(f"    {hormone:12s}: {value:6.2f} ({direction}{abs(change):.2f})")

    print("Simulation ended")
    print(f"Logs saved to {config.log_dir}")
if __name__ == "__main__":
    main()