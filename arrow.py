import pygame
import math

class Arrow:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start, self.end, 2)
        angle = math.atan2(self.end[1] - self.start[1], self.end[0] - self.start[0])
        arrowhead = [
            (self.end[0] - 10 * math.cos(angle - math.pi / 6), self.end[1] - 10 * math.sin(angle - math.pi / 6)),
            self.end,
            (self.end[0] - 10 * math.cos(angle + math.pi / 6), self.end[1] - 10 * math.sin(angle + math.pi / 6)),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), arrowhead)
