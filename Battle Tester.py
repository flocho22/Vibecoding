"""CLI entry point for the battle simulator."""

from __future__ import annotations

from battle_core import FIGHTER_CLASSES, simulate_match


class BattleSimulatorCLI:
    def _prompt_choice(self, prompt: str) -> str:
        while True:
            choice = input(prompt).strip()
            if choice in FIGHTER_CLASSES:
                return choice
            print("Invalid choice. Please enter 1, 2, or 3.")

    def choose_fighters(self):
        print("Welcome to this battle simulator!")
        print("Choose your fighters:")
        print("1. Mage  2. Knight  3. Swordsman")

        p1 = FIGHTER_CLASSES[self._prompt_choice("Player 1, choose 1, 2, or 3: ")]
        p2 = FIGHTER_CLASSES[self._prompt_choice("Player 2, choose 1, 2, or 3: ")]
        print(f"\nPlayer 1 chose: {p1.title}")
        print(f"Player 2 chose: {p2.title}\n")
        return p1, p2

    def choose_round_count(self) -> int:
        while True:
            raw = input("How many rounds should they fight? (1-15): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= 15:
                return int(raw)
            print("Please enter a whole number from 1 to 15.")

    def run(self) -> None:
        p1, p2 = self.choose_fighters()
        rounds = self.choose_round_count()

        result = simulate_match(p1, p2, rounds)

        for i, round_result in enumerate(result.round_results, start=1):
            print(f"=== ROUND {i} ===")
            print(f"{p1.title} (HP {p1.hp}) vs {p2.title} (HP {p2.hp})")
            for line in round_result.log[1:]:
                print(line)
            if round_result.winner == 0:
                print("Round result: Draw!\n")
            else:
                print(f"Round result: Player {round_result.winner} wins!\n")

        print("=== FINAL SCORE ===")
        print(f"Player 1 wins: {result.score[1]}")
        print(f"Player 2 wins: {result.score[2]}")
        print(f"Draws: {result.score[0]}")
        print(f"\nOverall winner: Player {result.overall_winner}!")


if __name__ == "__main__":
    BattleSimulatorCLI().run()
