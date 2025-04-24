import pygame
import sys
from board import Board

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Sudoku Game")
font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()

game_state = "start"  # "start", "playing", "win", "lose"
difficulty = None
board = None

def draw_start_screen():
    screen.fill((255, 255, 255))
    title = font.render("Sudoku", True, (0, 0, 0))
    screen.blit(title, (240, 80))

    easy = pygame.Rect(200, 200, 200, 50)
    medium = pygame.Rect(200, 280, 200, 50)
    hard = pygame.Rect(200, 360, 200, 50)

    pygame.draw.rect(screen, (200, 200, 200), easy)
    pygame.draw.rect(screen, (200, 200, 200), medium)
    pygame.draw.rect(screen, (200, 200, 200), hard)

    screen.blit(font.render("Easy", True, (0, 0, 0)), (270, 210))
    screen.blit(font.render("Medium", True, (0, 0, 0)), (255, 290))
    screen.blit(font.render("Hard", True, (0, 0, 0)), (270, 370))

    return easy, medium, hard

def draw_end_screen(win):
    screen.fill((255, 255, 255))
    msg = "You Win!" if win else "Game Over"
    text = font.render(msg, True, (0, 0, 0))
    screen.blit(text, (230, 200))

def draw_buttons():
    reset_btn = pygame.Rect(50, 610, 140, 50)
    restart_btn = pygame.Rect(230, 610, 140, 50)
    exit_btn = pygame.Rect(410, 610, 140, 50)

    pygame.draw.rect(screen, (220, 220, 220), reset_btn)
    pygame.draw.rect(screen, (220, 220, 220), restart_btn)
    pygame.draw.rect(screen, (220, 220, 220), exit_btn)

    screen.blit(font.render("Reset", True, (0, 0, 0)), (90, 625))
    screen.blit(font.render("Restart", True, (0, 0, 0)), (255, 625))
    screen.blit(font.render("Exit", True, (0, 0, 0)), (455, 625))

    return reset_btn, restart_btn, exit_btn

running = True
while running:
    screen.fill((255, 255, 255))

    if game_state == "start":
        easy_btn, med_btn, hard_btn = draw_start_screen()

    elif game_state == "playing":
        board.draw()
        reset_btn, restart_btn, exit_btn = draw_buttons()

    elif game_state in ["win", "lose"]:
        draw_end_screen(game_state == "win")

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if game_state == "start":
                if easy_btn.collidepoint(pos):
                    difficulty = "easy"
                elif med_btn.collidepoint(pos):
                    difficulty = "medium"
                elif hard_btn.collidepoint(pos):
                    difficulty = "hard"
                if difficulty:
                    board = Board(540, 540, screen, difficulty)
                    game_state = "playing"

            elif game_state == "playing":
                if reset_btn.collidepoint(pos):
                    board.reset_to_original()
                elif restart_btn.collidepoint(pos):
                    game_state = "start"
                    difficulty = None
                elif exit_btn.collidepoint(pos):
                    running = False
                else:
                    grid_pos = board.click(*pos)
                    if grid_pos:
                        board.select(*grid_pos)

            elif game_state in ["win", "lose"]:
                game_state = "start"
                difficulty = None

        if event.type == pygame.KEYDOWN and game_state == "playing":
            if board.selected_cell:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    board.sketch(event.key - pygame.K_0)
                elif event.key == pygame.K_RETURN:
                    val = board.selected_cell.sketched_value
                    board.place_number(val)

                    if board.is_full():
                        if board.check_board():
                            game_state = "win"
                        else:
                            game_state = "lose"
                elif event.key == pygame.K_BACKSPACE:
                    board.clear()

    clock.tick(60)

pygame.quit()
sys.exit()
