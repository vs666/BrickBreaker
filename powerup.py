import colorama
from tempVar import ball_list

class PowerUp:
    def __init__(self, x, y, power_type, x_limit):
        self.x = x
        self.y = y
        self.x_limit = x_limit
        self.visible = False
        self.moving = False
        self.power_type = power_type

    def display(self, x, y, ch):
        if self.visible:
            if self.power_type == 'EP':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.LIGHTMAGENTA_EX+colorama.Fore.YELLOW+str(ch))
            elif self.power_type == 'BS':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.LIGHTGREEN_EX+colorama.Fore.YELLOW+str(ch))
            elif self.power_type == 'TB':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.LIGHTBLUE_EX+colorama.Fore.YELLOW+str(ch))
            elif self.power_type == 'SP':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.LIGHTRED_EX+colorama.Fore.YELLOW+str(ch))
            elif self.power_type == 'BS':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.LIGHTCYAN_EX+colorama.Fore.YELLOW+str(ch))
            elif self.power_type == 'PG':
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.WHITE+colorama.Fore.YELLOW+str(ch))
            else:
                print("\033["+str(int(x+11))+";"+str(int(y))+"f" +
                  colorama.Back.YELLOW+colorama.Fore.YELLOW+str(ch))
        if self.moving:
            self.x += 1

    def show(self):
        self.display(self.x, self.y, self.power_type)
        if self.x == self.x_limit:
            return True
        else:
            return False

    def charge(self):
        pass # execute polymorphism

class ExpandPaddle(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'EP', x_limit)
        self.paddle_object = paddle_object

    def charge(self, paddle_object):
        self.visible = False
        paddle_object.wi += 2


class ShrinkPaddle(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'SP', x_limit)
        self.paddle_object = paddle_object

    def charge(self, paddle_object):
        self.visible = False
        if paddle_object.wi <= 2:
            paddle_object = 2
        else:
            paddle_object.wi -= 1
        return True


class PaddleGrab(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'PG', x_limit)
        self.paddle_object = paddle_object
        

    def charge(self, props):
        props["PaddleGrab"] = True
        props["PGtime"] = 0
        self.visible = False


class BallFast(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'BF', x_limit)

    def charge(self, ball_ob):
        self.visible = False
        ball_ob.vel_x += 1
        # import time a


class BallSlow(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'BF', x_limit)

    def charge(self, ball_ob):
        self.visible = False
        if ball_ob.vel_x >= 2:
            ball_ob.vel_x -= 1
        # import time a

class ThroughBall(PowerUp):
    def __init__(self, x, y, paddle_object, x_limit):
        super().__init__(x, y, 'TB', x_limit)

    def charge(self, props):
        self.visible = False
        props["ThroughBall"]=True
        props["TBtime"]=0
        
class BallSplit(PowerUp):
    def __init__(self,x,y,paddle_object,x_limit):
        super().__init__(x,y,'BS',x_limit)

    def charge(self,Ball):
        print("BALL SPLIT")
        le = len(ball_list)
        self.visible = False
        for i in range(le):
            if ball_list[i] != None:
                ball_list.append(Ball(ball_list[i].x,ball_list[i].y,ball_list[i].lim_x, ball_list[i].lim_y))
        # done    
