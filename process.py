
import math


class Processes:

    def __init__(self,x11,x22,y11,y22):
        global x1,x2,y1,y2
        self.x1=x11
        self.x2=x22
        self.y1=y11
        self.y2=y22

    def calculate(self):
        distance = math.sqrt(((self.x2-self.x1)**2)+(self.y2-self.y1)**2)
        print(distance)


p = Processes(1,5,-2,8)
p.calculate()

