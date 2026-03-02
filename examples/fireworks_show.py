# examples/fireworks_show.py
import pygame
import random

from code_in_bloom.fireworks.constants import WIDTH, HEIGHT, FPS, BLACK
from code_in_bloom.fireworks.firework import Firework


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fireworks in Bloom")
    clock = pygame.time.Clock()

    fireworks = []
    running = True

    spawn_event = pygame.USEREVENT + 1

    
    pygame.time.set_timer(spawn_event, 900)  

    
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    fade_alpha = 70  

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_event:
                
                if len(fireworks) < 25:
                    for _ in range(random.randint(6, 10)):
                        fireworks.append(Firework())

        for f in fireworks:
            f.update()

        fireworks = [f for f in fireworks if (not f.exploded) or len(f.particles) > 0]

        
        fade.set_alpha(fade_alpha)
        screen.blit(fade, (0, 0))

        for f in fireworks:
            f.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()