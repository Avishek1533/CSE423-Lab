# Task 1:

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height= 800,800 #Window

speed= 0.4
direction=0.0  #Direction(degree)
angle=0.0  #Angle in radians
colour=1.0
bg_colour=0.0 #Background

class rain:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.length= random.randint(10,30)
        self.speed= random.uniform(0.5,1.5)


raindrop= [rain(random.uniform(-200,200), random.uniform(-200,200)) for i in range(100)]

def drawRain():
    global raindrop, colour, angle
    for temp in raindrop:
        glBegin(GL_LINES)
        glColor3f(colour,colour,colour)
        glVertex2f(temp.x,temp.y)
        glVertex2f(temp.x - math.sin(angle)*temp.length, temp.y - math.cos(angle)*temp.length)
        glEnd()


def specialKeyListener(key, x,y):
    global speed, colour, direction, bg_colour, angle
    if key == GLUT_KEY_UP:
        speed*=2
    if key == GLUT_KEY_DOWN:
        speed/=2
    if key == GLUT_KEY_RIGHT:
        direction -= 10  # Increase direction angle
        angle = math.radians(direction)
    if key == GLUT_KEY_LEFT:
        direction += 10  # Decrease direction angle
        angle = math.radians(direction)
    if key == GLUT_KEY_PAGE_UP:
        bg_colour += .1
        colour -= .1
    if key == GLUT_KEY_PAGE_DOWN:
        colour += .1
        bg_colour -= .1

    glutPostRedisplay()




#House

def House():
    #Shed
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.5, 0.0) #Orange
    glVertex2d(0,120)
    glVertex2d(-120,0)
    glVertex2d(120,0)
    glEnd()

    #Wall
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)  # Blue
    glVertex3d(-110, 0, 0)
    glVertex3d(-110, -130, 0)
    glVertex3d(110, -130, 0)
    glVertex3d(110, 0, 0)
    glEnd()

    # Door
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)  # Yellow 
    glVertex3d(-50, -60, 0)
    glVertex3d(-50, -130, 0)
    glVertex3d(-10, -130, 0)
    glVertex3d(-10, -60, 0)
    glEnd()

    # Window 
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)  # Yellow 
    glVertex3d(20, -50, 0)
    glVertex3d(20, -20, 0)
    glVertex3d(50, -20, 0)
    glVertex3d(50, -50, 0)
    glEnd()

    # cross inside the window
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)  # Black 
    glVertex3d(35, -50, 0)
    glVertex3d(35, -20, 0)
    glVertex3d(20, -35, 0)
    glVertex3d(50, -35, 0)
    glEnd()

    # lock to the door
    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)  # Black
    glVertex3d(-45, -95, 0)
    glEnd()


def display():
    global colour 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(bg_colour, bg_colour, bg_colour, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    House()
    drawRain()
    glutSwapBuffers()


def animate():
    glutPostRedisplay()
    global raindrop, speed, angle
    for temp in raindrop:
        temp.y -= math.cos(angle) * temp.speed * speed
        temp.x -= math.sin(angle) * temp.speed * speed
        if temp.y + temp.length < -100 or temp.x < -200 or temp.x > 200:
            temp.y = random.uniform(100, 200)
            temp.x = random.uniform(-200, 200)
            temp.z = random.uniform(10, 50)  # Reset z-coordinate for depth
            temp.length = random.randint(10, 30)
            temp.speed = random.uniform(0.5, 1.5)
            
def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)  # Enable depth perception

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # Enable depth buffer

window = glutCreateWindow(b"TASK 1: Building A House in Rainfall")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutSpecialFunc(specialKeyListener)

glutMainLoop()



