import pygame

class EmergencyVehicle:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.color = (255, 0, 0)  # Red color
        self.speed = 2

    def move_to(self, x, y):
        self.x += (x - self.x) * 0.05  # Smooth movement
        self.y += (y - self.y) * 0.05

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        font = pygame.font.Font(None, 20)
        text = font.render(f"EV{self.id}", True, (255, 255, 255))
        screen.blit(text, (self.x - 10, self.y - 15))
