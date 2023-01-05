import pygame as pg
import random
import time

WIDTH = 800
HEIGHT = 600
USER_RACKET_HEIGHT = 100
COM_RACKET_HEIGHT = 300
RACKET_WIDTH = 10
COM_SPEED = 10

ball_x = WIDTH / 2  # 75
ball_y = HEIGHT / 2 # 75
ball_r = 10     # 공 반지름
ball_speed_x = random.choice([-8, -7, -6, -5, 5, 6, 7, 8])    # 공의 x좌표가 이동할 때 속도 설정
ball_speed_y = random.choice([-5, 5])     # 공의 y좌표가 이동할 때 속도 설정. 0이 되지 않도록 함
user_score = 0
com_score = 0
com_y = 250
mouse_pos = (0, 0)

# 공 그리기
def draw_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    pg.draw.circle(GAME_SCREEN, (255, 255, 255), (ball_x, ball_y), ball_r)
    ball_x += ball_speed_x
    ball_y += ball_speed_y

# 유저 라켓 그리기
def draw_user_racket():
    if pos[1] <= 500:
        pg.draw.rect(GAME_SCREEN, (255, 255, 255), (0, pos[1], RACKET_WIDTH, USER_RACKET_HEIGHT))
    else:
        pg.draw.rect(GAME_SCREEN, (255, 255, 255), (0, 500, RACKET_WIDTH, USER_RACKET_HEIGHT))

# 컴퓨터 라켓 그리기
def draw_com_racket():
    global com_y, COM_SPEED
    pg.draw.rect(GAME_SCREEN, (255, 255, 255), (790, com_y, RACKET_WIDTH, COM_RACKET_HEIGHT))
    com_y += COM_SPEED
    
    # 라켓이 화면을 벗어나지 않으면서 자동으로 공을 따라가도록 함 | (참고) com_y의 범위는 0~300
    if com_y + 100 < ball_y < com_y + COM_RACKET_HEIGHT - 100:
        COM_SPEED = 0
    elif ball_y < com_y + 100:
        if com_y <= 0:
            com_y = 0
            COM_SPEED = 0
        else:
            COM_SPEED = -10
    elif ball_y > com_y + COM_RACKET_HEIGHT - 100:
        if com_y >= 300:
            com_y = 300
            COM_SPEED = 0
        else:
            COM_SPEED = 10

# 네트 그리기
def draw_net():
    for x in range(5):
        sy = 10 + 120 * x
        ey = 110 + 120 * x
        pg.draw.line(GAME_SCREEN, (255, 255, 255), (WIDTH / 2, sy), (WIDTH / 2, ey), 3)

# 점수 그리기
def draw_score():
    user = FONT_40.render("USER:" + str(user_score), True, (255, 255, 255))
    com = FONT_40.render("COM:" + str(com_score), True, (255, 255, 255))
    GAME_SCREEN.blit(user, (10, 10))
    GAME_SCREEN.blit(com, (650, 10))

# 난이도 상을 위해 공이 라켓과 부딪힐 때마다 공을 가속
def ball_acceleration():
    global ball_speed_x, ball_speed_y
    if ball_speed_x > 0:
        ball_speed_x += 2
    else:
        ball_speed_x -= 2
    if ball_speed_y > 0:
        ball_speed_y += 2
    else:
        ball_speed_y -= 2

# 공을 새로 세팅
def ball_set():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2
    ball_speed_x = random.choice([-8, -7, -6, -5, 5, 6, 7, 8])
    ball_speed_y = random.choice([-5, 5])

# 공의 이동, 벽/라켓과의 충돌 계산
def calc_ball():
    global ball_speed_x, ball_speed_y, user_score, com_score
    if ball_y < ball_r * 2 or ball_y > HEIGHT - ball_r * 2:
        ball_speed_y *= -1
    else:
        pass
    
    if ball_x <= 2 * ball_r:
        if pos[1] - ball_r < ball_y < pos[1] + USER_RACKET_HEIGHT + ball_r or pos[1] > 500 and ball_y > 500:
            ball_speed_x = abs(ball_speed_x)
            ball_acceleration()
        else:
            if ball_x <= 0:
                com_score += 1
                ball_set()
    elif ball_x >= WIDTH - 2 * ball_r:
        if com_y - ball_r < ball_y < com_y + COM_RACKET_HEIGHT + ball_r:
            ball_speed_x = -1 * abs(ball_speed_x)
            ball_acceleration()
        else:
            if ball_x >= 800:
                user_score += 1
                ball_set()
    else:
        pass
        
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