#the framerate is very important for the speed of the game and the responsiveness

def setup():                                                                                               
    size(1366, 730)    
    frameRate(80)
    background(100, 100, 100)

               
class Box:
    def __init__(self, speed, positionX, positionY, updown, obstacles):
        #walking speed
        self.speed = speed

        #position in the frame
        self.positionX = positionX
        self.positionY = positionY

        #vertical force acting on the character
        self.G = 0

        #whether it is jumping
        self.jumpstate = 0

        #which direction is it going
        self.direction = 0

        # whether it hits the ground or not
        self.bottom = 0
        
        #whether it's upside down or not
        self.updown = updown  

        #obstacles on the map         
        self.obstacles = obstacles 

        #determine the hit box around the character based on the position. /depicts how much I have to add to the original coordinates to get the other corners of the square    
        self.square = [[0,0], [0,118], [50,0], [50,118]] 
        
        #for the animation
        self.facing = -1
        
        #change the animationstage only after a certain frame count
        self.framecount = 0

        #keeps track of the animation stages
        self.piccount = 0

        #loading pictures for the animation
        self.walkright = {}
        for x in range(4):
            self.walkright[x] = loadImage(str(self.updown) + "walking" + str(x+1) + "right.png")
        
        self.walkleft = {}
        for x in range(4):
            self.walkleft[x] = loadImage(str(self.updown) + "walking" + str(x+1)+"left.png")
        
        self.jumppic = [loadImage(str(self.updown) + "jumpingright.png"), loadImage(str(self.updown) + "jumpingleft.png")]
        self.standpic = [loadImage(str(self.updown) + "standingright.png"), loadImage(str(self.updown) + "standingleft.png")]
            
    
    #function determining if the character hits an obstacle. Returns a string based on what happens        
    def borderHor(self):
        #CHECKS IF I'M WITHIN THE BORDER
        #goes through all the obstacles
        for x in self.obstacles:    
            #goes through all the corners of the square creating one of the corners
            for y in [0,20,40,60,80,100,118]:                    
                PositionY = self.positionY + y
                for z in [0, 50]:
                    PositionX = self.positionX + z
                    if self.updown == 1:           
                    #checks if you're "outside the box or not"
                        
                        if PositionX > x[0] and PositionX < x[1]:  
                            if PositionY > x[2] and PositionY < x[3]:
                                if self.positionY-x[2] > x[3]-self.positionY:
                                    self.positionY += 1
                                else:
                                    self.positionY -= 1
                                return "again"
                            if PositionY == x[2] and PositionY < x[3]:
                                return "ontop"
                            if PositionY == x[3] and PositionY > x[2]:
                                return "onbottom"
                    elif self.updown == -1:
                        if PositionX > x[0] and PositionX < x[1]:  
                            if PositionY > x[2] and PositionY < x[3]:
                                if self.positionY-x[2] > x[3]-self.positionY:
                                    self.positionY += 1
                                else:
                                    self.positionY -= 1
                                return "again"
                            if PositionY == x[2] and PositionY < x[3]:
                                return "onbottom"
                            if PositionY == x[3] and PositionY > x[2]:
                                return "ontop"        
        return "air"
        
    #function determining if the character hits an obstacle. Returns a string based on what happens        
    def borderVert(self):         
    #same logic as the horizontal
        for x in self.obstacles:    
        #goes through all the obstacles
            for y in [0,20,40,60,80,100,118]:                    
            #goes through all the corners of the square    #creating one of the corners
                PositionY = self.positionY + y
                for z in [0, 50]:
                    PositionX = self.positionX + z
                    if PositionY > x[2] and PositionY < x[3]:
                        if PositionX+10 > x[0] and PositionX < x[1]:
                            return "noRight"
                        if PositionX-10 < x[1] and PositionX > x[0]:
                            return "noLeft"
        return "free"
             
    
    #function for moving the character and to make it stop of it hits the boundaries of the play area or obstacles                                                 
    def move(self):
        #repeats until the point moves out of the obstacle
        while self.borderHor() == "again":
            self.G = 0    #so that it stops going upwards
       
        #VARIABLES
        Vert = self.borderVert()
        Hori = self.borderHor()
        #GRAVITY       
        if self.bottom == 0:
            if self.borderHor() == "ontop":
                self.G = 0
            elif Hori == "air" or Hori == "onbottom":
                if self.G < 20:
                    self.G += self.updown*0.3  
        elif self.bottom == 1:
            if self.G < 20:
                self.G += self.updown*0.3
         
        #LEFT OR RIGHT
        if self.direction == -1 and not Vert == "noLeft":
            self.positionX -= 5*self.speed
        if self.direction == 1 and not Vert == "noRight":
            self.positionX += 5*self.speed
         
        #JUMP  
        if self.jumpstate == 1 and Hori == "ontop":
            self.G = -8 * self.updown
         
        #UP OR DOWN
        self.positionY += int(self.G)
        
        
    #determines which animation should be loaded according to the diretion and whether it is jumping or not    
    def display(self):
        
        #jumpleft
        if self.borderHor() == "air" and self.facing == -1:
            image(self.jumppic[1],self.positionX-10, self.positionY, 70, 120)
        
        #jumpright
        elif self.borderHor() == "air" and self.facing == 1:
            image(self.jumppic[0],self.positionX-10, self.positionY, 70, 120)
        
        #running right
        elif self.direction == 1:
            if self.framecount % 14 == 13:
                self.piccount += 1
            self.framecount +=1
            image(self.walkright[self.piccount % 4],self.positionX-10, self.positionY, 70, 120)
        
        #running left
        elif self.direction == -1:
            if self.framecount % 14 == 13:
                self.piccount += 1
            self.framecount +=1
            image(self.walkleft[self.piccount % 4],self.positionX-10, self.positionY, 70, 120)
        
        #standingleft
        elif self.direction == 0 and self.facing == -1:
            image(self.standpic[1],self.positionX-10, self.positionY, 70, 120)
        
        #standingleft
        elif self.direction == 0 and self.facing == 1:
            image(self.standpic[0],self.positionX-10, self.positionY, 70, 120)
        
 

class Level:
    def __init__(self, BoxUp, BoxDown, goals, obstacle, Background):

        #similarly to the character function
        self.obstacles = obstacle
        self.gameover = 0
        self.goals = goals
        self.Square = BoxDown
        self.Boxxy = BoxUp
        self.framecount=0
        self.piccount=0
        self.sparkle = [loadImage("lightbulb1.png"), loadImage("lightbulb2.png")]
        self.background = [Background, loadImage("paperbackground.jpg")]
    
    #what should be reached
    def goal(self):
        if self.Boxxy.positionX < self.goals[0][0] and self.Boxxy.positionX+50 > self.goals[0][0] and self.Boxxy.positionY < self.goals[0][1] and self.Boxxy.positionY+110 > self.goals[0][1]:
            if self.Square.positionX < self.goals[1][0] and self.Square.positionX+50 > self.goals[1][0] and self.Square.positionY < self.goals[1][1] and self.Square.positionY+110 > self.goals[1][1]:
                self.gameover = 1
                
    #rendering the image        
    def display(self):
        image(self.background[1],0,0)
        image(self.background[0], 0, 0 )
        self.Boxxy.display()
        self.Square.display()
        for x in range(2):
            if self.framecount % 50 == 13:
                self.piccount += 1
            self.framecount +=1
            image(self.sparkle[self.piccount%2],self.goals[x][0]-65, self.goals[x][1]-65, 130, 130)
       # for x in self.obstacles:
            #rect(x[0], x[2], (x[1]-x[0]), (x[3]-x[2]))
            

    def gameplay(self):
        self.Boxxy.move()
        self.Square.move()
        self.goal()
        self.display()
        


 ########
##LEVELS##
 ########


#coordinates for the walls and obstacles on each level
Obstacle1 = [[0,50,0,730],[0,1366,680,730],[1316,1366,0,730],[0,1366,0,50],[0,1366,350,380],[0,300,275,350],[1100,1366,380,455],[430,572,204,232],[545,1051,586,611]]
Obstacle2 = [[0,50,0,730],[0,1366,680,730],[1316,1366,0,730],[0,1366,0,50],[0,1366,350,380],[0,300,275,350],[1100,1366,380,455],[430,572,204,232],[545,1051,586,611]]
Obstacle3 = [[0,50,0,730],[0,1366,680,730],[1316,1366,0,730],[0,1366,0,50],[0,1366,350,380],[0,300,275,350],[1100,1366,380,455],[430,572,204,232],[545,1051,586,611]]

BoxesUp = {1: Box(1, 1000, 200, 1, Obstacle1), 2: Box(1, 1000, 200, 1, Obstacle2), 3: Box(2, 400, 400, -1, Obstacle3)}
BoxesDown ={1: Box(1, 1000, 400, -1, Obstacle1), 2: Box(1, 1000, 400, -1, Obstacle2), 3: Box(2, 400, 400, -1, Obstacle3)}


Level1 = Level(BoxesUp[1], BoxesDown[1], [[645,200],[415, 535]], Obstacle1, loadImage("level1.png"))
Level2 = Level(BoxesUp[2], BoxesDown[2], [[632,311],[415, 535]], Obstacle2, loadImage("level2.png"))

############################



def keyPressed():    
    for Boxxy in BoxesUp.values():
        if keyCode == UP and Boxxy.borderHor()=="ontop":
            Boxxy.jumpstate = 1
        if keyCode == LEFT:
            Boxxy.direction = -1    
        if keyCode == RIGHT:
            Boxxy.direction = 1
        if Boxxy.direction != 0:
            Boxxy.facing = Boxxy.direction
    for Square in BoxesDown.values():
        if keyCode == UP and Square.borderHor()=="ontop":
            Square.jumpstate = 1
        if keyCode == LEFT:
            Square.direction = -1    
        if keyCode == RIGHT:
            Square.direction = 1
        if Square.direction != 0:
            Square.facing = Square.direction
def keyReleased():    
    for Boxxy in BoxesUp.values():
        if keyCode == UP:
            Boxxy.jumpstate = 0
        if keyCode == LEFT:
            Boxxy.direction = 0
        if keyCode == RIGHT:
            Boxxy.direction = 0
    for Square in BoxesDown.values():
        if keyCode == UP:
            Square.jumpstate = 0
        if keyCode == LEFT:
            Square.direction = 0
        if keyCode == RIGHT:
            Square.direction = 0
                        


def draw():
    background(100, 100, 100)
    
    if not Level1.gameover:
        Level1.gameplay()
    
    elif not Level2.gameover:
        Level2.gameplay() 
    
    #not yet implemented 
    #elif not Level3.gameover:
    #   Level3.gameplay()  
    
    else:
        return