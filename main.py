import sys
import pygame
from grid import Grid
from colors import Color
from tetramino import Figures
from game_panel import Panel
from buttons import Button
from record import Record


def main_menu():
    """Вывод главного меню"""
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("PyTetris")
    pygame.mixer.music.load("sounds/bg_music.mp3")
    bg_main_menu = pygame.image.load('images/bg.png')
    screen.blit(bg_main_menu, (0, 0))
    font = pygame.font.SysFont('arial', 60)
    menu_text = font.render("MAIN MENU", True, Color().white)
    rect_menu = menu_text.get_rect(center=(350, 110))
    btn_play = Button(350, 300, "PLAY", font, Color().green, Color().orange)
    btn_quit = Button(350, 450, "QUIT", font, Color().green, Color().orange)
    screen.blit(menu_text, rect_menu)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for button in [btn_play, btn_quit]:
            button.change_color(mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_play.check_for_input(mouse_pos):
                    run(screen)
                if btn_quit.check_for_input(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def pause(screen):
    """Вывод меню паузы игрового процесса"""
    paused = True
    font_message = pygame.font.SysFont("comicsans", 30)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        screen.fill(Color().black)
        message1 = font_message.render("PAUSED", True, Color().white)
        rect_m1 = message1.get_rect(center=(350, 110))
        screen.blit(message1, rect_m1)
        message2 = font_message.render("Press C to continue or Q to quit.", True, Color().white)
        rect_m2 = message2.get_rect(center=(350, 450))
        screen.blit(message2, rect_m2)
        pygame.display.update()


def game_over(screen):
    """Вывод меню окончания игры"""
    running = False
    font_message = pygame.font.SysFont("comicsans", 30)

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = True
                    run(screen)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        screen.fill(Color().black)
        message1 = font_message.render("GAME OVER", True, Color().red)
        rect_m1 = message1.get_rect(center=(350, 110))
        screen.blit(message1, rect_m1)
        message2 = font_message.render("Press R to restart or Q to quit.", True, Color().white)
        rect_m2 = message2.get_rect(center=(350, 450))
        screen.blit(message2, rect_m2)
        pygame.display.update()


def run(screen):
    """Игровой цикл"""
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    fps = 20
    event_fall = 1
    speed = 10
    bg_surf = pygame.image.load("images/bg.png").convert()
    width = 400
    height = 800
    record = Record()
    grid = Grid(width, height)
    panel = Panel()
    bg_color = Color().black
    figures = Figures(width, height)
    figures.add()
    pygame.time.set_timer(event_fall, 150)
    running = True

    while running:
        pygame.mixer.music.unpause()
        clock.tick(fps)
        screen.fill(bg_color)
        screen.blit(bg_surf, (400, 0))
        figures.draw(screen)
        grid.draw(screen)
        panel.draw(screen, figures.tetramino[figures.next_tetra], figures.score, record.record)
        if figures.score > 5000:
            speed = 40
        elif figures.score > 1000:
            speed = 20
        figures.fall(speed)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                figures.rotation()
            elif event.type == event_fall:
                key = pygame.key.get_pressed()
                figures.move(key)
                record.check_record(figures.score)
                if figures.check_top():
                    pygame.mixer.music.pause()
                    game_over(screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.pause()
                    pause(screen)


main_menu()
