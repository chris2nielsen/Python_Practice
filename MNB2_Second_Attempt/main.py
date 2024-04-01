import pygame
import time
from Character import Sarge, Target
from Bullets import Bullet

pygame.init()
pygame.display.set_caption("Game Window!")

clock = pygame.time.Clock()
infoObject = pygame.display.Info()
screen_height, screen_width = infoObject.current_w, infoObject.current_h

# Initialize font
font_size = 24
game_font = pygame.font.SysFont('Arial', font_size)

display = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

sprite_group = pygame.sprite.Group()

player = Sarge()
sprite_group.add(player)

target = Target()
sprite_group.add(target)

directions = []

running = True
while running:
    clock.tick(60)
    display.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Exit game with ESC
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_w:
                player.vel_y = -player.speed
            if event.key == pygame.K_a:
                player.vel_x = -player.speed
            if event.key == pygame.K_s:
                player.vel_y = player.speed
            if event.key == pygame.K_d:
                player.vel_x = player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.vel_y = 0
            if event.key == pygame.K_a:
                player.vel_x = 0
            if event.key == pygame.K_s:
                player.vel_y = 0
            if event.key == pygame.K_d:
                player.vel_x = 0
#heres a comment lol
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # On mouse click, append the click position to directions
            x, y = event.pos  # event.pos contains a tuple of (x, y)
            directions.append(x)
            directions.append(y)



    # Update Objects Attributes
    sprite_group.update(directions)


    directions.clear()

    # Render the Display
    sprite_group.draw(display)
    player.bullet_group.draw(display)

    # Update the display
    pygame.display.update()

pygame.quit()


