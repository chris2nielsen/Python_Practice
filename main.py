# main.py
import pygame
from Characters import Character  # Assuming the filename is Character.py

# Initialize Pygame and setup window...
pygame.init()
clock = pygame.time.Clock()
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Game Window!")

# Initialize font
font_size = 24
game_font = pygame.font.SysFont('Arial', font_size)



# Setup characters...
characters = [Character('Raymond', 50, 50, 50, 50, (255, 0, 0), 5, True),
              Character('Garry', 100, 100, 50, 50, (0, 255, 0), 5, False),
              Character('Bert', 150, 150, 50, 50, (0, 0, 255), 5, False)]
active_character = characters[0]

running = True
# Game loop...
while running:
    pygame.time.delay(10)
    # Handle events including mouse and keyboard input...
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            mouseX, mouseY = event.pos
            for char in characters:
                char.isActive = char.x <= mouseX <= char.x + char.width and char.y <= mouseY <= char.y + char.height
                if char.isActive:
                    active_character = char
                    break

        # Update active_character's targetX and targetY on left click...
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            active_character.targetX, active_character.targetY = event.pos

    # Update and draw characters...
    window.fill((0, 0, 0))
    for char in characters:
        char.move_towards_target()
        char.draw(window)

    # Handle keypresses for WASD Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        active_character.targetY = active_character.y
        active_character.targetX = active_character.x
        active_character.move_WASD('up')
    if keys[pygame.K_a]:
        active_character.targetY = active_character.y
        active_character.targetX = active_character.x
        active_character.move_WASD('left')
    if keys[pygame.K_s]:
        active_character.targetY = active_character.y
        active_character.targetX = active_character.x
        active_character.move_WASD('down')
    if keys[pygame.K_d]:
        active_character.move_WASD('right')
    # Exit game with ESC
    if keys[pygame.K_ESCAPE]:
        running = False

    # Render the text
    text_surface = game_font.render(f'Active Character: {active_character.name}', True, (255, 255, 255))

    # Calculate text position (upper right corner)
    text_x = screen_width - text_surface.get_width() - 10  # 10 pixels from the right edge
    text_y = 10  # 10 pixels from the top

    # Blit the text onto the window surface
    window.blit(text_surface, (text_x, text_y))

    # Update the display
    pygame.display.update()

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()