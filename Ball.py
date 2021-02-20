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

    def check_death(self):      # Redundant now, updated to isDead()
        if self.x == self.lim_x-1:
            return True
        else:
            return False

    def __check_collision(self, fut_x, fut_y, plank):
        global ar
        fut_x = int(fut_x)
        fut_y = int(fut_y)
        if fut_x <= 0 or fut_x >= self.lim_x - 1 or fut_y >= self.lim_y - 1 or fut_y <= 0:
            return 'wall'
        for i in range(int(fabs(self.vel_y)+1)):
            for j in range(int(fabs(self.vel_x))+1):
                av = j
                if self.vel_x < 0:
                    av = -1*av
                if self.vel_y > 0 and ar[int(self.x + av)][int(self.y + i)] >= 3:
                    return 'brick'
                if self.vel_y < 0 and ar[int(self.x + av)][int(self.y - i)] >= 3:
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

    def __handle_wall_collision(self):
        if self.x + self.vel_x >= self.lim_x-1 or self.x + self.vel_x <= 0:
            self.vel_x = -1*self.vel_x
        if self.y + self.vel_y >= self.lim_y-1 or self.y + self.vel_y <= 0:
            self.vel_y = -1*self.vel_y

    def __handle_brick_collision(self):
        global brk
        xt = False
        yt = False
        pts = 0
        pp = 0
        if props["ThroughBall"]:
            ar[int(self.x)][int(self.y)]=0
            tvel_x = fabs(self.vel_x)
            tvel_y = fabs(self.vel_y)
            
            while self.x < self.lim_x - 1 and self.y < self.lim_y - 1 and (tvel_x > 0 or tvel_y > 0):
                for i in range(3):
                    if self.vel_x > 0:
                        if ar[int(self.x+i)][int(self.y)] == 4:
                            pts+=brk[int(self.x+i)][int(self.y)].destroy(ar,brk)
                    else:
                        if ar[int(self.x-i)][int(self.y)] == 4:
                            pts+=brk[int(self.x-i)][int(self.y)].destroy(ar,brk)
                    if self.vel_y > 0:
                        if ar[int(self.x)][int(self.y+i)] == 4:
                            pts+=brk[int(self.x)][int(self.y+i)].destroy(ar,brk)
                    else:
                        if ar[int(self.x)][int(self.y-i)]==4:
                            pts+=brk[int(self.x)][int(self.y-i)].destroy(ar,brk)
                    adsx = 1
                    if self.vel_x < 0:
                        adsx = -1
                    adsy = 1
                    if self.vel_y < 0:
                        adsy = -1
                    
                    for j in range(3):
                        if ar[int(self.x+(adsx*i))][int(self.y+(adsy*j))] == 4:
                            pts+=brk[int(self.x+(adsx*i))][int(self.y+(adsy*j))].destroy(ar,brk)
                if tvel_y <= tvel_x:
                    avx = 1
                    if self.vel_x < 0:
                        avx = -1
                    self.x += avx
                    tvel_x-=1
                if tvel_y >= tvel_x:
                    avy = 1
                    if self.vel_y < 0:
                        avy = -1
                    self.y += avy
                    tvel_y-=1
                    
            # pp = ar[int(self.x)][int(self.y)]
            ar[int(self.x)][int(self.y)]=1

            return pts
        tempVX = self.vel_x 
        tempVY = self.vel_y
        xsi = 1
        if self.vel_x < 0:
            xsi = -1
        ysi = 1
        if self.vel_y < 0:
            ysi = -1
        xdis = 0
        ydis = 0
        self.vel_x = xsi
        self.vel_y = ysi
        pts = 0
        while fabs(xdis) < fabs(tempVX) or fabs(ydis) < fabs(tempVY):
            xt = False
            yt = False
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
                self.vel_x = -1*xsi
            if yt:
                self.vel_y = -1*ysi
            if xt or yt:
                self.vel_y *= fabs(tempVY)
                self.vel_x *= fabs(tempVX)
                return pts
            if xdis != tempVX:
                ar[int(self.x)][int(self.y)]=0
                xdis += xsi
                self.x += xsi
                ar[int(self.x)][int(self.y)]=1
            if ydis != tempVY:
                ar[int(self.x)][int(self.y)]=0
                ydis += ysi
                self.y += ysi
                ar[int(self.x)][int(self.y)]=1
        if pts == 0:
            self.vel_x = tempVX
            self.vel_y = tempVY
        return pts

        
        

    def __handle_plank_collision(self, plank):
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
        if self.__check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'brick':
            pts = self.__handle_brick_collision()
        if self.__check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'plank':
            self.__handle_plank_collision(plank)
        if self.__check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'wall':
            self.__handle_wall_collision()
        if self.__check_collision(self.x+self.vel_x, self.y+self.vel_y, plank) == 'None':
            ar[int(self.x)][int(self.y)] = 0
            self.x += self.vel_x
            self.y += self.vel_y
            ar[int(self.x)][int(self.y)] = 1
        return False, pts

    def launch_object(self):
        if self.vel_x == 0 and self.vel_y == 0:
            self.vel_x = -1
            self.vel_y = 1  
        if self.vel_x > 0:
            self.vel_x = -1*self.vel_x
        self.state = 'moving'
