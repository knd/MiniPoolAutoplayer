import math
import ImageFile, Image, ImageDraw
import findBalls


class Ball:
    # color: will be marked as number 
    def __init__(self, r, position , color): 
        self.x = position[0] 
        self.y = position[1]
        self.r = r
        self.color = color

        self.wall_x1 = 60 
        self.wall_y1 = 130

        self.wall_x2 = 640
        self.wall_y2 = 420 

        hole1 =  Hole(0, 59, 130, 80, 150)
        hole2 =  Hole(1, 60, 395, 80, 415)
        hole3 =  Hole(2, 340, 400, 360, 420)
        hole4 =  Hole(3, 620, 410, 640, 430)
        hole5 =  Hole(4, 620, 130, 640, 150)
        hole6 =  Hole(5, 340, 130, 360, 150)
        self.hole = [hole1, hole2, hole3, hole4, hole5, hole6]

    def printOut(self): 
        print self.x, self.y, self.r, self.color

    def touch(self, x, y): 
        # alpha = 0.18
        alpha = 0.35
        dist = math.hypot(x - self.x, y-self.y)
        return self.r*2 - alpha <=  dist <= self.r*2 + alpha

    def touchOther(self, x1, y1, x2, y2): 
        alpha = 0.1
        dist = math.hypot(x1- x2, y1-y2)
        return self.r*2 - alpha <=  dist <= self.r*2 + alpha

    def touchTable(self, x, y): 
        return x <= self.wall_x1  + self.r or x >= self.wall_x2 - self.r or y <= self.wall_y1 + self.r or y >= self.wall_y2 - self.r

    def isInHole(self, x, y):
        for i in range(len(self.hole)): 
            if self.hole[i].x1 <= x and x <= self.hole[i].x2 and self.hole[i].y1 <= y and y <= self.hole[i].y2: 
                # print "reach the hole", self.hole[i].index
                return True
            # if i == 2: 
            #   if hole[i].x1 <= x and x <= hole[i].x2: 
            #       print "reach the hole", hole[i].index
            #       return True
            # if i == 5: 
            #   if hole[i].x1 <= x and x <= hole[i].x2: 
            #       print "reach the hole", hole[i].index
            #       return True
        return False


    def hitAnyBall(self, x, y, balls, index):
        # constants
        step = 1
        alpha = 0.35
        # take care if the x == self.x
        if x == self.x: 
            newX, newY = self.x, self.y
            # be careful here since ball my on the walls
            while self.inTable(newX, newY):
                if self.y > y: 
                    newY += step 
                else: 
                    newY -= step
                if self.touchTable(newX, newY):
                    # print "hit the ball @ ", x, y
                    # print "touch the table @ ", newX, newY
                    if self.isInHole(newX, newY):
                        # print "hit the ball ", index, " @ ", x, y
                        # print "touch table @", newX, newY
                        return (x, y)
                    return (-1, -1)
                for i in range(len(balls)): 
                    tempx, tempy = balls[i].x, balls[i].y
                    dist = math.hypot(tempx - newX, tempy - newY)
                    if dist < self.r *2 - alpha and not self.x == tempx and not self.y == tempy: 
                        # for debugging
                        # print x, y
                        return (-1, -1)

            return (-1, -1)
        #case that x != self.x
        # print x, y, self.x, self.y
        m = (y - self.y)*1.0/(x-self.x)
        # print "slope of equations = ", m
        newX = self.x
        newY = self.y 
        while self.inTable(newX, newY):
            if self.x > x: 
                newX += step
            else: 
                newX -= step
            newY = (m*(newX - self.x) + self.y)
            ## doing hole only for this one, we need to add for other cases
            if self.touchTable(newX, newY):
                # print "hit the ball @ ", x, y
                # print "touch the table @ ", newX, newY
                if self.isInHole(newX, newY):
                    # print "hit the ball ", index, " @ ", x, y
                    # print "touch table @", newX, newY
                    return (x, y)
                return (-1, -1)
            
            for i in range(len(balls)): 
                tempx, tempy = balls[i].x ,balls[i].y
                dist = math.hypot(tempx- newX, tempy - newY)
                if dist < self.r * 2 - alpha and not self.x == tempx and not self.y == tempy: 
                    # print "can't get there because other ball", tempx,tempy 
                    return (-1, -1)
        return (-1, -1)


    def inTable(self, x, y): 
        return self.wall_x1 + self.r <= x and x <= self.wall_x2 - self.r and self.wall_y1  + self.r <= y and y <= self.wall_y2 - self.r
                        

class WhiteBall(Ball): 
    
    def getHitPositions(self, otherBall):
        x1 = otherBall.x - self.r * 2
        y1 = otherBall.y - self.r * 2

        x2 = otherBall.x + self.r * 2
        y2 = otherBall.y + self.r * 2

        count = 0
        pos  = [] 
        for x in range(x1, x2 + 1, 1):
            for y in range(y1, y2+1, 1):
                if otherBall.touch(x, y): 
                    pos.append((x, y))

        alpha = 5 
        result = []
        for i in range(len(pos)): 
            midx = (pos[i][0] + self.x)/2.0
            midy = (pos[i][1] + self.y)/2.0

            a = math.hypot(pos[i][0] - midx, pos[i][1] - midy)
            b = math.hypot(pos[i][0] - otherBall.x, pos[i][1] - otherBall.y)
            c = math.hypot(otherBall.x - midx, otherBall.y - midy)

            if math.sqrt(abs(a + b - c)) <= alpha and a <= c and self.inTable(pos[i][0], pos[i][1]):
                result.append(pos[i])
        return result
    
    def hitReflectBall(self, x, y, balls, index): 
        return None

    def hitAnyBall(self, x, y, balls, index): 
        # constants
        step = 1
        alpha = 0.35
        # take care if the x == self.x
        if x == self.x: 
            newX, newY = self.x, self.y
            # be careful here since ball my on the walls
            while self.inTable(newX, newY):
                if self.y < y: 
                    newY += step 
                else: 
                    newY -= step
                for i in range(len(balls)): 
                    tempx, tempy = balls[i].x, balls[i].y
                    dist = math.hypot(tempx - newX, tempy - newY)
                    if dist < self.r *2 - alpha and not balls[i].color == index:
                        # for debugging
                        return False

            return True
        #case that x != self.x
        m = (y - self.y)*1.0/(x-self.x)
        # print m
        newX, newY = self.x, self.y
        while self.inTable(newX, newY):
            if self.x < x: 
                newX += step
            else: 
                newX -= step
            newY = int(m*(newX - self.x) + self.y)
            
            for i in range(len(balls)): 
                tempx, tempy = balls[i].x ,balls[i].y
                dist = math.hypot(tempx- newX, tempy - newY)
                if dist < self.r * 2 - alpha and not balls[i].color == index:
                    return False
        return True

class Hole: 
    def __init__(self, index, x1, y1, x2, y2): 
        self.index = index
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

def switchUpSideDown(pos):
    height = 500
    width = 700
    return (pos[0], height - pos[1])
    
def getMousePosition(): 

    # here is the hardcode for the holes
    # hole1 =  Hole(0, 37, 108, 70, 180)
    # hole2 =  Hole(1, 33, 412, 70, 447)
    # hole3 =  Hole(2, 337, 420, 336, 451)
    # hole4 =  Hole(3, 638, 416, 668, 446)
    # hole5 =  Hole(4, 634, 105, 666, 140)
    # hole6 =  Hole(5, 336, 102, 367, 130)
    # hole = [hole1, hole2, hole3, hole4, hole5, hole6]
    
    # test 1
#   w = WhiteBall(8, (567, 403), 0)
#   r1 = Ball(8, (345, 319), 1)
#   r2 = Ball(8, (140, 400), 2)
#   r3 = Ball(8, (489, 250), 3)
#   r4 = Ball(8, (69, 223), 4)
#   r5 = Ball(8, (213, 409), 5)
#   r6 = Ball(8, (535, 158), 6)
#   r7 = Ball(8, (611, 406), 7)
#   r8 = Ball(8, (515, 282), 8)
#   r9 = Ball(8, (579, 174), 9)
#   balls = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
#
#   # test 2
#   w = WhiteBall(8, (609, 266), 0)
#   r3 = Ball(8, (442, 316), 3)
#   r4 = Ball(8, (220, 154), 4)
#   r7 = Ball(8, (103, 389), 7)
#   r9 = Ball(8, (385, 294), 9)
#   balls = [r3, r4, r7, r9]
#   # balls = [r2]
#
#   # # test 3
#   w = WhiteBall(8, (349, 273), 0)
#   r1 = Ball(8, (343, 316), 1)
#   r2 = Ball(8, (559, 273), 2)
#   r3 = Ball(8, (510, 266), 3)
#   r4 = Ball(8, (68, 220), 4)
#   r5 = Ball(8, (214, 406), 5)
#   r6 = Ball(8, (534, 155), 6)
#   r7 = Ball(8, (589, 406), 7)
#   r8 = Ball(8, (511, 242), 8)
#   r9 = Ball(8, (578, 170), 9)
#   balls = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
#   
#   # test 4
#   w = WhiteBall(8, (340, 271), 0)
#   r1 = Ball(8, (333, 295), 1)
#   r2 = Ball(8, (475, 170), 2)
#   r3 = Ball(8, (196, 408), 3)
#   r4 = Ball(8, (527, 173), 4)
#   r5 = Ball(8, (245, 340), 5)
#   r6 = Ball(8, (515, 222), 6)
#   r7 = Ball(8, (530, 201), 7)
#   r8 = Ball(8, (503, 274), 8)
#   r9 = Ball(8, (524, 275), 9)
#   balls = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
#
#   # test 5
#    w = WhiteBall(8, (348, 276), 0)
#    r1 = Ball(8, (226, 172), 1)
#    r2 = Ball(8, (539, 294), 2)
#    r3 = Ball(8, (117, 336), 3)
#    r4 = Ball(8, (274, 243), 4)
#    r5 = Ball(8, (68, 237), 5)
#    r6 = Ball(8, (509, 266), 6)
#    r7 = Ball(8, (401, 327), 7)
#    r8 = Ball(8, (494, 203), 8)
#    r9 = Ball(8, (574, 246), 9)
#    balls = [r1, r2, r3, r4, r5, r6, r7, r8, r9]
    # balls = [r6]

    image = Image.open("screenshot.png")
    balls = findBalls.getBallPositions(image)
    
    b = []
    for i in range(len(balls)): 
        if balls[i][0] == 0: 
            print "there is a white ball"
            w = WhiteBall(8, switchUpSideDown(balls[i][1]), 0)
        else: 
            b.append(Ball(8, switchUpSideDown(balls[i][1]), i + 1))
    
    for i in range(len(b)): 
        print b[i].x, b[i].y

    balls = b
    # this is for selecting target position
    angle = 0
    ball = -1
    firstTarget = []
    secondTarget = []
    for i in range(len(balls)): 
        regularBall = balls[i]
        result = w.getHitPositions(regularBall)
        found = False
        for j in range(len(result)):
            hitPoint = result[j]
            if w.hitAnyBall(hitPoint[0], hitPoint[1], balls, regularBall.color): 
		firstTarget.append(hitPoint)
                position = regularBall.hitAnyBall(hitPoint[0], hitPoint[1], balls, regularBall.color)
                if not position == (-1, -1):
                    secondTarget.append(position)
#                    temp = calAngle( position, (w.x, w.y), (balls[i].x, balls[i].y) ) 
#                    if temp > angle: 
#                        angle = temp
#                        ball = balls[i].color
#                        target = position
    # return switchUpSideDown((w.x, w.y)) , switchUpSideDown(position)
    # print "=============="
    # print "target : ball ", ball
    # print "hit ball @ ", target
    # print "angle = ", angle

    # return the positon of target 
    for i in range(len(secondTarget)):
    	secondTarget[i] = switchUpSideDown(secondTarget[i])
    for i in range(len(firstTarget)): 
	firstTarget[i] = switchUpSideDown(firstTarget[i])

    return switchUpSideDown((w.x, w.y)), secondTarget + [firstTarget[0]]
    # return switchUpSideDown((w.x, w.y)), [switchUpSideDown(target)]

def calAngle(pointA, pointB, pointC):
    side1 = math.hypot( pointA[0] - pointB[0], pointA[1] - pointB[1])   
    side2 = math.hypot( pointB[0] - pointC[0], pointB[1] - pointC[1])   
    side3 = math.hypot( pointC[0] - pointA[0], pointC[1] - pointA[1])   

    return (side1**2 + side2**2 - side3**2)/(2*side1*side2)

if __name__ == "__main__": 
    print getMousePosition()
