import pygame
import numpy as np
import random
import models
from environment.maze import Maze

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 7, 7  # Maze size
CELL_SIZE = 40  # Size of each cell in pixels
SCREEN_WIDTH = WIDTH * CELL_SIZE * 3.5  
SCREEN_HEIGHT = (HEIGHT * CELL_SIZE) + 60 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

# Directions for movement (right, down, left, up)
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Function to generate a maze
def generate_maze(width, height):
    maze = np.ones((height, width), dtype=int)
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]
    
    while stack:
        x, y = stack[-1]
        neighbors = []
        
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny - (ny - y)//2][nx - (nx - x)//2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    
    # Ensure start and end are open
    maze[0][0] = 0
    maze[height-1][width-1] = 0
    
    return maze, (width - 1, height - 1)

# Function to draw the maze
def draw_maze(screen, maze, offset_x=0, offset_y=0):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y, x] == 1:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Function to draw the barriers
def draw_barriers(screen, player_maze_offset_x, ai_maze_offset_x, maze_offset_y):
    # Draw the white barrier on the right edge of the player maze
    pygame.draw.rect(screen, WHITE, pygame.Rect(player_maze_offset_x + 1, maze_offset_y, 10, HEIGHT * CELL_SIZE))
    
    # Draw the white barrier on the left edge of the AI maze
    pygame.draw.rect(screen, WHITE, pygame.Rect(ai_maze_offset_x - 10, maze_offset_y, 10, HEIGHT * CELL_SIZE))
    
    # Draw the white barrier on the top edge of the player maze
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, maze_offset_y - 10, player_maze_offset_x + 11, 10))
    
    # Draw the white barrier on the top edge of the AI maze
    pygame.draw.rect(screen, WHITE, pygame.Rect(ai_maze_offset_x - 10, maze_offset_y - 10, SCREEN_WIDTH - ai_maze_offset_x + 10, 10))

# Function to move the player or AI
def move(position, direction, maze):
    x, y = position
    if direction == 0 and x > 0 and maze[y][x - 1] == 0:  # Move left
        x -= 1
    elif direction == 1 and x < WIDTH - 1 and maze[y][x + 1] == 0:  # Move right
        x += 1
    elif direction == 2 and y > 0 and maze[y - 1][x] == 0:  # Move up
        y -= 1
    elif direction == 3 and y < HEIGHT - 1 and maze[y + 1][x] == 0:  # Move down
        y += 1
    return x, y

# Function to display text on the screen
def display_text(screen, text, size, color, pos):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Function to show the main menu
def main_menu():
    screen.fill(BLACK)  
    title_font_size = 72
    menu_font_size = 36

    # Position for the title
    title_text = "MAZE GAME"
    title_font = pygame.font.Font(None, title_font_size)
    title_surface = title_font.render(title_text, True, WHITE)
    title_x = (SCREEN_WIDTH - title_surface.get_width()) // 2
    title_y = (SCREEN_HEIGHT // 4) - (title_surface.get_height() // 2)
    screen.blit(title_surface, (title_x, title_y))

    # Position for the "Press 1 for VS MODE" text
    vs_mode_text = "Press 1 for VS MODE"
    menu_font = pygame.font.Font(None, menu_font_size)
    vs_mode_surface = menu_font.render(vs_mode_text, True, WHITE)
    vs_mode_x = (SCREEN_WIDTH - vs_mode_surface.get_width()) // 2
    vs_mode_y = (SCREEN_HEIGHT // 2) - (vs_mode_surface.get_height() // 2)
    screen.blit(vs_mode_surface, (vs_mode_x, vs_mode_y))

    # Position for the "Press ESC to QUIT" text
    quit_text = "Press ESC to QUIT"
    quit_surface = menu_font.render(quit_text, True, WHITE)
    quit_x = (SCREEN_WIDTH - quit_surface.get_width()) // 2
    quit_y = (3 * SCREEN_HEIGHT // 4) - (quit_surface.get_height() // 2)
    screen.blit(quit_surface, (quit_x, quit_y))

    pygame.display.flip()  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return difficulty_menu()  # Go to the difficulty menu
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        pygame.time.wait(10)

# Function to show the difficulty menu
def difficulty_menu():
    screen.fill(BLACK)
    menu_font_size = 36

    # Position for the "Choose Difficulty" text
    difficulty_text = "Choose Difficulty"
    menu_font = pygame.font.Font(None, menu_font_size)
    difficulty_surface = menu_font.render(difficulty_text, True, WHITE)
    difficulty_x = (SCREEN_WIDTH - difficulty_surface.get_width()) // 2
    difficulty_y = (SCREEN_HEIGHT // 4) - (difficulty_surface.get_height() // 2)
    screen.blit(difficulty_surface, (difficulty_x, difficulty_y))

    # Position for the "Press 1 for Easy" text
    easy_text = "Press 1 for Easy"
    easy_surface = menu_font.render(easy_text, True, WHITE)
    easy_x = (SCREEN_WIDTH - easy_surface.get_width()) // 2
    easy_y = (SCREEN_HEIGHT // 2) - (easy_surface.get_height() // 2) - 40
    screen.blit(easy_surface, (easy_x, easy_y))

    # Position for the "Press 2 for Normal" text
    normal_text = "Press 2 for Normal"
    normal_surface = menu_font.render(normal_text, True, WHITE)
    normal_x = (SCREEN_WIDTH - normal_surface.get_width()) // 2
    normal_y = (SCREEN_HEIGHT // 2) - (normal_surface.get_height() // 2)
    screen.blit(normal_surface, (normal_x, normal_y))

    # Position for the "Press 3 for Hard" text
    hard_text = "Press 3 for Hard"
    hard_surface = menu_font.render(hard_text, True, WHITE)
    hard_x = (SCREEN_WIDTH - hard_surface.get_width()) // 2
    hard_y = (SCREEN_HEIGHT // 2) - (hard_surface.get_height() // 2) + 40
    screen.blit(hard_surface, (hard_x, hard_y))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 500  # Easy
                elif event.key == pygame.K_2:
                    return 300  # Normal
                elif event.key == pygame.K_3:
                    return 200  # Hard

        pygame.time.wait(10)

# Function to show the tutorial
def show_tutorial():
    screen.fill(BLACK)

    # Display tutorial text
    tutorial_texts = [
        "BLUE block : YOU",
        "YELLOW block : kadalgurun",
        "RED block : GOAL",
        "MOVE : Arrow Keys",
        "PAUSE : ESC",
        "",
        "Press ENTER to continue"
    ]

    tutorial_font_size = 27
    tutorial_font = pygame.font.Font(None, tutorial_font_size)

    for i, line in enumerate(tutorial_texts):
        tutorial_surface = tutorial_font.render(line, True, WHITE)
        tutorial_x = (SCREEN_WIDTH - tutorial_surface.get_width()) // 2
        tutorial_y = SCREEN_HEIGHT // 6 + i * 40
        screen.blit(tutorial_surface, (tutorial_x, tutorial_y))

    pygame.display.flip()

    # Wait for the user to press ENTER
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Exit the tutorial

        pygame.time.wait(10)

# Function to show the pause menu
def pause_menu():
    screen.fill(BLACK)

    # PAUSED text
    paused_text = "PAUSED"
    paused_font = pygame.font.Font(None, 72)
    paused_surface = paused_font.render(paused_text, True, WHITE)
    paused_rect = paused_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(paused_surface, paused_rect)

    # Press R to Resume text
    resume_text = "Press R to Resume"
    resume_font = pygame.font.Font(None, 36)
    resume_surface = resume_font.render(resume_text, True, WHITE)
    resume_rect = resume_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    screen.blit(resume_surface, resume_rect)

    # Press ESC to Quit to Main Menu text
    quit_text = "Press ESC to Quit to Main Menu"
    quit_font = pygame.font.Font(None, 36)
    quit_surface = quit_font.render(quit_text, True, WHITE)
    quit_rect = quit_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(quit_surface, quit_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume
                    return "resume"
                elif event.key == pygame.K_ESCAPE:  # Quit to Main Menu
                    return "quit_to_menu"

# Main game loop
def game_loop(ai_move_time):
    running = True
    ai_last_move = pygame.time.get_ticks()  # Initialize the last move time
    player_wins = 0  # Initialize player win counter
    ai_wins = 0  # Initialize AI win counter

    while running:
        # Generate a new maze and reset positions
        maze, exit_position = generate_maze(WIDTH, HEIGHT)
        player_pos = [0, 0]  # Player start position
        ai_pos = [0, 0]  # AI start position

        # Initialize the AI model for the maze
        game = Maze(maze, exit_cell=exit_position)
        model = models.SarsaTableTraceModel(game)
        model.train(discount=0.90, exploration_rate=0.10, learning_rate=0.10, episodes=200, stop_at_convergence=True)
        
        level_running = True
        while level_running:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    level_running = False

                # Handle player movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_pos = move(player_pos, 0, maze)
                    elif event.key == pygame.K_RIGHT:
                        player_pos = move(player_pos, 1, maze)
                    elif event.key == pygame.K_UP:
                        player_pos = move(player_pos, 2, maze)
                    elif event.key == pygame.K_DOWN:
                        player_pos = move(player_pos, 3, maze)
                    elif event.key == pygame.K_ESCAPE:
                        action = pause_menu()
                        if action == "resume":
                            continue  # Resume game
                        elif action == "quit_to_menu":
                            level_running = False  # End level
                            running = False  # End game loop

            if not level_running:
                break

            # AI movement using the SARSA model with a timer delay
            current_time = pygame.time.get_ticks()
            if current_time - ai_last_move >= ai_move_time:
                ai_action = model.predict(np.array([ai_pos]))
                ai_pos = move(ai_pos, ai_action, maze)
                ai_last_move = current_time

            # Draw player and AI mazes at the bottom edge of the screen
            maze_offset_y = SCREEN_HEIGHT - HEIGHT * CELL_SIZE - 10  # Adjust the vertical offset to move the maze to the bottom
            draw_maze(screen, maze, 0, maze_offset_y)
            draw_maze(screen, maze, SCREEN_WIDTH - WIDTH * CELL_SIZE, maze_offset_y)
            draw_barriers(screen, WIDTH * CELL_SIZE, SCREEN_WIDTH - WIDTH * CELL_SIZE, maze_offset_y)

            # Draw the "VS" text in the middle of the screen
            vs_font_size = 120
            vs_font = pygame.font.Font(None, vs_font_size)
            vs_surface = vs_font.render("VS", True, WHITE)
            vs_x = (SCREEN_WIDTH // 2) - (vs_surface.get_width() // 2)
            vs_y = (SCREEN_HEIGHT // 2) - (vs_surface.get_height() // 2)
            screen.blit(vs_surface, (vs_x, vs_y))

            # Draw the player and AI positions
            pygame.draw.rect(screen, BLUE, pygame.Rect(player_pos[0] * CELL_SIZE, maze_offset_y + player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, YELLOW, pygame.Rect(SCREEN_WIDTH - WIDTH * CELL_SIZE + ai_pos[0] * CELL_SIZE, maze_offset_y + ai_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw the exit
            pygame.draw.rect(screen, RED, pygame.Rect(exit_position[0] * CELL_SIZE, maze_offset_y + exit_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, pygame.Rect(SCREEN_WIDTH - WIDTH * CELL_SIZE + exit_position[0] * CELL_SIZE, maze_offset_y + exit_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Check for win conditions
            if tuple(player_pos) == exit_position:
                player_wins += 1  # Increment player win counter
                display_text(screen, "YOU WIN!", 72, BLUE, (vs_x - 60, vs_y - 50))
                level_running = False
            elif tuple(ai_pos) == exit_position:
                ai_wins += 1  # Increment AI win counter
                display_text(screen, "YOU LOST!", 72, YELLOW, (vs_x - 60, vs_y - 50))
                level_running = False

            # Display the counters
            display_text(screen, f"Player : {player_wins}", 36, WHITE, (50, 10))
            display_text(screen, f"kadalgurun : {ai_wins}", 36, WHITE, (SCREEN_WIDTH - 200, 10))

            pygame.display.flip()

    return False if not running else True


if __name__ == "__main__":
    while True:
        main_menu()  # Show the main menu
        ai_move_time = difficulty_menu()  # Get the selected difficulty
        show_tutorial()  # Show the tutorial before the game starts
        game_active = game_loop(ai_move_time)  # Start the game loop with the chosen difficulty
        
        # If game_active is False, return to main menu
        if not game_active:
            continue  # This will loop back to the main menu
        else:
            break  # If for any reason the game should quit, exit the loop
