# src/code_in_bloom/fireworks/firework.py
import random
import math
import pygame

from .particle import Particle
from .constants import WIDTH, HEIGHT, COLORS


class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = random.choice(COLORS)
        self.particles = []
        self.exploded = False

        self.speed = random.uniform(-15, -12)
        self.vy = self.speed
        self.vx = 0
        self.target_y = random.randint(HEIGHT // 3, HEIGHT // 2)
        self.color_fade = 1.0

    def update(self):
        if not self.exploded:
            self.vx += random.uniform(-0.05, 0.05)
            self.x += self.vx
            self.vy += 0.1
            self.y += self.vy

            if self.vy >= 0 or self.y <= self.target_y:
                self.explode()
        else:
            for p in self.particles:
                p.update()

            self.color_fade -= 0.01
            if self.color_fade < 0:
                self.color_fade = 0

            for p in self.particles:
                p.color = (
                    min(int(p.color[0] * self.color_fade), 255),
                    min(int(p.color[1] * self.color_fade), 255),
                    min(int(p.color[2] * self.color_fade), 255),
                )

            self.particles = [p for p in self.particles if p.life > 0]

    def explode(self):
        self.exploded = True
        num_particles = random.randint(220, 320)

        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.5, 6)
            size = random.uniform(1, 3)
            self.particles.append(Particle(self.x, self.y, self.color, angle, speed, size))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
        else:
            for p in self.particles:
                p.draw(surface)
