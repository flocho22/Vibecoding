"""Shared battle simulator logic used by CLI and pygame UI."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional


@dataclass(frozen=True)
class Fighter:
    title: str
    hp: int
    attack: int
    defense: int
    speed: int
    element: str


FIGHTER_CLASSES: dict[str, Fighter] = {
    "1": Fighter("Mage", hp=90, attack=24, defense=8, speed=16, element="Arcane"),
    "2": Fighter("Knight", hp=130, attack=18, defense=16, speed=9, element="Steel"),
    "3": Fighter("Swordsman", hp=110, attack=21, defense=12, speed=13, element="Wind"),
}


@dataclass
class RoundResult:
    winner: int  # 0 draw, 1 p1, 2 p2
    p1_hp: int
    p2_hp: int
    log: list[str]


@dataclass
class MatchResult:
    rounds_requested: int
    round_results: list[RoundResult]
    score: dict[int, int]
    overall_winner: int


def _next_attacker(p1: Fighter, p2: Fighter, rng: random.Random) -> tuple[int, Fighter, Fighter]:
    if p1.speed > p2.speed:
        return 1, p1, p2
    if p2.speed > p1.speed:
        return 2, p2, p1
    return (1, p1, p2) if rng.choice([True, False]) else (2, p2, p1)


def calculate_damage(attacker: Fighter, defender: Fighter, rng: random.Random) -> int:
    variance = rng.randint(-4, 4)
    return max(5, attacker.attack - defender.defense // 2 + variance)


def simulate_round(p1: Fighter, p2: Fighter, rng: random.Random) -> RoundResult:
    p1_hp, p2_hp = p1.hp, p2.hp
    log: list[str] = [f"{p1.title} vs {p2.title}"]

    turn = 1
    while p1_hp > 0 and p2_hp > 0:
        first_num, first, second = _next_attacker(p1, p2, rng)
        second_num = 2 if first_num == 1 else 1

        if first_num == 1:
            dmg = calculate_damage(first, second, rng)
            p2_hp = max(0, p2_hp - dmg)
            log.append(f"T{turn}A: P1 deals {dmg} ({p2_hp} HP left)")
            if p2_hp <= 0:
                break
            counter = calculate_damage(second, first, rng)
            p1_hp = max(0, p1_hp - counter)
            log.append(f"T{turn}B: P2 deals {counter} ({p1_hp} HP left)")
        else:
            dmg = calculate_damage(first, second, rng)
            p1_hp = max(0, p1_hp - dmg)
            log.append(f"T{turn}A: P2 deals {dmg} ({p1_hp} HP left)")
            if p1_hp <= 0:
                break
            counter = calculate_damage(second, first, rng)
            p2_hp = max(0, p2_hp - counter)
            log.append(f"T{turn}B: P1 deals {counter} ({p2_hp} HP left)")

        turn += 1

    winner = 0
    if p1_hp <= 0 and p2_hp <= 0:
        winner = 0
    elif p2_hp <= 0:
        winner = 1
    elif p1_hp <= 0:
        winner = 2

    return RoundResult(winner=winner, p1_hp=p1_hp, p2_hp=p2_hp, log=log)


def simulate_match(
    p1: Fighter,
    p2: Fighter,
    rounds: int,
    seed: Optional[int] = None,
) -> MatchResult:
    rng = random.Random(seed)
    score = {0: 0, 1: 0, 2: 0}
    results: list[RoundResult] = []

    for _ in range(rounds):
        rr = simulate_round(p1, p2, rng)
        results.append(rr)
        score[rr.winner] += 1

    while score[1] == score[2]:
        rr = simulate_round(p1, p2, rng)
        results.append(rr)
        score[rr.winner] += 1

    overall = 1 if score[1] > score[2] else 2
    return MatchResult(
        rounds_requested=rounds,
        round_results=results,
        score=score,
        overall_winner=overall,
    )
