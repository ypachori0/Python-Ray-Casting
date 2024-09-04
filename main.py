import pygame
import math 

#initialize pygame
pygame.init()

#screen dimensions
nScreenWidth = 120 #window width
nScreenHeight = 120 #window height
screen = pygame.display.set_mode((nScreenWidth*8, nScreenHeight*8)) #scaling it up by 8 for better visibility

#player positions and direction
fPlayerX = 2.0
fPlayerY = 2.0
fPlayerA = 0.0 #this is the player's angle

#fov and depth
fFOV = math.pi/4.0
fDepth = 16.0

#load map
def load_map(file_path):
    with open(file_path, 'r') as f:
        map_data = f.read().splitlines()
    return map_data 

#load map from map.txt
game_map = load_map('map.txt')

#update map dimensions based on loaded map
nMapWidth = len(game_map[0])
nMapHeight = len(game_map)

#set up timing
clock = pygame.time.Clock()

def handle_input():
    global fPlayerX, fPlayerY, fPlayerA
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        fPlayerA -= 0.1 #rotate left
    if keys[pygame.K_RIGHT]:
        fPlayerA += 0.1 #rotate right
    if keys[pygame.K_UP]:
        fPlayerX += math.cos(fPlayerA)*0.1 #move forward
        fPlayerY += math.sin(fPlayerA)*0.1
        #check for collision
        if game_map[int(fPlayerY)][int(fPlayerX)] == '#':
            fPlayerX -= math.cos(fPlayerA)*0.1
            fPlayerY -= math.sin(fPlayerA)*0.1
        
#implement ray casting
def render_scene():
    screen.fill((0, 0, 0))  # Clear screen

    for x in range(nScreenWidth):
        fRayAngle = (fPlayerA - fFOV / 2.0) + (x / nScreenWidth) * fFOV

        fDistanceToWall = 0.0
        hit_wall = False

        fEyeX = math.cos(fRayAngle)
        fEyeY = math.sin(fRayAngle)

        while not hit_wall and fDistanceToWall < fDepth:
            fDistanceToWall += 0.1
            nTestX = int(fPlayerX + fEyeX * fDistanceToWall)
            nTestY = int(fPlayerY + fEyeY * fDistanceToWall)

            # Check if ray is out of bounds
            if nTestX < 0 or nTestX >= nMapWidth or nTestY < 0 or nTestY >= nMapHeight:
                hit_wall = True  # Ray is out of bounds
                fDistanceToWall = fDepth
            else:
                # Ray is in bounds so test to see if the ray cell is a wall block
                if game_map[nTestY][nTestX] == '#':
                    hit_wall = True

        # Calculate distance to ceiling and floor
        nCeiling = int(nScreenHeight / 2.0 - nScreenHeight / fDistanceToWall)
        nFloor = nScreenHeight - nCeiling

        # Ensure shade is within valid range
        shade = max(0, min(255, int(255 / fDistanceToWall)))
        wall_color = (shade, shade, shade)

        # Draw the wall
        for y in range(nScreenHeight):
            if y < nCeiling:
                screen.set_at((x * 8, y * 8), (0, 0, 0))  # Ceiling
            elif y > nCeiling and y <= nFloor:
                screen.set_at((x * 8, y * 8), wall_color)  # Wall
            else:
                # Floor shading
                b = max(0, min(255, int(255 * (y - nScreenHeight / 2.0) / (nScreenHeight / 2.0))))
                floor_color = (b // 2, b // 2, b)
                screen.set_at((x * 8, y * 8), floor_color)

        
#game loop
running = True
while running:
    handle_input()
    render_scene()
    pygame.display.flip()
    clock.tick(30) #limit to 30 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()