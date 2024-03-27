import pygame
from Characters import Teammate, Player, Enemy
import csv
from Weapons import Weapon, Attachment

# Global Variables and Pygame/Window Init Stuff
########################################################################################################################

pygame.init()
pygame.display.set_caption("Game Window!")


clock = pygame.time.Clock()
infoObject = pygame.display.Info()
screen_height, screen_width = infoObject.current_w, infoObject.current_h

# Initialize font
font_size = 24
game_font = pygame.font.SysFont('Arial', font_size)

window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Game Loop Run Condition
running = True

# Load Weapons
########################################################################################################################
weapons_csv = "D:\\Python_Projects\\Game_Making\\MNB2_csvs\\Allied_Weapons.csv"
weapons = []
bayonet = Attachment('Bayonet', 0, 0, 0, 0, 0, 0, 0, 10, 0)

with open(weapons_csv, mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)

    # reader holds the keys to each row of the file, as dictionaries
    for row in reader:
        # Create a Weapon instance for each row in the CSV
        weapon = Weapon(name=row['Name'], accuracy=row['Accuracy'], range=row['Range'],
                        damage=row['Damage'], weight=row['Weight'], mag_size=row['Mag_Size'],
                        fire_rate=row['Fire_Rate'], reload_time=row['Reload_Time'],
                        cqc=row['CQC'], attachment=bayonet)
        weapons.append(weapon)  # Don't forget to append the weapon to your list

# Load Characters
########################################################################################################################
'''Later I need to allow ability for these to be called from a csv file given inputs the game engine calls. That way Im 
not loading every possible enemy, teammate, and player class at all times; just the ones being rendered'''

player = Player('Me', 200, 200, 50, 50, 10, 'standby', 100, 0.2, 15, weapons[1], 0, 'Sarge')

# Setup good_guys...
good_guys = [Teammate('Raymond', 'Red', 50, 50, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[0], 0, 'Medic', 1, True),
             Teammate('Gary', 'Green', 100, 100, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[1], 0, 'Gunner', 1, False),
             Teammate('Bert', 'Blue', 150, 150, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[2], 0, 'Engineer', 1, False)]

selected_teammate = good_guys[0]

bad_guys = [Enemy('Hanz', 'Yellow', 1900, 1000, 50, 50, 3, 'Moving', 100, 0.1, 15, weapons[1], 'Volkssturm')]

# Load Game Assets
########################################################################################################################


# Game Loop
########################################################################################################################
while running:
    pygame.time.delay(10)
    window.fill((0, 0, 0))
    # Handle mouse and keyboard directions
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            mouseX, mouseY = event.pos
            for char in good_guys:
                char.isActive = (char.x_pos <= mouseX <= char.x_pos + char.width and char.y_pos <= mouseY <= char.y_pos
                                 + char.height)
                if char.isActive:
                    selected_teammate = char
                    break
                '''need to figure out how to not be selecting a character at all times: 
                else:
                    active_character = None
                '''

        # Update active_character's new_x and new_y on left click to center the character...
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Subtract half of the character's size to center it at the click location
            selected_teammate.new_x, selected_teammate.new_y = event.pos[0] - selected_teammate.width // 2, event.pos[1] - selected_teammate.height // 2

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

    # Update and draw characters...
    for char in good_guys:
        if char == selected_teammate:
            char.isActive = True
        else:
            char.isActive = False
        char.update_status(good_guys, bad_guys, player)
        char.draw(window)
    for char in bad_guys:
        char.update_status(bad_guys, good_guys, player)
        char.draw(window)
        if char.x_pos < 0:
            player.lives -= 1

    player.draw(window)

    # Render various details to the screen for debugging purposes
    name_surface = game_font.render(f'Active Character: {selected_teammate.name}', True, (255, 255, 255))

    status_surface = game_font.render(f"{selected_teammate.name}'s Status: {selected_teammate.status}", True, (255, 255, 255))

    weapon_surface = game_font.render(f"{selected_teammate.name}'s Current Weapon: {selected_teammate.weapon.name}", True,
                                      (255, 255, 255))

    name_position = (10, 10)
    status_position = (10, name_position[1] + name_surface.get_height() + 5)
    weapon_position = (10, status_position[1] + status_surface.get_height() + 5)

    window.blit(name_surface, name_position)
    window.blit(status_surface, status_position)
    window.blit(weapon_surface, weapon_position)

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
