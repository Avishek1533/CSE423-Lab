# Task 2:
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


WIDTH, HEIGHT = 800, 600 #Window


points = []  # List to store points
speed_multiplier = 0.7  
freeze = False  


def draw_point(x, y, color):
    glColor3f(*color)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_box():
    #Boundary box
    glColor3f(1.0, 1.0, 1.0)  # White 
    glLineWidth(6)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, -1.0)
    glVertex2f(1.0, 1.0)
    glVertex2f(-1.0, 1.0)
    glEnd()


def update_points():
    global points
    for i in points:
        if not freeze:
            i[0] += i[3] * i[5] * speed_multiplier  # x += direction_x * speed
            i[1] += i[4] * i[5] * speed_multiplier  # y += direction_y * speed

            # Bounce off the walls
            if i[0] <= -1.0 or i[0] >= 1.0:
                i[3] *= -1  # Reverse x direction
            if i[1] <= -1.0 or i[1] >= 1.0:
                i[4] *= -1  # Reverse y direction


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw_box()  # Draw the boundary box

    # Draw all points
    for i in points:
        if i[6]:  # Only draw if visible
            draw_point(i[0], i[1], i[2])

    glutSwapBuffers()


def mouse(button, state, x, y):
    global points
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x_norm = (x / WIDTH) * 2 - 1
        y_norm = -((y / HEIGHT) * 2 - 1)

        # Generate a random color and direction
        color = (random.random(), random.random(), random.random())
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])
        speed = random.uniform(0.01, 0.05)

        points.append([x_norm, y_norm, color, direction_x, direction_y, speed, True])

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        #Blink
        for point in points:
            point[6] = not point[6]

    glutPostRedisplay()


def keyboard(key, x, y):
    global speed_multiplier, freeze
    if key == b' ':
        freeze = not freeze  
    elif key == GLUT_KEY_UP:
        speed_multiplier *= 1.4  # Increase speed
    elif key == GLUT_KEY_DOWN:
        speed_multiplier /= 1.4  # Decrease speed

    glutPostRedisplay()


def animate():
    update_points()
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)  # 2D orthogonal projection
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Task 2:BUilding The Amazing Box")
    init()

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)

    glutMainLoop()

if __name__ == "__main__":
    main()


    