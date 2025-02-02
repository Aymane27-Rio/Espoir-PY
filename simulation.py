import pygame
import sys
from vehicle import EmergencyVehicle
from arrow import Arrow
from communication import CommunicationModel
from history import History

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guardian Path Simulation")

# Initialize objects
vehicles = [EmergencyVehicle(1, 100, 100), EmergencyVehicle(2, 200, 200)]
comm_model = CommunicationModel(vehicles)
history = History()
arrows = []

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move vehicles
    vehicles[0].move_to(400, 300)
    vehicles[1].move_to(500, 350)
    
    # Draw vehicles and arrows
    for vehicle in vehicles:
        vehicle.draw(screen)
    
    arrows.append(Arrow((vehicles[0].x, vehicles[0].y), (400, 300)))
    arrows.append(Arrow((vehicles[1].x, vehicles[1].y), (500, 350)))

    for arrow in arrows:
        arrow.draw(screen)

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
sys.exit()
