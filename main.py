import random
import pygame
import sys
from queue import Queue
from pygame.locals import *
import numpy

snake_speed = 15 #速度
windows_width = 800
windows_height = 800
cell_size = 20
map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)
LEFT = numpy.array([[0,1,0],[-1,0,0],[0,0,1]]) #左旋
RIGHT = numpy.array([[0,-1,0],[1,0,0],[0,0,1]]) #右旋
UP = numpy.array([[0,0,-1],[0,1,0],[1,0,0]]) #上旋
DOWN = numpy.array([[0,0,1],[0,1,0],[-1,0,0]]) #下旋

class Node:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        return
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getz(self):
        return self.z
    def setx(self,x):
        self.x = x
    def sety(self,y):
        self.y = y
    def setz(self,z):
        self.z = z

def random_location(): #随机生成地点
    return Node( random.randint(0, map_width - 1), random.randint(0, map_height - 1), random.randint(0, map_height - 1))

def terminate(): #退出
    pygame.quit()
    sys.exit()

def snake_move(direction, snake_coords):
    if (direction == numpy.array([0,1,0])).all():
        newHead = Node(snake_coords[0].getx(), snake_coords[0].gety() + 1, snake_coords[0].getz())
    elif (direction == numpy.array([0,-1,0])).all():
        newHead = Node(snake_coords[0].getx(), snake_coords[0].gety() - 1, snake_coords[0].getz())
    elif (direction == numpy.array([0,0,1])).all():
        newHead = Node(snake_coords[0].getx(), snake_coords[0].gety(), snake_coords[0].getz() + 1)
    elif (direction == numpy.array([0,0,-1])).all():
        newHead = Node(snake_coords[0].getx(), snake_coords[0].gety(), snake_coords[0].getz() - 1)
    elif (direction == numpy.array([1,0,0])).all():
        newHead = Node(snake_coords[0].getx() + 1, snake_coords[0].gety(), snake_coords[0].getz())
    elif (direction == numpy.array([-1,0,0])).all():
        newHead = Node(snake_coords[0].getx() - 1, snake_coords[0].gety(), snake_coords[0].getz())
    snake_coords.insert(0, newHead)


def snake_check(snake_coords):
    flag = True
    if snake_coords[0].getx() == -1 or snake_coords[0].getx() == map_width or snake_coords[0].gety() == -1 or \
			snake_coords[0].gety() == map_height:
        flag = False # 碰壁
    for snake_body in snake_coords[1:]:
        if snake_body.getx() == snake_coords[0].getx() and snake_body.gety() == snake_coords[0].gety():
            flag = False # 碰到自己
    return flag

def snake_food(snake_coords, food):
    if snake_coords[0].getx() == food.getx() and snake_coords[0].gety() == food.gety():
        food.setx(random.randint(0, map_width - 1))
        food.sety(random.randint(0, map_height - 1))
    else:
        del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉

def snake_draw(screen, snake_coords):
    for coord in snake_coords:
        x = coord.getx() * cell_size
        y = coord.gety() * cell_size
        wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, (10,20,30), wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
			x + 4, y + 4, cell_size - 8, cell_size - 8)
        pygame.draw.rect(screen, (33,66,99), wormInnerSegmentRect)


def food_draw(screen, food):
    x = food.getx() * cell_size
    y = food.gety() * cell_size
    appleRect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, (255,0,0), appleRect)


def score_draw(screen,score):
    font = pygame.font.Font('myfont.ttf', 30)
    scoreSurf = font.render('得分: %s' % score, True, (0,255,0))
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windows_width - 120, 10)
    screen.blit(scoreSurf, scoreRect)

def show_gameover_info(screen):
    font = pygame.font.Font('myfont.ttf', 40)
    tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏~', True, (65, 105, 225))
    screen.blit(tip, (80, 300))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    terminate()
                else:
                    return


def game_body(screen,snake_speed_clock):
    startx = random.randint(3, map_width - 8) #开始位置
    starty = random.randint(3, map_height - 8)
    startz = random.randint(3, map_height - 8)
    snake_coords = [Node(startx,starty,startz),Node(startx-1,starty,startz),Node(startx-2,starty,startz)]
    a_origin = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # 绝对坐标的初始矩阵,设定为单位矩阵方便运算
    mat_change = a_origin #旋转矩阵初始化
    direction = numpy.array([0,1,0])      #  右1 里2 左3 外4 下5 上6
    food = random_location()     #实物随机位置
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                '''if (event.key == K_LEFT or event.key == K_a) and direction != 4:
                    direction = 3
                elif (event.key == K_RIGHT or event.key == K_d) and direction != 3:
                    direction = 4
                elif (event.key == K_UP or event.key == K_w) and direction != 2:
                    direction = 1
                elif (event.key == K_DOWN or event.key == K_s) and direction != 1:
                    direction = 2'''

                if event.key == K_LEFT :
                    mat_change = numpy.dot(mat_change, LEFT)
                elif event.key == K_RIGHT :
                    mat_change = numpy.dot(mat_change, RIGHT)
                elif event.key == K_UP :
                    mat_change = numpy.dot(mat_change, UP)
                elif event.key == K_DOWN :
                    mat_change = numpy.dot(mat_change, DOWN)
                elif event.key == K_a :
                    dtmp = numpy.array([0,-1,0])
                    if not (numpy.dot(mat_change, dtmp)==direction).all():
                        direction = numpy.dot(mat_change, dtmp)
                elif event.key == K_w :
                    dtmp = numpy.array([0,0,1])
                    if not (numpy.dot(mat_change, dtmp)==direction).all():
                        direction = numpy.dot(mat_change, dtmp)
                elif event.key == K_s :
                    dtmp = numpy.array([0,0,-1])
                    if not (numpy.dot(mat_change, dtmp)==direction).all():
                        direction = numpy.dot(mat_change, dtmp)
                elif event.key == K_d :
                    dtmp = numpy.array([0,1,0])
                    if not (numpy.dot(mat_change, dtmp)==direction).all():
                        direction = numpy.dot(mat_change, dtmp)
                elif event.key == K_ESCAPE:
                    terminate()
        snake_move(direction, snake_coords) #移动
        flag = snake_check(snake_coords)
        if not flag:
            break #游戏结束
        snake_food(snake_coords, food) #判断是否吃到食物
        screen.fill((0,0,0))
        snake_draw(screen, snake_coords)
        food_draw(screen, food)
        score_draw(screen, len(snake_coords) - 3)
        pygame.display.update()
        snake_speed_clock.tick(snake_speed)


def main():
    pygame.init() # 初始化
    snake_speed_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((windows_width, windows_height))
    screen.fill((0,0,0))
    pygame.display.set_caption("贪吃蛇")
    while True:
        game_body(screen, snake_speed_clock)#主程序
        show_gameover_info(screen)

main()

'''
    3d的时候z轴使用height方便以后加按钮
'''