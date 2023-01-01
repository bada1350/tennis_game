import pygame as pg
import random
import time

WIDTH = 800
HEIGHT = 600
RACKET_HEIGHT = 100
RACKET_WIDTH = 10
COM_SPEED = 7.0
ball_x = WIDTH / 2  # 75
ball_y = HEIGHT / 2 # 75
ball_r = 10     # 공 반지름
ball_speed_x = random.randint(-8, 8)    # 공의 x좌표가 이동할 때 속도 설정. 너무 느리거나 0이 되지 않도록 함
if ball_speed_x >= -4 and ball_speed_x <= 4:
    ball_speed_x = -5
ball_speed_y = random.randint(-8, 8)     # 공의 y좌표가 이동할 때 속도 설정. 0이 되지 않도록 함
if ball_speed_y == 0:
    ball_speed_y = 1
user_score = 0
com_score = 0
com_y = 250
mouse_pos = (0, 0)

def draw_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    pg.draw.circle(GAME_SCREEN, (255, 255, 255), (ball_x, ball_y), ball_r)
    ball_x += ball_speed_x
    ball_y += ball_speed_y

def draw_user_racket():
    if pos[1] <= 500:
        pg.draw.rect(GAME_SCREEN, (255, 255, 255), (0, pos[1], 10, 100))
    else:
        pg.draw.rect(GAME_SCREEN, (255, 255, 255), (0, 500, 10, 100))
    
def draw_com_racket():
    global com_y, COM_SPEED
    pg.draw.rect(GAME_SCREEN, (255, 255, 255), (790, com_y, 10, 300))
    com_y += COM_SPEED
    if com_y < 0 or com_y > 300:
        COM_SPEED *= -1
    
    if com_y > 0 and com_y < 300:
        if com_y + 50 < ball_y and COM_SPEED < 0 or com_y + 50 > ball_y and COM_SPEED > 0:
            COM_SPEED *= -1
    
def draw_net():
    for x in range(5):
        sy = 10 + 120 * x
        ey = 110 + 120 * x
        pg.draw.line(GAME_SCREEN, (255, 255, 255), (WIDTH / 2, sy), (WIDTH / 2, ey), 3)
        
def draw_score():
    user = FONT_40.render("P1:" + str(user_score), True, (255, 255, 255))
    com = FONT_40.render("COM:" + str(com_score), True, (255, 255, 255))
    GAME_SCREEN.blit(user, (10, 10))
    GAME_SCREEN.blit(com, (650, 10))

# 오브젝트의 이동을 연산하는 함수 - 공의 이동, 라켓의 이동, 충돌여부 계산
def calc_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, user_score, com_score
    if ball_x <= 10:
        ball_speed_x = 0
        com_score += 1
        ball_x = WIDTH / 2
        ball_y = HEIGHT / 2
        ball_speed_x = random.randint(-8, 8)
        if ball_speed_x >= -4 and ball_speed_x <= 4:
            ball_speed_x = -5
        ball_speed_y = random.randint(-4, 4)
        if ball_speed_y == 0:
            ball_speed_y = 1
    elif ball_x >= 790:
        ball_speed_x = 0
        user_score += 1
        ball_x = WIDTH / 2
        ball_y = HEIGHT / 2
        ball_speed_x = random.randint(-8, 8)
        if ball_speed_x >= -4 and ball_speed_x <= 4:
            ball_speed_x = -5
        ball_speed_y = random.randint(-4, 4)
        if ball_speed_y == 0:
            ball_speed_y = 1
    else:
        pass

    if ball_y < 20 or ball_y > 580:
        ball_speed_y *= -1
    else:
        pass

    if ball_x <= 20 and pos[1] - 10 < ball_y < pos[1] + 110:
        ball_speed_x *= -1
        if ball_speed_x > 0:
            ball_speed_x += random.randint(1, 3)
        else:
            ball_speed_x -= random.randint(1, 3)
        if ball_speed_y > 0:
            ball_speed_y += random.randint(1, 2)
        else:
            ball_speed_y -= random.randint(1, 2)
    
    if ball_x >= WIDTH - 20 and com_y - 10 < ball_y < com_y + 310:
        ball_speed_x *= -1
        if ball_speed_x > 0:
            ball_speed_x += random.randint(1, 3)
        else:
            ball_speed_x -= random.randint(1, 3)
        if ball_speed_y > 0:
            ball_speed_y += random.randint(1, 2)
        else:
            ball_speed_y -= random.randint(1, 2)

pg.init()
pg.display.set_caption("테니스 게임")
pg.key.set_repeat(1, 5)
GAME_SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
FONT_40 = pg.font.Font("nanum-gothic/NanumGothic.ttf", 40)

GAME_RUNNING = True
pos = (0, 0)
while GAME_RUNNING:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            GAME_RUNNING = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                GAME_RUNNING = False
            else:
                pass
        else:
            pass
    
    # 배경 그리기
    GAME_SCREEN.fill((0, 0, 0))
    draw_net()

    # 오브젝트 계산 및 그리기
    pos = pg.mouse.get_pos()
    msg = str(pos[0]) + "," + str(pos[1])
    msg_img = FONT_40.render(msg, True, (255, 0, 0))
    GAME_SCREEN.blit(msg_img, pos)

    draw_user_racket()
    draw_com_racket()
    draw_ball()
    draw_score()

    calc_ball()
    
    # 화면 업데이트 및 업데이트 간격 설정
    pg.display.update()
    time.sleep(0.03)
pg.quit()