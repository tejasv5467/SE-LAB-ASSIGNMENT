import random
import pygame


class Particle:
    """A small dust particle kicked up when an anvil hits the ground."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3.5, 3.5)
        self.vy = random.uniform(-4.5, -1.0)
        self.size = random.randint(3, 6)
        self.max_life = random.randint(18, 30)
        self.life = self.max_life

    @property
    def alive(self):
        return self.life > 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25   # gravity
        self.vx *= 0.96   # air drag
        self.life -= 1

    def render(self, surface):
        radius = max(1, int(self.size * self.life / self.max_life))
        pygame.draw.circle(surface, (165, 150, 130), (int(self.x), int(self.y)), radius)
