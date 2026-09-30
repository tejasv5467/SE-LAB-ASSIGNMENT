import random
import pygame


MIN_SPEED = 4.5
MAX_SPEED = 7.0


class Anvil:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.width = 40
        self.height = 32
        self.x = random.randint(20, screen_width - self.width - 20)
        self.y = -self.height
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED)

    def update(self):
        self.y += self.speed

    def is_off_screen(self, screen_height):
        return self.y > screen_height + 10

    def hits_ground(self, ground_y):
        return self.y + self.height >= ground_y

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def _tint(self, cool, hot):
        """Blend from a grey (slow anvil) to an orange/red (fast anvil)."""
        t = (self.speed - MIN_SPEED) / (MAX_SPEED - MIN_SPEED)
        t = max(0.0, min(1.0, t))
        return tuple(int(c + (h - c) * t) for c, h in zip(cool, hot))

    def render(self, surface):
        top_color = self._tint((120, 120, 130), (255, 140, 40))
        base_color = self._tint((80, 80, 90), (200, 60, 30))
        edge_color = self._tint((200, 200, 210), (255, 190, 100))

        top_rect = pygame.Rect(int(self.x) + 4, int(self.y), self.width - 8, 14)
        pygame.draw.rect(surface, top_color, top_rect, border_radius=2)

        base_rect = pygame.Rect(int(self.x), int(self.y) + 14, self.width, 18)
        pygame.draw.rect(surface, base_color, base_rect, border_radius=3)
        pygame.draw.rect(surface, edge_color, base_rect, width=1, border_radius=3)
