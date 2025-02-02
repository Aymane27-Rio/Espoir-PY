import pygame
import sys
import heapq
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guardian Path Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (255, 69, 0)
GREEN = (0, 200, 0)
BLUE = (30, 144, 255)
GRAY = (120, 120, 120)
YELLOW = (255, 223, 0)

# City grid settings
GRID_SIZE = 50
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Vehicle class
class Vehicle:
    def __init__(self, x, y, color, special=False):
        self.x = x
        self.y = y
        self.color = color
        self.special = special
        self.path = []
        self.speed = GRID_SIZE // 10 if not special else GRID_SIZE // 5
        self.stopped = False
        self.destination_reached = False
        self.direction = random.choice([(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)])

    def move(self):
        if self.path:
            self.x, self.y = self.path.pop(0)
            if not self.path:
                self.destination_reached = True
        elif not self.stopped:
            possible_moves = [(self.x + dx, self.y + dy) for dx, dy in [(-GRID_SIZE, 0), (GRID_SIZE, 0), (0, -GRID_SIZE), (0, GRID_SIZE)]]
            random.shuffle(possible_moves)
            for new_x, new_y in possible_moves:
                if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
                    self.x, self.y = new_x, new_y
                    break

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 3)
        if self.special:
            pygame.draw.circle(screen, YELLOW, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), GRID_SIZE // 4, 2)

# Node class (for pathfinding & signals)
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.signal_active = False

    def draw(self, screen):
        color = GREEN if self.signal_active else GRAY
        pygame.draw.circle(screen, color, (self.x + GRID_SIZE // 2, self.y + GRID_SIZE // 2), 8)

# Generate road nodes
nodes = {(x * GRID_SIZE, y * GRID_SIZE): Node(x * GRID_SIZE, y * GRID_SIZE) for x in range(COLS) for y in range(ROWS)}

# Vehicles (regular and special)
vehicles = [Vehicle(random.randint(0, COLS - 1) * GRID_SIZE, random.randint(0, ROWS - 1) * GRID_SIZE, BLUE) for _ in range(5)]
special_vehicle = Vehicle(100, 100, RED, special=True)

# Dijkstra's Algorithm for shortest path
def dijkstra(start, end):
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {}
    
    while queue:
        current_distance, current = heapq.heappop(queue)
        
        if current == end:
            path = []
            while current in previous_nodes:
                path.append(current)
                current = previous_nodes[current]
            return path[::-1]
        
        for dx, dy in [(-GRID_SIZE, 0), (GRID_SIZE, 0), (0, -GRID_SIZE), (0, GRID_SIZE)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if neighbor in distances:
                continue
            
            distances[neighbor] = current_distance + 1
            previous_nodes[neighbor] = current
            heapq.heappush(queue, (distances[neighbor], neighbor))
    return []

# Game loop
running = True
selected_destination = None
start_movement = False
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected_destination = (mouse_x // GRID_SIZE * GRID_SIZE, mouse_y // GRID_SIZE * GRID_SIZE)
            special_vehicle.path = dijkstra((special_vehicle.x, special_vehicle.y), selected_destination)
            special_vehicle.destination_reached = False
            start_movement = False
            for pos in special_vehicle.path:
                if pos in nodes:
                    nodes[pos].signal_active = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start_movement = True
    
    for node in nodes.values():
        node.draw(screen)
    
    for vehicle in vehicles:
        if any(abs(vehicle.x - node.x) < GRID_SIZE and abs(vehicle.y - node.y) < GRID_SIZE for node in nodes.values() if node.signal_active):
            vehicle.stopped = True
        else:
            vehicle.stopped = False
            vehicle.move()
        vehicle.draw(screen)
    
    if start_movement and not special_vehicle.destination_reached:
        special_vehicle.move()
    elif special_vehicle.destination_reached:
        for node in nodes.values():
            node.signal_active = False
    special_vehicle.draw(screen)
    
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
