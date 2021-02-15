

class Motion:
    def __init__(self, x_pos, y_pos, x_limit, y_limit, width):
        self.x = x_pos
        self.y = y_pos
        self.lim_x = x_limit
        self.lim_y = y_limit
        self.width = width

    def _check_limit(self, x_d, y_d):
        if x_d + self.x < 0 or self.x + x_d > self.lim_x or y_d + self.y - self.width < 0 or self.y + y_d + self.width > self.lim_y:
            return True
        else:
            return False

    def move_object(self, x_disp, y_disp):
        if self._check_limit(x_disp, y_disp) == False:
            self.x += x_disp
            self.y += y_disp
            return True
        else:
            return False
