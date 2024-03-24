# main.py
import pygame
from Characters import Character, Teammate, Player  # Assuming the filename is Character.py

# Initialize Pygame and setup window...
pygame.init()
clock = pygame.time.Clock()
infoObject = pygame.display.Info()
screen_height, screen_width = infoObject.current_w, infoObject.current_h
window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Game Window!")

# Initialize font
font_size = 24
game_font = pygame.font.SysFont('Arial', font_size)

player = Player('Me', 200, 200, 50, 50, 10, 'standby', 100, 0.2, 15, 'Pistol', 0, 'Sarge')

# Setup teammates...
teammates = [Teammate('Raymond', 'Red', 50, 50, 50, 50, 1, 'standby', 100, 0.2, 15, 'AR', 0, 'Medic', 1, True),
              Teammate('Gary', 'Green', 100, 100, 50, 50, 1, 'standby', 100, 0.2, 15, 'MG', 0, 'Gunner', 1, False),
              Teammate('Bert', 'Blue', 150, 150, 50, 50, 1, 'standby', 100, 0.2, 15, 'SMG', 0, 'Engineer', 1, False)]

active_character = teammates[0]
running = True
# Game loop...
while running:
    pygame.time.delay(10)
    # Handle events including mouse and keyboard input...
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            mouseX, mouseY = event.pos
            for char in teammates:
                char.isActive = char.xPos <= mouseX <= char.xPos + char.width and char.yPos <= mouseY <= char.yPos + char.height
                if char.isActive:
                    active_character = char
                    break

        # Update active_character's targetX and targetY on left click to center the character...
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Subtract half of the character's size to center it at the click location
            active_character.targetX, active_character.targetY = event.pos[0] - active_character.width // 2, event.pos[1] - active_character.height // 2

    # Update and draw characters...
    window.fill((0, 0, 0))
    for char in teammates:
        char.move(char.targetX, char.targetY)
        #char.updateStatus()
        char.draw(window)

    player.draw(window)
    # Handle key presses for WASD Movement
    keys = pygame.key.get_pressed()

    directions = []
    if keys[pygame.K_w]:
        directions.append('up')
    if keys[pygame.K_a]:
        directions.append('left')
    if keys[pygame.K_s]:
        directions.append('down')
    if keys[pygame.K_d]:
        directions.append('right')

    # Only call move_WASD if there are directions to process
    if directions:
        player.move(directions, screen_height, screen_width)

    # Exit game with ESC
    if keys[pygame.K_ESCAPE]:
        running = False

    # Render the name of the active character.
    name_surface = game_font.render(f'Active Character: {active_character.name}', True, (255, 255, 255))

    # Render the status of the active character. Adjust the vertical position to display it underneath the name.
    # The vertical adjustment is based on the height of the name_surface plus a small gap (e.g., 5 pixels).
    status_surface = game_font.render(f"{active_character.name}'s Status: {active_character.status}", True, (255, 255, 255))

    # Calculate the position for the name surface. Let's assume you start at (10, 10) for example.
    name_position = (10, 10)

    # Calculate the position for the status surface, starting underneath the name surface.
    # The vertical position is the y-position of the name plus the height of the name_surface plus a small gap.
    status_position = (10, name_position[1] + name_surface.get_height() + 5)

    # Draw (blit) the surfaces onto the screen at their respective positions.
    window.blit(name_surface, name_position)
    window.blit(status_surface, status_position)

    # Update the display
    pygame.display.update()

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()