# from variables import game_matrix as ar



'''
    Bricks look like this : 
0         1         2         3         4         5         6         7         8         9        10         11
012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
1    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
2    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
3               [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
4               [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
5    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]                    
6    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
7               [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
8               [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]
9    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]                    
0    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]    [=][=][=][=][=]                    
1
'''

class Brick:
    def __init__(self,pos_x,pos_y,poo):
        self.x = pos_x
        self.y = pos_y
        self.state = 'alive'
        self.poo = poo
    
    def remove(self,ar):
        # global ar
        if ar[int(self.x)][int(self.y)] != 4:
            print('X,Y where we find error :',self.x,self.y)
            import time
            time.sleep(3)
            exit(0)
        ar[int(self.x)][int(self.y)] = 0
        ar[int(self.x)][int(self.y-1)] = 0
        ar[int(self.x)][int(self.y+1)] = 0
    
    def check_powerUp(self):
        for i in range(len(self.poo)):
            if self.poo[i] != None and self.poo[i].x == self.x and (self.poo[i].y-self.y)**2 <= 1:
                self.poo[i].visible = True
                self.poo[i].moving = True

    


class NormalBrick(Brick):
    def __init__(self,pos_x,pos_y,level,poo):
        super().__init__(pos_x,pos_y,poo)
        self.level = level
    
    def collide(self,ar,brickObj):
        self.check_powerUp()
        score = 0
        self.level-=1
        from variables import score
        if self.level == 0:
            self.remove(ar)
            self.state = 'dead'
            score+=3
            return self.state,score
        else:
            score+=2
            return self.state,score
    def destroy(self,ar,brickObj):
        su = 0
        while self.state == 'alive':
            a,su1 = self.collide(ar,brickObj)
            su+=su1
        ar[int(self.x)][int(self.y)]=0
        ar[int(self.x)][int(self.y+1)]=0
        ar[int(self.x)][int(self.y-1)]=0
        brickObj[int(self.x)][int(self.y)]=None
        self.state = 'dead'
        return su

class UnbreakableBrick(Brick):
    def __init__(self,pos_x,pos_y,poo):
        super().__init__(pos_x,pos_y,poo)
        self.level = 10
        
    def collide(self,ar,brickObj):
        self.check_powerUp()
        # do nothing
        return self.state,0
    
    def destroy(self,ar,brickObj):
        # 10 points for destroying the unbreakable bricks
        self.level = 0
        ar[int(self.x)][int(self.y)] = 0
        ar[int(self.x)][int(self.y+1)] = 0
        ar[int(self.x)][int(self.y-1)] = 0
        brickObj[int(self.x)][int(self.y)] = None
        self.state = 'dead'
        return 10
        

class ExplodingBrick(Brick):
    def __init__(self,pos_x,pos_y,poo):
        super().__init__(pos_x,pos_y,poo)
        self.level = 100

    def collide(self,ar,brickObj):
        self.check_powerUp()
        return 'dead',self.destroy(ar,brickObj)
    
    
    def destroy(self,ar,brickObj):
        self.check_powerUp()
        sc_su = 0
        self.state = 'dead'
        brickObj[int(self.x)][int(self.y)] = None
        for i in range(5):
            if ar[int(self.x)][int(self.y+i)]==4 and brickObj[int(self.x)][int(self.y+i)] != None:
                # print('Hello World',self.x,int(self.y+i))
                sc_su += brickObj[int(self.x)][int(self.y+i)].destroy(ar,brickObj)
            if ar[int(self.x)][int(self.y-i)]==4 and brickObj[int(self.x)][int(self.y-i)] != None:
                # print('Hello World',self.x,int(self.y-i))
                sc_su += brickObj[int(self.x)][int(self.y-i)].destroy(ar,brickObj)
            if ar[int(self.x+1)][int(self.y+i)]==4 and brickObj[int(self.x+1)][int(self.y+i)] != None:
                # print('Hello World',self.x+1,int(self.y+i))
                sc_su += brickObj[int(self.x+1)][int(self.y+i)].destroy(ar,brickObj)
            if ar[int(self.x-1)][int(self.y-i)]==4 and brickObj[int(self.x-1)][int(self.y-i)] != None:
                # print('Hello World',self.x-1,int(self.y-i))
                sc_su += brickObj[int(self.x-1)][int(self.y-i)].destroy(ar,brickObj)
            if ar[int(self.x-1)][int(self.y+i)]==4 and brickObj[int(self.x-1)][int(self.y+i)] != None:
                # print('Hello World',self.x-1,int(self.y+i))
                sc_su += brickObj[int(self.x-1)][int(self.y+i)].destroy(ar,brickObj)
            if ar[int(self.x-1)][int(self.y+i)]==4 and brickObj[int(self.x-1)][int(self.y+i)] != None:
                # print('Hello World',self.x-1,int(self.y+i))
                sc_su += brickObj[int(self.x-1)][int(self.y+i)].destroy(ar,brickObj)

        ar[int(self.x)][int(self.y)]=0
        ar[int(self.x)][int(self.y-1)]=0
        ar[int(self.x)][int(self.y+1)]=0
        return sc_su