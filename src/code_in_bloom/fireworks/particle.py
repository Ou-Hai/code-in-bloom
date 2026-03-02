# src/code_in_bloom/fireworks/particle.py
import math
import pygame


class Particle:
    def __init__(self, x, y, color, angle, speed, size):
        self.x = x
        self.y = y
        self.color = color
        self.angle = angle
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.02
        self.drag = 0.95
        self.size = size
        self.life = 100
        self.fade = 2
        self.history = []
        self.max_history = 20

    def update(self):
        self.vx *= self.drag
        self.vy *= self.drag
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size *= 0.98
        self.size = max(self.size, 1)

        self.color = (
            min(int(self.color[0] * 0.98), 255),
            min(int(self.color[1] * 0.98), 255),
            min(int(self.color[2] * 0.98), 255),
        )

        self.history.append({"x": self.x, "y": self.y, "alpha": 255})
        if len(self.history) > self.max_history:
            self.history.pop(0)

        for point in self.history:
            point["alpha"] -= 10
            point["alpha"] = max(point["alpha"], 0)

        from .constants import HEIGHT
        if self.y > HEIGHT + 10:
            self.life = 0

    def draw(self, surface):
        if self.life > 0:
            if len(self.history) > 1:
                for i in range(len(self.history) - 1):
                    cur = self.history[i]
                    nxt = self.history[i + 1]
                    alpha = cur["alpha"]

                    color = (
                        min(int(self.color[0] * (alpha / 255)), 255),
                        min(int(self.color[1] * (alpha / 255)), 255),
                        min(int(self.color[2] * (alpha / 255)), 255),
                    )
                    pygame.draw.line(surface, color, (cur["x"], cur["y"]), (nxt["x"], nxt["y"]), 2)

            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
