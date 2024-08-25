import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FONT_SIZE = 30
CONTROL_FONT_SIZE = 20  # Smaller font for controls
WINNING_SCORE = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
CPU_SPEED = 6  # Increased speed for smarter CPU

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong Game')

# Initialize fonts
font = pygame.font.Font(None, FONT_SIZE)
control_font = pygame.font.Font(None, CONTROL_FONT_SIZE)

# Load sounds
hit_sound = pygame.mixer.Sound('hit_sound.wav')
score_sound = pygame.mixer.Sound('score_sound.wav')
win_sound = pygame.mixer.Sound('win_sound.wav')
selection_sound = pygame.mixer.Sound('selection_sound.wav')
start_sound = pygame.mixer.Sound('start_sound.wav')
quit_sound = pygame.mixer.Sound('quit_sound.wav')
restart_sound = pygame.mixer.Sound('restart_sound.wav')
pause_sound = pygame.mixer.Sound('pause_sound.wav')

# Load and play background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Loop background music

# Global variables
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y
player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
score1 = 0
score2 = 0
paused = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_objects(mode, player1_y, player2_y, ball_x, ball_y, score1, score2, paused):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (30, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    if mode == '1 Player':
        pygame.draw.rect(screen, BLACK, (WIDTH - 30 - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    else:
        pygame.draw.rect(screen, BLACK, (WIDTH - 30 - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    pygame.draw.ellipse(screen, BLACK, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    draw_text(f'{score1} - {score2}', font, BLACK, screen, WIDTH // 2, 20)
    
    # Draw game controls at the bottom
    if paused:
        draw_text('PAUSED - Press SPACE to Resume', control_font, BLACK, screen, WIDTH // 2, HEIGHT - 30)
    draw_text('Press R to Restart', control_font, BLACK, screen, WIDTH // 2, HEIGHT - 70)
    draw_text('Press Q to Quit', control_font, BLACK, screen, WIDTH // 2, HEIGHT - 100)
    draw_text('Press SPACE to Pause', control_font, BLACK, screen, WIDTH // 2, HEIGHT - 130)
    
    pygame.display.flip()

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global player1_y, player2_y
    global score1, score2

    ball_x = WIDTH // 2 - BALL_SIZE // 2
    ball_y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed_x = BALL_SPEED_X
    ball_speed_y = BALL_SPEED_Y
    player1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    score1 = 0
    score2 = 0

def selection_screen():
    while True:
        screen.fill(WHITE)
        draw_text('SELECTION: 1 Player OR 2 Players', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('1 Player', font, BLACK, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('2 Players', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text('Quit', font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sound.play()
                pygame.time.wait(500)  # Wait for sound to play
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selection_sound.play()
                    pygame.time.wait(500)  # Wait for sound to play
                    return '1 Player'
                if event.key == pygame.K_2:
                    selection_sound.play()
                    pygame.time.wait(500)  # Wait for sound to play
                    return '2 Players'
                if event.key == pygame.K_q:
                    quit_sound.play()
                    pygame.time.wait(500)  # Wait for sound to play
                    pygame.quit()
                    sys.exit()

def game_loop(mode):
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global player1_y, player2_y
    global score1, score2
    global paused

    reset_game()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_sound.play()
                pygame.time.wait(500)  # Wait for sound to play
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_sound.play()
                    pygame.time.wait(500)  # Wait for sound to play
                    reset_game()
                if event.key == pygame.K_q:
                    quit_sound.play()
                    pygame.time.wait(500)  # Wait for sound to play
                    return selection_screen()
                if event.key == pygame.K_SPACE:
                    if not paused:
                        pause_sound.play()
                        pygame.time.wait(500)  # Wait for sound to play
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player1_y > 0:
                player1_y -= PADDLE_SPEED
            if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
                player1_y += PADDLE_SPEED
            
            if mode == '2 Players':
                if keys[pygame.K_UP] and player2_y > 0:
                    player2_y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
                    player2_y += PADDLE_SPEED
            else:
                # Smarter CPU movement
                if ball_speed_x > 0:  # CPU is expected to intercept the ball
                    if ball_y < player2_y + PADDLE_HEIGHT / 2:
                        player2_y -= CPU_SPEED
                    if ball_y > player2_y + PADDLE_HEIGHT / 2:
                        player2_y += CPU_SPEED
                    player2_y = max(min(player2_y, HEIGHT - PADDLE_HEIGHT), 0)

            ball_x += ball_speed_x
            ball_y += ball_speed_y
            
            if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
                ball_speed_y = -ball_speed_y

            if (ball_x <= 30 + PADDLE_WIDTH and player1_y < ball_y + BALL_SIZE and player1_y + PADDLE_HEIGHT > ball_y):
                ball_speed_x = -ball_speed_x
                hit_sound.play()
            if (ball_x >= WIDTH - 30 - BALL_SIZE and player2_y < ball_y + BALL_SIZE and player2_y + PADDLE_HEIGHT > ball_y):
                ball_speed_x = -ball_speed_x
                hit_sound.play()

            if ball_x < 0:
                score2 += 1
                score_sound.play()
                if score2 >= WINNING_SCORE:
                    win_sound.play()
                    pygame.time.wait(1000)
                    reset_game()
                else:
                    ball_x = WIDTH // 2 - BALL_SIZE // 2
                    ball_y = HEIGHT // 2 - BALL_SIZE // 2
                    ball_speed_x = -ball_speed_x
            if ball_x > WIDTH:
                score1 += 1
                score_sound.play()
                if score1 >= WINNING_SCORE:
                    win_sound.play()
                    pygame.time.wait(1000)
                    reset_game()
                else:
                    ball_x = WIDTH // 2 - BALL_SIZE // 2
                    ball_y = HEIGHT // 2 - BALL_SIZE // 2
                    ball_speed_x = -ball_speed_x

            draw_objects(mode, player1_y, player2_y, ball_x, ball_y, score1, score2, paused)
        else:
            draw_objects(mode, player1_y, player2_y, ball_x, ball_y, score1, score2, paused)

        clock.tick(FPS)

# Start the game
game_mode = selection_screen()
game_loop(game_mode)
