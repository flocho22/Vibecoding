"""Simple pygame front-end for the battle simulator.

Run:
    python pygame_battle.py
"""

from __future__ import annotations

import pygame

from battle_core import FIGHTER_CLASSES, MatchResult, simulate_match

WIDTH, HEIGHT = 1000, 680
BG = (18, 24, 38)
PANEL = (35, 45, 67)
TEXT = (235, 240, 255)
ACCENT = (119, 204, 255)
WIN = (120, 230, 140)


class Button:
    def __init__(self, rect: pygame.Rect, text: str):
        self.rect = rect
        self.text = text

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, active: bool = False) -> None:
        color = ACCENT if active else PANEL
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        label = font.render(self.text, True, TEXT)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def hit(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


def draw_text(screen: pygame.Surface, font: pygame.font.Font, text: str, x: int, y: int, color=TEXT) -> None:
    screen.blit(font.render(text, True, color), (x, y))


def make_fighter_buttons(y: int) -> list[Button]:
    names = [("1", "Mage"), ("2", "Knight"), ("3", "Swordsman")]
    return [Button(pygame.Rect(80 + i * 300, y, 250, 70), f"{k}. {name}") for i, (k, name) in enumerate(names)]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Elemental Battle Simulator")
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("arial", 40, bold=True)
    font = pygame.font.SysFont("arial", 26)
    small = pygame.font.SysFont("consolas", 20)

    state = "pick_p1"
    p1_key = None
    p2_key = None
    rounds = 3
    result: MatchResult | None = None

    fighter_buttons = make_fighter_buttons(220)
    minus_button = Button(pygame.Rect(360, 260, 80, 60), "-")
    plus_button = Button(pygame.Rect(560, 260, 80, 60), "+")
    start_button = Button(pygame.Rect(390, 380, 220, 70), "Start Battle")
    reset_button = Button(pygame.Rect(390, 580, 220, 60), "Play Again")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if state in {"pick_p1", "pick_p2"}:
                    for i, b in enumerate(fighter_buttons, start=1):
                        if b.hit(pos):
                            if state == "pick_p1":
                                p1_key = str(i)
                                state = "pick_p2"
                            else:
                                p2_key = str(i)
                                state = "rounds"
                elif state == "rounds":
                    if minus_button.hit(pos):
                        rounds = max(1, rounds - 1)
                    elif plus_button.hit(pos):
                        rounds = min(15, rounds + 1)
                    elif start_button.hit(pos) and p1_key and p2_key:
                        result = simulate_match(FIGHTER_CLASSES[p1_key], FIGHTER_CLASSES[p2_key], rounds)
                        state = "result"
                elif state == "result" and reset_button.hit(pos):
                    state = "pick_p1"
                    p1_key = p2_key = None
                    rounds = 3
                    result = None

        screen.fill(BG)
        draw_text(screen, title_font, "Elemental Battle Simulator", 250, 50)

        if state == "pick_p1":
            draw_text(screen, font, "Player 1: Pick your fighter", 340, 150)
            for b in fighter_buttons:
                b.draw(screen, font)

        elif state == "pick_p2":
            draw_text(screen, font, f"Player 1 selected: {FIGHTER_CLASSES[p1_key].title}", 320, 140)
            draw_text(screen, font, "Player 2: Pick your fighter", 340, 180)
            for b in fighter_buttons:
                b.draw(screen, font)

        elif state == "rounds":
            draw_text(screen, font, f"P1: {FIGHTER_CLASSES[p1_key].title}    P2: {FIGHTER_CLASSES[p2_key].title}", 270, 160)
            draw_text(screen, font, "Choose number of rounds", 360, 220)
            minus_button.draw(screen, title_font)
            plus_button.draw(screen, title_font)
            draw_text(screen, title_font, str(rounds), 485, 268)
            start_button.draw(screen, font)

        elif state == "result" and result:
            draw_text(screen, font, f"P1: {FIGHTER_CLASSES[p1_key].title}    P2: {FIGHTER_CLASSES[p2_key].title}", 250, 120)
            draw_text(screen, font, f"Round wins -> P1: {result.score[1]} | P2: {result.score[2]} | Draws: {result.score[0]}", 190, 170)
            draw_text(screen, title_font, f"Overall Winner: Player {result.overall_winner}", 245, 230, WIN)
            draw_text(screen, font, "Recent combat log:", 120, 310)
            y = 350
            for line in result.round_results[-1].log[-10:]:
                draw_text(screen, small, line, 120, y)
                y += 26
            reset_button.draw(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
