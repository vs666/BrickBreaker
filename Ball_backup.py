from motion import Motion
from Board import Board
from variables import game_matrix as ar
from variables import props
from variables import BrickOb as brk
from math import fabs
'''
check death 
check collision 
reflect vertical
reflect horizontial
reflect board ( pass board object)
dead ball (board object ??)
'''


class Ball(Motion):
    def __init__(self, x_in, y_in, x_lim, y_lim):
        super().__init__(x_in, y_in, x_lim, y_lim, 0)
        self.vel_x = 0
        self.vel_y = 0
        self.state = 'rest'

    def check_death(self):
        if self.x == self.lim_x-1:
            return True
        else:
            return False

    def check_collision(self, fut_x, fut_y, plank):
        global ar
        fut_x = int(fut_x)
        fut_y = int(fut_y)
        if fut_x <= 0 or fut_x >= self.lim_x - 1 or fut_y >= self.lim_y - 1 or fut_y <= 0:
            return 'wall'
        for i in range(int(fabs(self.vel_y)+1)):

            if self.vel_y > 0 and ar[fut_x][int(self.y + i)] >= 3:
                return 'brick'
            if self.vel_y < 0 and ar[fut_x][int(self.y - i)] >= 3:
                return 'brick'
        if (fut_x >= plank.x and self.x < plank.x) and ((plank.y + int(plank.wi) >= self.y and self.y >= plank.y - int(plank.wi))):
            return 'plank'
        elif (fut_x >= plank.x and self.x < plank.x) and self.y + self.vel_y <= plank.y + int(plank.wi) and self.y+self.vel_y >= plank.y + int(plank.wi):
            return 'plank'
        else:
            return 'None'

    def handle_collision(self):     # Handles normal collision and not with plank
        global ar
        if (self.x+self.vel_x) <= 0 or (self.x+self.vel_x) >= self.lim_x-1 or ar[int(self.x+self.vel_x)][int(self.y)] != 0:
            self.vel_x = -1*self.vel_x
        if (self.y + self.vel_y) <= 0 or (self.y + self.vel_y) >= self.lim_y - 1 or ar[int(self.x)][int(self.y+self.vel_y)] != 0:
            self.vel_y = -1*self.vel_y
        elif ar[int(self.vel_x+self.x)][int(self.vel_y+self.y)] != 0:
            self.vel_x = -1*self.vel_x
            self.vel_y = -1*self.vel_y

        # else no collision has happened

    def handle_wall_collision(self):
        if self.x + self.vel_x >= self.lim_x-1 or self.x + self.vel_x <= 0:
            self.vel_x = -1*self.vel_x
        if self.y + self.vel_y >= self.lim_y-1 or self.y + self.vel_y <= 0:
            self.vel_y = -1*self.vel_y

    def handle_brick_collision(self):
        global brk
        xt = False
        yt = False
        pts = 0
        for i in range(int(fabs(self.vel_y)+2)):
            if self.vel_y > 0 and ar[int(self.x + self.vel_x)][int(self.y+i)] == 4:
                a,b = brk[int(self.x + self.vel_x)][int(self.y+i)].collide(ar,brk)
                pts+=b
                xt = True
            if self.vel_y < 0 and ar[int(self.x + self.vel_x)][int(self.y-i)] == 4:
                a,b = brk[int(self.x + self.vel_x)][int(self.y-i)].collide(ar,brk)
                pts+=b
                xt = True
        if self.vel_y > 0 and ar[int(self.x+self.vel_x)][int(self.y-1)] == 4:
            xt = True
            a,b = brk[int(self.x+self.vel_x)][int(self.y-1)].collide(ar,brk)
            pts+=b
        if self.vel_y < 0 and ar[int(self.x + self.vel_x)][int(self.y+1)] == 4:
            xt = True
            a,b = brk[int(self.x+self.vel_x)][int(self.y+1)].collide(ar,brk)
            pts+=b
        if self.vel_y > 0 and ar[int(self.x)][int(self.y+1)] == 3:
            yt = True
            a,b = brk[int(self.x)][int(self.y+2)].collide(ar,brk)
            pts+=b
        if self.vel_y < 0 and ar[int(self.x)][int(self.y-1)] == 3:
            yt = True
            a,b = brk[int(self.x)][int(self.y-2)].collide(ar,brk)
            pts+=b
        if xt:
            self.vel_x = -1*self.vel_x
        if yt:
            self.vel_y = -1*self.vel_y
        return pts
    def handle_plank_collision(self, plank):
        '''
                All the plank collision logic here
        '''
        if props["PaddleGrab"]:
            ar[int(self.x)][int(self.y)]=0
            self.reset(plank.x,plank.y)
        else:
            import math
            if self.state != 'rest' and self.y > plank.y + int(plank.wi) and self.y < plank.y - int(plank.wi):
                self.vel_y = -1*int(self.vel_y/math.fabs(self.vel_y))*fabs(self.y-plank.wi)
            elif self.state != 'rest':
                self.vel_x = -1*self.vel_x
                # self.vel_y = (plank.x-self.x)

    def reset(self, x, y):
        # self.vel_x = 0
        # self.vel_y = 0
        self.x = x
        self.y = y
        self.state = 'rest'

    def isDead(self):
        if self.x + self.vel_x >= self.lim_x-5:
            return True
        return False

    def move_object(self, plank):   # overriding
        global ar
        pts = 0
        if self.state == 'rest':
            ar[int(self.x)][int(self.y)] = 0
            self.x = plank.x - 1
            self.y = plank.y
            ar[int(self.x)][int(self.y)] = 1
            return False, 0
        if self.isDead():
            return True, 0
        elif self.check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'plank':
            self.handle_plank_collision(plank)
        elif self.check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'wall':
            self.handle_wall_collision()
        elif self.check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'brick':
            pts = self.handle_brick_collision()
        if self.check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'None':
            ar[int(self.x)][int(self.y)] = 0
            self.x += self.vel_x
            self.y += self.vel_y
            ar[int(self.x)][int(self.y)] = 1
        return False, pts

    def launch_object(self):
        self.vel_x = -1
        self.vel_y = 1  
        self.state = 'moving'
