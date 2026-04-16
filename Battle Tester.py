"""Elemental Battle Simulator.

Users can:
1) Pick two fighters
2) Choose how many rounds to play
3) Get an overall winner at the end
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class Fighter:
    title: str
    hp: int
    attack: int
    defense: int
    speed: int
    element: str

    def clone_for_round(self) -> "Fighter":
        """Return a copy used in one round so base stats are preserved."""
        return Fighter(
            title=self.title,
            hp=self.hp,
            attack=self.attack,
            defense=self.defense,
            speed=self.speed,
            element=self.element,
        )


FIGHTER_CLASSES = {
    "1": Fighter("Mage", hp=90, attack=24, defense=8, speed=16, element="Arcane"),
    "2": Fighter("Knight", hp=130, attack=18, defense=16, speed=9, element="Steel"),
    "3": Fighter("Swordsman", hp=110, attack=21, defense=12, speed=13, element="Wind"),
}


class BattleSimulator:
    def choose_fighters(self) -> tuple[Fighter, Fighter]:
        print("Welcome to this battle simulator!")
        print("Choose your fighters:")
        print("1. Mage  2. Knight  3. Swordsman")

        player1_choice = self._prompt_choice("Player 1, choose 1, 2, or 3: ")
        player2_choice = self._prompt_choice("Player 2, choose 1, 2, or 3: ")

        player1 = FIGHTER_CLASSES[player1_choice]
        player2 = FIGHTER_CLASSES[player2_choice]

        print(f"\nPlayer 1 chose: {player1.title}")
        print(f"Player 2 chose: {player2.title}\n")

        return player1, player2

    def _prompt_choice(self, prompt: str) -> str:
        while True:
            choice = input(prompt).strip()
            if choice in FIGHTER_CLASSES:
                return choice
            print("Invalid choice. Please enter 1, 2, or 3.")

    def choose_round_count(self) -> int:
        while True:
            raw = input("How many rounds should they fight? (1-15): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= 15:
                return int(raw)
            print("Please enter a whole number from 1 to 15.")

    def fight_round(self, base_p1: Fighter, base_p2: Fighter, round_number: int) -> int:
        """Run a single round.

        Returns:
            1 if player 1 wins, 2 if player 2 wins, 0 for draw.
        """
        p1 = base_p1.clone_for_round()
        p2 = base_p2.clone_for_round()

        print(f"=== ROUND {round_number} ===")
        print(f"{p1.title} (HP {p1.hp}) vs {p2.title} (HP {p2.hp})")

        turn = 1
        while p1.hp > 0 and p2.hp > 0:
            first_num, first, second = self._next_attacker(p1, p2)
            second_num = 2 if first_num == 1 else 1

            damage = self.calculate_damage(first, second)
            second.hp = max(0, second.hp - damage)
            print(
                f"Turn {turn}A: Player {first_num}'s {first.title} "
                f"hits for {damage} damage. Defender HP: {second.hp}"
            )
            if second.hp <= 0:
                break

            counter = self.calculate_damage(second, first)
            first.hp = max(0, first.hp - counter)
            print(
                f"Turn {turn}B: Player {second_num}'s {second.title} "
                f"hits for {counter} damage. Defender HP: {first.hp}"
            )
            turn += 1

        if p1.hp <= 0 and p2.hp <= 0:
            print("Round result: Draw!\n")
            return 0
        if p2.hp <= 0:
            print("Round result: Player 1 wins!\n")
            return 1

        print("Round result: Player 2 wins!\n")
        return 2

    def _next_attacker(self, p1: Fighter, p2: Fighter) -> tuple[int, Fighter, Fighter]:
        if p1.speed > p2.speed:
            return 1, p1, p2
        if p2.speed > p1.speed:
            return 2, p2, p1

        if random.choice([True, False]):
            return 1, p1, p2
        return 2, p2, p1

    @staticmethod
    def calculate_damage(attacker: Fighter, defender: Fighter) -> int:
        variance = random.randint(-4, 4)
        damage = attacker.attack - defender.defense // 2 + variance
        return max(5, damage)

    def run(self) -> None:
        player1, player2 = self.choose_fighters()
        rounds = self.choose_round_count()

        score = {1: 0, 2: 0, 0: 0}

        for i in range(1, rounds + 1):
            winner = self.fight_round(player1, player2, i)
            score[winner] += 1

        print("=== FINAL SCORE ===")
        print(f"Player 1 wins: {score[1]}")
        print(f"Player 2 wins: {score[2]}")
        print(f"Draws: {score[0]}")

        if score[1] > score[2]:
            print("\nOverall winner: Player 1!")
        elif score[2] > score[1]:
            print("\nOverall winner: Player 2!")
        else:
            # Tie breaker guarantees an overall winner.
            print("\nScore is tied. Starting one tiebreaker round!")
            tiebreak_round = rounds + 1
            tie_winner = self.fight_round(player1, player2, tiebreak_round)
            while tie_winner == 0:
                tiebreak_round += 1
                print("Tiebreaker drew again. Running another tiebreaker...")
                tie_winner = self.fight_round(player1, player2, tiebreak_round)

            print(f"Overall winner after tiebreakers: Player {tie_winner}!")


if __name__ == "__main__":
    BattleSimulator().run()
