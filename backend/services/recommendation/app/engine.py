from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Arm:
    successes: int = 1
    failures: int = 1


class ThompsonBandit:
    def __init__(self, arms: list[str]) -> None:
        self._arms = {arm: Arm() for arm in arms}

    def select(self) -> str:
        samples = {
            name: random.betavariate(arm.successes, arm.failures)
            for name, arm in self._arms.items()
        }
        return max(samples, key=samples.get)

    def update(self, arm_name: str, reward: bool) -> None:
        arm = self._arms[arm_name]
        if reward:
            arm.successes += 1
        else:
            arm.failures += 1
