import random
import pygame
from game.player import Player
from game.anvil import Anvil
from game.particle import Particle


BASE_SPAWN_DELAY = 700   # ms between anvils at the start of a run
MIN_SPAWN_DELAY = 200    # ms floor so the game never becomes impossible
DELAY_DROP_PER_SEC = 12  # ms shaved off the delay for every second survived
SHAKE_FRAMES = 8         # how long the screen shakes after an impact
SHAKE_MAGNITUDE = 4      # max pixel offset of the shake
DUST_PER_IMPACT = 12     # dust particles spawned per impact
BG_COLOR = (35, 38, 45)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(width, height)
        self.anvils = []
        self.particles = []
        self.shake_frames = 0
        self.ground_y = height - 20
        self.scene = pygame.Surface((width, height))

        self.spawn_delay = BASE_SPAWN_DELAY
        self.last_spawn_time = pygame.time.get_ticks()

        self.start_ticks = pygame.time.get_ticks()
        self.survival_time = 0
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 52)
        self.font_medium = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update(self):
        if self.game_state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()

        self.player.update()

        self.survival_time = (pygame.time.get_ticks() - self.start_ticks) // 1000

        # Dynamic difficulty: spawn faster the longer the player survives
        self.spawn_delay = max(
            MIN_SPAWN_DELAY,
            BASE_SPAWN_DELAY - self.survival_time * DELAY_DROP_PER_SEC,
        )

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            self.anvils.append(Anvil(self.width))
            self.last_spawn_time = now

        player_rect = self.player.rect
        for anvil in self.anvils[:]:
            anvil.update()

            if player_rect.colliderect(anvil.rect):
                self.game_state = "GAME_OVER"

            if anvil.hits_ground(self.ground_y):
                self.spawn_impact(anvil)
                self.anvils.remove(anvil)
            elif anvil.is_off_screen(self.height):
                self.anvils.remove(anvil)

        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

        if self.shake_frames > 0:
            self.shake_frames -= 1

        if self.game_state == "GAME_OVER":
            self.shake_frames = 0

    def spawn_impact(self, anvil):
        """Dust puff + brief screen shake where an anvil lands."""
        impact_x = anvil.x + anvil.width / 2
        for _ in range(DUST_PER_IMPACT):
            self.particles.append(Particle(impact_x + random.uniform(-12, 12), self.ground_y))
        self.shake_frames = SHAKE_FRAMES

    def reset(self):
        self.player = Player(self.width, self.height)
        self.anvils.clear()
        self.particles.clear()
        self.shake_frames = 0
        self.spawn_delay = BASE_SPAWN_DELAY
        self.start_ticks = pygame.time.get_ticks()
        self.last_spawn_time = pygame.time.get_ticks()
        self.survival_time = 0
        self.game_state = "PLAYING"

    def render(self, target):
        # Draw the whole frame off-screen first, so it can be shaken as one piece
        screen = self.scene
        screen.fill(BG_COLOR)

        ground_y = self.ground_y
        pygame.draw.rect(screen, (70, 75, 85), (0, ground_y, self.width, 20))
        pygame.draw.line(screen, (160, 90, 40), (0, ground_y), (self.width, ground_y), 3)

        self.player.render(screen)
        for anvil in self.anvils:
            anvil.render(screen)
        for particle in self.particles:
            particle.render(screen)

        time_surf = self.font_medium.render(f"Survival Time: {self.survival_time}s", True, (240, 240, 240))
        screen.blit(time_surf, (20, 20))

        inst_surf = self.font_small.render("Use [A/D] or [Arrow Keys] to Dodge", True, (170, 175, 185))
        screen.blit(inst_surf, (self.width - inst_surf.get_width() - 20, 25))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("CRUSHED! GAME OVER", True, (235, 65, 65))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 60))

            score_surf = self.font_medium.render(f"You survived: {self.survival_time} seconds", True, (255, 255, 255))
            screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, self.height // 2))

            restart_surf = self.font_small.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))

        # Blit the finished frame, offset randomly while the screen is shaking
        offset = (0, 0)
        if self.shake_frames > 0:
            mag = max(1, SHAKE_MAGNITUDE * self.shake_frames // SHAKE_FRAMES)
            offset = (random.randint(-mag, mag), random.randint(-mag, mag))
        target.fill(BG_COLOR)
        target.blit(self.scene, offset)
