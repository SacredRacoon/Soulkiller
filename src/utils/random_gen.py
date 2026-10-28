import random
from typing import Optional, List, Tuple
import numpy as np

class SeededRandom:
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed if seed is not None else random.randint(0, 2**32 -1)
        self.rng = random.Random(self.seed)
        self.np_rng = np.random.RandomState(self.seed)
        self.call_count = 0

    def get_seed(self) -> int:
        return self.seed

    def reset(self,new_seed: Optional[int] = None):
        if new_seed is not None:
            self.seed = new_seed
        self.rng = random.Random(self.seed)
        self.np_rng = np.random.RandomState(self.seed)
        self.call_count = 0

    def uniform(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        self.call_count += 1
        return self.rng.uniform(min_val, max_val)

    def randint(self, min_val: int, max_val: int) -> int:
        self.call_count += 1
        return self.rng.randint(min_val,max_val)

    def gauss(self, mu: float, sigma: float) -> float:
        self.call_count += 1
        return self.rng.gauss(mu,sigma)

    def choice(self, sequence: List) -> any:
        self.call_count += 1
        return self.rng.choice(sequence)

    def weighted_choice(self, items: List, weights: List[float]) -> any:
        self.call_count += 1
        return self.rng.choices(items, weights=weights, k=1)[0]

    def probability(self, chance: float) ->bool:
        self.call_count += 1
        return self.rng.random() < chance

    def floctuation(self,base_value: float, min_change: float = -0.02, max_change: float = 0.02) -> float:
        self.call_count += 1
        change = self.rng.uniform(min_change, max_change)
        return base_value + change

    def normal_fluctuation(self, base_value: float, std_dev: float = 0.01) -> float:
        self.call_count += 1
        change = self.rng.gauss(0, std_dev)
        return base_value + change

    def get_stats(self) -> dict:
        return {"seed": self.seed, "call_count": self.call_count}