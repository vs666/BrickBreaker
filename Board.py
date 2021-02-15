from motion import Motion
from variables import game_matrix as ar
from variables import power_objects,props

class Board(Motion):
    def __init__(self, x_limit, y_limit, x_initial, y_initial,ball_ob):
        super().__init__(x_initial, y_initial, x_limit, y_limit, 3)
        self.wi = 2
        self.speed = 2
        self.ball_ob = ball_ob
    def move(self, char):
        if char == 'a' or char == 'A':
            if self.y > 1 + self.wi:
                self.move_object(0, int(-1*self.speed))
        elif char == 'd' or char == 'D':
            if self.lim_y - self.y > self.wi + 1:
                self.move_object(0, int(self.speed))
        else:
            pass

    def placePlank(self):
        global ar
        for i in range(self.wi+self.speed):
            if i+self.y < self.lim_y and self.y - i >= 0:
                ar[int(self.x)][int(self.y+i)] = 0
                ar[int(self.x)][int(self.y-i)] = 0

        for i in range(self.wi):
            ar[int(self.x)][int(self.y+i)] = 2
            ar[int(self.x)][int(self.y-i)] = 2
        from math import fabs
        for i in range(len(power_objects)):
            if power_objects[i]!= None and power_objects[i].x == int(self.x) and fabs(power_objects[i].y - self.y) <= self.wi: 
                if power_objects[i].power_type == 'PG':
                    power_objects[i].charge(props)
                elif power_objects[i].power_type == 'BF':
                    from tempVar import ball_list
                    for i in range(len(ball_list)):
                        power_objects[i].charge(ball_list[i])
                elif power_objects[i].power_type == 'BS':
                    power_objects[i].charge()
                else:
                    power_objects[i].charge(self)
                # import time
                # time.sleep(10)

