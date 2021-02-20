from variables import *
from util_methods import *
import numpy as np
import sys
from time import sleep
from Board import Board
import time
from input import Get
from Ball import Ball
from input import input_to
import colorama
from tempVar import ball_list

MSG = '''
  ____           _          _        ____                          _                  
 | __ )   _ __  (_)   ___  | | __   | __ )   _ __    ___    __ _  | | __   ___   _ __ 
 |  _ \  | '__| | |  / __| | |/ /   |  _ \  | '__|  / _ \  / _` | | |/ /  / _ \ | '__|
 | |_) | | |    | | | (__  |   <    | |_) | | |    |  __/ | (_| | |   <  |  __/ | |   
 |____/  |_|    |_|  \___| |_|\_\   |____/  |_|     \___|  \__,_| |_|\_\  \___| |_|   
                                                                                      

'''

'''
    -----Game Session Variables------
'''

sys.stdout.write('\033[?25l')
for i in range(WINDOW_HEIGHT):
    for j in range(WINDOW_WIDTH):
        if i == WINDOW_HEIGHT - 1 or j == WINDOW_WIDTH - 1 or i == 0 or j == 0:
            game_matrix[i][j] = - 1
    

def render_game():
    # print(game_matrix)
    # sleep(100)
    pr = []
    for i in range(len(game_matrix)):
        for j in range(len(game_matrix[0])):
            if game_matrix[i][j]==4:
                if BrickOb[i][j].level == 1:
                    sys.stdout.write(colorama.Back.LIGHTCYAN_EX+colorama.Fore.LIGHTCYAN_EX+"=")
                elif BrickOb[i][j].level == 2:
                    sys.stdout.write(colorama.Back.YELLOW+colorama.Fore.YELLOW+"=")
                elif BrickOb[i][j].level == 3:
                    sys.stdout.write(colorama.Back.WHITE+colorama.Fore.WHITE+"=")
                elif BrickOb[i][j].level == 10:
                    sys.stdout.write(colorama.Back.LIGHTRED_EX+colorama.Fore.LIGHTRED_EX+"=")
                else:
                    sys.stdout.write(colorama.Back.GREEN+"=")
            elif game_matrix[i][j]==3 and game_matrix[i][j-1]==4:
                if BrickOb[i][j-1].level == 1:
                    sys.stdout.write(colorama.Back.LIGHTCYAN_EX+colorama.Fore.LIGHTCYAN_EX+"]")
                elif BrickOb[i][j-1].level == 2:
                    sys.stdout.write(colorama.Back.YELLOW+colorama.Fore.YELLOW+"]")
                elif BrickOb[i][j-1].level == 3:
                    sys.stdout.write(colorama.Back.WHITE+colorama.Fore.WHITE+"]")
                elif BrickOb[i][j-1].level == 10:
                    sys.stdout.write(colorama.Back.LIGHTRED_EX+colorama.Fore.LIGHTRED_EX+"]")
                else:
                    sys.stdout.write(colorama.Back.GREEN+"]")

            elif game_matrix[i][j]==3:
                if BrickOb[i][j+1].level == 1:
                    sys.stdout.write(colorama.Back.LIGHTCYAN_EX+colorama.Fore.LIGHTCYAN_EX+"[")
                elif BrickOb[i][j+1].level == 2:
                    sys.stdout.write(colorama.Back.YELLOW+colorama.Fore.YELLOW+"[")
                elif BrickOb[i][j+1].level == 3:
                    sys.stdout.write(colorama.Back.WHITE+colorama.Fore.WHITE+"[")
                elif BrickOb[i][j+1].level == 10:
                    sys.stdout.write(colorama.Back.LIGHTRED_EX+colorama.Fore.LIGHTRED_EX+"[")
                else:
                    sys.stdout.write(colorama.Back.GREEN+"[")
                
            if game_matrix[i][j] == 0:
                sys.stdout.write(" ")
            elif game_matrix[i][j] == -1:
                sys.stdout.write(colorama.Back.BLACK+" ")
            elif game_matrix[i][j] == 1:
                sys.stdout.write(colorama.Fore.RED+"o")
            elif game_matrix[i][j] == 2:  # plank
                sys.stdout.write(colorama.Back.BLUE+colorama.Fore.BLUE+"=")
            sys.stdout.write(colorama.Back.RESET)
            sys.stdout.write(colorama.Fore.RESET)
        sys.stdout.write('           ')
        sys.stdout.write('\n')


def showDashboard():
    sys.stdout.write(colorama.Back.BLACK)
    sys.stdout.write(colorama.Fore.LIGHTGREEN_EX+MSG)
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX+'Score : ')
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX+str(score)+'                                                                                                                                   ')
    sys.stdout.write('\n')
    # sys.stdout.write(colorama.Back.RESET)
    
    sys.stdout.write(colorama.Back.BLUE)
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX+'Time Elapsed : ')
    sys.stdout.write(colorama.Fore.LIGHTYELLOW_EX+str(int((time.process_time_ns()-secs)/100000000))+'                                                                                                                           ')
    # sys.stdout.write(colorama.Back.RESET)
    sys.stdout.write('\n')
    sys.stdout.write(colorama.Back.BLACK)
    sys.stdout.write(colorama.Fore.WHITE+'Lives : ')
    for i in range(lives):
        sys.stdout.write(colorama.Back.BLACK+' @ ')
    for i in range(5-lives):
        sys.stdout.write(colorama.Back.BLACK+' X ')
    sys.stdout.write('                                                                                                                        ')
    # sys.stdout.write(colorama.Back.RESET)
    # sys.stdout.write(colorama.Fore.RESET)
    sys.stdout.write('\n')
    for i in range(WINDOW_WIDTH):
        if i % 3 == 1:
            sys.stdout.write(colorama.Back.RED+'X')
        else:
            sys.stdout.write(colorama.Back.RED+'=')
    sys.stdout.write(colorama.Fore.RESET)
    sys.stdout.write(colorama.Back.RESET)
    sys.stdout.write('\n')

ball = Ball(WINDOW_HEIGHT-11, WINDOW_WIDTH/2, WINDOW_HEIGHT, WINDOW_WIDTH)
plank = Board(WINDOW_HEIGHT-10, WINDOW_WIDTH-1,
              WINDOW_HEIGHT-10, WINDOW_WIDTH/2,ball)
ball_list.append(ball)
ball_list.append(Ball(WINDOW_HEIGHT-11, WINDOW_WIDTH/2+1, WINDOW_HEIGHT, WINDOW_WIDTH))
'''
Game Loop
'''
system('clear')

while True:
    chinp = input_to(Get(), 0.05)
    sleep(0.1)
    # while(time.time_ns()-tmp_t <= 15000000):
    #     continue
    sys.stdin.flush()
    # clear_screen()
    print('\033[%d;%dH'%(0,0))
    showDashboard()
    render_game()
    displayPowers()
    print(colorama.Back.RESET+colorama.Fore.RESET+"\033["+str(int(WINDOW_HEIGHT+12))+";"+"0"+"f")
    if chinp == 'q':
        exit(0)
    elif chinp == 'p':
        if mode=='play':
            mode='pause'
        else:
            mode='play'
    elif chinp == 's':
        for jojo in range(len(ball_list)):
            if ball_list[jojo] != None and ball_list[jojo].state == 'rest':  # launch the ball
                ball_list[jojo].launch_object()
    elif chinp == 'a' or chinp == 'd':
        plank.move(chinp)
    if mode=='pause':
        continue
    plank.placePlank(Ball)
    zod = 0
    while zod < len(ball_list):
        if ball_list[zod]==None:
            zod+=1
            continue
        az,bz = ball_list[zod].move_object(plank)
        score+=bz    
        if az:
            cl = 0
            for jon in range(len(ball_list)):
                if ball_list[jon]!= None:
                    cl+=1
            if cl <= 1:
                lives -= 1
                if props["PGtime"]==1:
                    props["PaddleGrab"] = False
                else:
                    props["PGtime"] = 1

                if props["TBtime"]==1:
                    props["ThroughBall"] = False
                else:
                    props["TBtime"] = 1
                if lives == 0:
                    from gameover import display_end
                    display_end(score)
                    exit(0)
                else:
                    game_matrix[int(ball_list[zod].x)][int(ball_list[zod].y)] = 0
                    ball_list[zod].reset(plank.x-1, plank.y)
                    game_matrix[int(ball_list[zod].x)][int(ball_list[zod].y)] = 1
            else:
                game_matrix[int(ball_list[zod].x)][int(ball_list[zod].y)] = 0
                ball_list[zod]=None
        zod+=1

sys.stdout.write('\033[?25h')