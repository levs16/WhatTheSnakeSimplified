import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Colorful Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Snake
snake_size = 10
snake_speed = 15
snake = [(width / 2, height / 2)]
snake_direction = (1, 0)

# Food
food_size = 10
food = (random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10)

# Background
bg_color = blue

# Game states
STATE_START = 0
STATE_PLAYING = 1
STATE_PAUSE = 2
STATE_LOSE = 3
game_state = STATE_START

# Fonts
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_START or game_state == STATE_LOSE:
                if event.key == pygame.K_SPACE:
                    game_state = STATE_PLAYING
                    snake = [(width / 2, height / 2)]
                    snake_direction = (1, 0)
            elif game_state == STATE_PLAYING:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)
                elif event.key == pygame.K_p:
                    game_state = STATE_PAUSE
            elif game_state == STATE_PAUSE:
                if event.key == pygame.K_p:
                    game_state = STATE_PLAYING

    # Handle game states
    if game_state == STATE_START:
        window.fill(black)
        start_text = font.render("Press SPACE to start", True, white)
        window.blit(start_text, (width // 4, height // 2))
    elif game_state == STATE_PLAYING:
        # Move the snake
        snake_head = (snake[0][0] + snake_direction[0] * snake_size, snake[0][1] + snake_direction[1] * snake_size)
        snake.insert(0, snake_head)

        # Check for collisions
        if snake_head == food:
            food = (random.randrange(1, width // 10) * 10, random.randrange(1, height // 10) * 10)
        else:
            snake.pop()

        # Check if snake hits the wall
        if snake_head[0] < 0 or snake_head[0] >= width or snake_head[1] < 0 or snake_head[1] >= height:
            game_state = STATE_LOSE
        # Check if snake collides with itself
        elif len(snake) > 1 and snake_head in snake[1:]:
            game_state = STATE_LOSE

        # Draw background
        window.fill(bg_color)

        # Draw snake
        for segment in snake:
            pygame.draw.rect(window, green, (segment[0], segment[1], snake_size, snake_size))

        # Draw food
        pygame.draw.rect(window, red, (food[0], food[1], food_size, food_size))

    elif game_state == STATE_PAUSE:
        pause_text = font.render("PAUSED - Press P to resume", True, white)
        window.blit(pause_text, (width // 4, height // 2))
    elif game_state == STATE_LOSE:
        lose_text = font.render("You lost! Press SPACE to play again", True, white)
        window.blit(lose_text, (width // 5, height // 2))

    pygame.display.flip()

    # Control the snake's speed
    pygame.time.Clock().tick(snake_speed)
