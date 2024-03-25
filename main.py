import pygame
from Characters import Character, Teammate, Player  # Assuming the filename is Character.py
import csv
from Weapons import Weapon, Attachment

# Path to your sacred scroll
weapons_csv = "D:\\Python_Projects\\Game_Making\\MNB2_csvs\\Allied_Weapons.csv"
weapons = []
bayonet = Attachment('Bayonet', 0, 0, 0, 0, 0, 0, 0, 10, 0)

with open(weapons_csv, mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    print("Headers:", reader.fieldnames)  # This will show you the exact headers

    # Now reader holds the keys to each row of your file, as dictionaries
    for row in reader:
        # Create a Weapon instance for each row in the CSV
        weapon = Weapon(name=row['Name'], accuracy=row['Accuracy'], range=row['Range'],
                        damage=row['Damage'], weight=row['Weight'], magSize=row['Mag_Size'],
                        fireRate=row['Fire_Rate'], reloadTime=row['Reload_Time'],
                        CQC=row['CQC'], attachment=bayonet)
        weapons.append(weapon)  # Don't forget to append the weapon to your list

# Display your weapons
for weapon in weapons:
    print(weapon)

pygame.init()
clock = pygame.time.Clock()
infoObject = pygame.display.Info()
screen_height, screen_width = infoObject.current_w, infoObject.current_h
window = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Game Window!")

# Initialize font
font_size = 24
game_font = pygame.font.SysFont('Arial', font_size)

player = Player('Me', 200, 200, 50, 50, 10, 'standby', 100, 0.2, 15, weapons[1], 0, 'Sarge')

# Setup teammates...
teammates = [Teammate('Raymond', 'Red', 50, 50, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[0], 0, 'Medic', 1, True),
              Teammate('Gary', 'Green', 100, 100, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[1], 0, 'Gunner', 1, False),
              Teammate('Bert', 'Blue', 150, 150, 50, 50, 1, 'standby', 100, 0.2, 15, weapons[2], 0, 'Engineer', 1, False)]

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
        if char.xPos != char.targetX or char.yPos != char.targetY:
            char.status = 'Moving'
        if char.xPos == char.targetX and char.yPos == char.targetY:
            char.status = 'Standby'
        """how to handle pinned status?
            char.status = 'Pinned'
        how to handle aim/fire status?
            char.status = 'Aiming'
        how to prio status? moving/ability -> reloading/aiming/shooting -> pinned -> dead?
        prio queue fs
        """
        if char == active_character:
            char.isActive = True
        else:
            char.isActive = False
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

    weapon_surface = game_font.render(f"{active_character.name}'s current weapon: {active_character.weapon.name}", True,
                                      (255, 255, 255))

    # Calculate the position for the name surface. Let's assume you start at (10, 10) for example.
    name_position = (10, 10)

    # Calculate the position for the status surface, starting underneath the name surface.
    # The vertical position is the y-position of the name plus the height of the name_surface plus a small gap.
    status_position = (10, name_position[1] + name_surface.get_height() + 5)

    weapon_position = (10, status_position[1] + status_surface.get_height() + 5)

    # Draw (blit) the surfaces onto the screen at their respective positions.
    window.blit(name_surface, name_position)
    window.blit(status_surface, status_position)
    window.blit(weapon_surface, weapon_position)

    # Update the display
    pygame.display.update()

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()
