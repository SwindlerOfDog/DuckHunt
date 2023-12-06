import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Setting game window dimensions
window_width = 1280
window_height = 720
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Duck Game')  # Set the window title

# Loading the background image
bg_image = pygame.image.load('Assets/DHBG.jpg')
# Scaling the background image to fit the game window
bg_image = pygame.transform.scale(bg_image, (window_width, window_height))

# Loading the duck image
duck_image = pygame.image.load("Assets/DHD.png")
duck_image = pygame.transform.scale(duck_image, (50, 50))

# Set the initial speed of the duck
duck_speed = 5

def spawn_new_duck():
    # Function to spawn a new duck
    if random.choice([True, False]):  # True for left, False for right
        duck_x = -50
        duck_angle = random.uniform(0.25 * math.pi, 0.75 * math.pi)  # Angle towards the right
    else:
        duck_x = window_width
        duck_angle = random.uniform(1.25 * math.pi, 1.75 * math.pi)  # Angle towards the left

    duck_y = random.uniform(50, window_height - 50)  # Random y position within the screen boundaries
    duck_timer = pygame.time.get_ticks()  # Set the timer when the duck is spawned

    return duck_x, duck_y, duck_angle, duck_timer  # Added a timer for the duck

# Set the initial position of the duck randomly on the left or right side
duck_x, duck_y, duck_angle, duck_timer = spawn_new_duck()

# Set the time at the start
start_time = pygame.time.get_ticks()

# Set the game timer to 60 seconds
game_timer = 60000  # 60 seconds in milliseconds

# Set the initial score
score = 0

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 is the left mouse button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the mouse click is within the duck's bounding box
            if duck_x <= mouse_x <= duck_x + 50 and duck_y <= mouse_y <= duck_y + 50:
                # Add 100 points if clicked on the duck
                score += 100
                # Respawn a new duck
                duck_x, duck_y, duck_angle, duck_timer = spawn_new_duck()
            else:
                # Subtract 50 points if not clicked on the duck
                score = max(0, score - 50)

    # Clear the screen
    game_display.blit(bg_image, (0, 0))

    # Calculate the elapsed time since the duck was spawned
    elapsed_duck_time = pygame.time.get_ticks() - duck_timer
    elapsed_game_time = pygame.time.get_ticks() - start_time

    # Update the duck's position based on the angle
    duck_x += duck_speed * math.cos(duck_angle)
    duck_y += duck_speed * math.sin(duck_angle)

    # If the duck hits the top or bottom, reflect the angle
    if duck_y < 50 or duck_y > window_height - 50:
        duck_angle = 2 * math.pi - duck_angle  # Reflect the angle

    # If the duck goes off the screen or 10 seconds have passed, reset its position and angle
    if duck_x < -50 or duck_x > window_width + 50 or elapsed_duck_time > 10000:
        duck_x, duck_y, duck_angle, duck_timer = spawn_new_duck()

    # Keep the duck within the top and bottom boundaries
    duck_y = max(50, min(window_height - 50, duck_y))

    # Determine whether the duck is moving to the left or right
    facing_left = duck_speed * math.cos(duck_angle) < 0

    # Flip the duck image horizontally if moving to the left
    if facing_left:
        duck_image_flipped = pygame.transform.flip(duck_image, True, False)
        game_display.blit(duck_image_flipped, (duck_x, duck_y))
    else:
        game_display.blit(duck_image, (duck_x, duck_y))

    # Display the visual timer in the top left corner for the duck
    duck_timer_text = font.render(f"Duck Timer: {int((10000 - elapsed_duck_time) / 1000)}s", True, (255, 255, 255))
    game_display.blit(duck_timer_text, (10, 10))

    # Display the visual timer in the top right corner for the game
    game_timer_text = font.render(f"Game Timer: {int((game_timer - elapsed_game_time) / 1000)}s", True, (255, 255, 255))
    game_display.blit(game_timer_text, (window_width - 200, 10))

    # Display the score in the bottom left corner
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    game_display.blit(score_text, (10, window_height - 40))

    # Check if the game timer has reached 0
    if elapsed_game_time >= game_timer:
        # Pause the game and print the score
        game_display.blit(font.render(f"Time!!! Your Score is: {score}", True, (255, 0, 0)), (window_width // 2 - 200, window_height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        pygame.quit()
        sys.exit()

    # Update the display
    pygame.display.flip()

    # Add a small delay to control the frame rate
    clock.tick(60)