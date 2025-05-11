
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import random
import time
import math


window_width = 800
window_height = 600
catcher_width = 80
catcher_height = 30
diamond_size = 15
score = 0
game_over = False
game_paused = False
delta_time = 0
last_frame_time = 0


button_size = 30
button_margin = 20
button_y = window_height - button_size - 10


diamond_x = 0
diamond_y = 0
diamond_speed = 100  
diamond_acceleration = 5  
diamond_color = [1.0, 1.0, 1.0] 
diamond_active = False


catcher_x = window_width // 2
catcher_y = 50
catcher_speed = 300  
catcher_color = [1.0, 1.0, 1.0]  # White

class AABB:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def has_collided(box1, box2):
    return (box1.x < box2.x + box2.width and
            box1.x + box1.width > box2.x and
            box1.y < box2.y + box2.height and
            box1.y + box1.height > box2.y)

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx >= 0 and dy < 0
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  # dx >= 0 and dy < 0
            return 6

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_line(x1, y1, x2, y2):
    # left to right for zone calculation
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    zone = find_zone(x1, y1, x2, y2)
    
    # Convert endpoints to zone 0
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    
    
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    
    GL.glBegin(GL.GL_POINTS)
    
    
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1_z0
    
    for x in range(x1_z0, x2_z0 + 1):
        # Convert point back to original zone 
        orig_x, orig_y = convert_from_zone0(x, y, zone)
        GL.glVertex2f(orig_x, orig_y)
        
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
    
    GL.glEnd()

def spawn_diamond():
    global diamond_x, diamond_y, diamond_active, diamond_color
    
    diamond_x = random.randint(diamond_size, window_width - diamond_size)
    diamond_y = window_height
    diamond_active = True
    

    r = random.uniform(0.5, 1.0)
    g = random.uniform(0.5, 1.0)
    b = random.uniform(0.5, 1.0)
    diamond_color = [r, g, b]

def draw_diamond(x, y, size, color):
    GL.glColor3f(color[0], color[1], color[2])
    
    
    half_size = size // 2
    
    # Top to right
    draw_line(x, y + half_size, x + half_size, y)
    # Right to bottom
    draw_line(x + half_size, y, x, y - half_size)
    # Bottom to left
    draw_line(x, y - half_size, x - half_size, y)
    # Left to top
    draw_line(x - half_size, y, x, y + half_size)

def draw_catcher(x, y, width, height, color):
    GL.glColor3f(color[0], color[1], color[2])
    
    
    half_width = width // 2
    
    # Left to bottom-left
    draw_line(x - half_width, y, x - half_width + width // 4, y - height)
    # Bottom-left to bottom-right
    draw_line(x - half_width + width // 4, y - height, x + half_width - width // 4, y - height)
    # Bottom-right to right
    draw_line(x + half_width - width // 4, y - height, x + half_width, y)
    # Right to left 
    draw_line(x + half_width, y, x - half_width, y)

def draw_restart_button():
    GL.glColor3f(0.0, 0.8, 0.8)  

    button_x = button_margin + button_size // 2
    

    draw_line(button_x + button_size // 4, button_y + button_size // 4, 
              button_x + button_size // 4, button_y + 3 * button_size // 4)
    

    draw_line(button_x - button_size // 4, button_y + button_size // 2, 
              button_x + button_size // 4, button_y + 3 * button_size // 4)
    draw_line(button_x - button_size // 4, button_y + button_size // 2, 
              button_x + button_size // 4, button_y + button_size // 4)

def draw_play_pause_button():
    button_x = window_width // 2
    
    GL.glColor3f(1.0, 0.75, 0.0)  
    
    if game_paused:
        draw_line(button_x - button_size // 4, button_y + button_size // 4, 
                 button_x - button_size // 4, button_y + 3 * button_size // 4)
        draw_line(button_x - button_size // 4, button_y + button_size // 4, 
                 button_x + button_size // 4, button_y + button_size // 2)
        draw_line(button_x + button_size // 4, button_y + button_size // 2, 
                 button_x - button_size // 4, button_y + 3 * button_size // 4)
    else:
        # Draw pause 
        draw_line(button_x - button_size // 4, button_y + button_size // 4, 
                 button_x - button_size // 4, button_y + 3 * button_size // 4)
        draw_line(button_x + button_size // 4, button_y + button_size // 4, 
                 button_x + button_size // 4, button_y + 3 * button_size // 4)

def draw_exit_button():
    GL.glColor3f(1.0, 0.0, 0.0)  # Red
    
    button_x = window_width - button_margin - button_size // 2
    
    # Draw X shape
    draw_line(button_x - button_size // 4, button_y + button_size // 4, 
             button_x + button_size // 4, button_y + 3 * button_size // 4)
    draw_line(button_x - button_size // 4, button_y + 3 * button_size // 4, 
             button_x + button_size // 4, button_y + button_size // 4)

def reset_game():
    global score, game_over, game_paused, diamond_speed, catcher_color
    
    score = 0
    game_over = False
    game_paused = False
    diamond_speed = 100
    catcher_color = [1.0, 1.0, 1.0]  
    

    spawn_diamond()
    
    print("Starting Over")

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    
    if game_paused:
        print("Game Paused")
    else:
        print("Game Resumed")

def exit_game():
    print(f"Goodbye! Your final score: {score}")
    GLUT.glutLeaveMainLoop()

def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    
    
    if diamond_active:
        draw_diamond(diamond_x, diamond_y, diamond_size, diamond_color)
    
    
    draw_catcher(catcher_x, catcher_y, catcher_width, catcher_height, catcher_color)
    
    
    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()
    
    GLUT.glutSwapBuffers()

def update(value):
    global diamond_y, diamond_active, score, game_over, catcher_color
    global diamond_speed, delta_time, last_frame_time
    
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time
    
    if not game_over and not game_paused:
        # Only move diamond if game is active
        if diamond_active:
            diamond_y -= diamond_speed * delta_time
            
            diamond_box = AABB(diamond_x - diamond_size // 2, diamond_y - diamond_size // 2, 
                              diamond_size, diamond_size)
            catcher_box = AABB(catcher_x - catcher_width // 2, catcher_y - catcher_height, 
                              catcher_width, catcher_height)
            
            if has_collided(diamond_box, catcher_box):
                score += 1
                print(f"Score: {score}")
                diamond_active = False
                # Increase diamond speed
                diamond_speed += diamond_acceleration
            
                spawn_diamond()
            
            
            elif diamond_y - diamond_size // 2 <= 0:
                game_over = True
                diamond_active = False
                catcher_color = [1.0, 0.0, 0.0]  # Turn catcher red
                print(f"Game Over! Final score: {score}")
        else:
        
            spawn_diamond()
    
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(16, update, 0)  

def keyboard(key, x, y):
    global catcher_x, delta_time
    
    if not game_over and not game_paused:
        speed = int(catcher_speed * delta_time)
        
        # Move catcher left
        if key == GLUT.GLUT_KEY_LEFT:
            catcher_x = max(catcher_width // 2, catcher_x - speed)
        
        # Move catcher right
        elif key == GLUT.GLUT_KEY_RIGHT:
            catcher_x = min(window_width - catcher_width // 2, catcher_x + speed)
    
    GLUT.glutPostRedisplay()

def mouse_click(button, state, x, y):
    if button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN:
        y = window_height - y
        
        if (button_margin <= x <= button_margin + button_size and 
            button_y <= y <= button_y + button_size):
            reset_game()
        
        elif (window_width // 2 - button_size // 2 <= x <= window_width // 2 + button_size // 2 and 
              button_y <= y <= button_y + button_size):
            toggle_pause()
        
        elif (window_width - button_margin - button_size <= x <= window_width - button_margin and 
              button_y <= y <= button_y + button_size):
            exit_game()

def init():
    GL.glClearColor(0.0, 0.0, 0.1, 1.0)  # Dark blue background
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, window_width, 0, window_height, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GL.glPointSize(1.0)

def main():
    global last_frame_time
    
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(window_width, window_height)
    GLUT.glutCreateWindow(b"Catch the Diamonds!")
    
    init()
    GLUT.glutDisplayFunc(display)
    GLUT.glutSpecialFunc(keyboard)
    GLUT.glutMouseFunc(mouse_click)
    
    last_frame_time = time.time()
    reset_game()  
    
    GLUT.glutTimerFunc(16, update, 0)  
    GLUT.glutMainLoop()

if __name__ == "__main__":
    main()