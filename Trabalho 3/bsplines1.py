import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

window_width = 800
window_height = 600
degree = 3  # Initial degree
control_points = np.zeros((6, 2))  # Array to store control points

# Set initial control points
control_points[0] = [100, 446.99128263114306]
control_points[1] = [220, 415.8660901426639]
control_points[2] = [340, 417.2893298502736]
control_points[3] = [460, 115.47194365537226]
control_points[4] = [580, 407.7135285679133]
control_points[5] = [700, 160.53058364604104]

# Function to draw the B-Spline curve
def draw_curve():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(0.0, 0.0, 0.0)  # Black color

    # Draw control points as circles
    for point in control_points:
        x, y = point
        glPushMatrix()
        glTranslatef(x, y, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for angle in range(0, 360, 10):
            rad = np.deg2rad(angle)
            glVertex2f(5 * np.cos(rad), 5 * np.sin(rad))
        glEnd()
        glPopMatrix()

    glColor3f(1.0, 0.0, 0.0)  # Red color

    # Sample the B-Spline curve
    t = np.linspace(degree, len(control_points), 1000)
    curve = np.zeros((len(t), 2))
    for i, u in enumerate(t):
        sum_x = 0.0
        sum_y = 0.0
        for j in range(len(control_points)):
            basis = basis_function(j, degree, u)
            sum_x += basis * control_points[j][0]
            sum_y += basis * control_points[j][1]
        curve[i] = [sum_x, sum_y]

    # Draw the B-Spline curve
    glBegin(GL_LINE_STRIP)
    for point in curve:
        glVertex2f(point[0], point[1])
    glEnd()

    glutSwapBuffers()

# Function to compute the basis function
def basis_function(i, d, u):
    if d == 0:
        if u >= i and u < i + 1:
            return 1.0
        else:
            return 0.0
    else:
        left = (u - i) / d * basis_function(i, d-1, u)
        right = (i + d + 1 - u) / d * basis_function(i+1, d-1, u)
        return left + right

# Function to handle mouse events
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert mouse coordinates to OpenGL coordinates
        opengl_x = x
        opengl_y = window_height - y

        # Find the closest control point and update its position
        min_distance = float('inf')
        closest_index = -1
        for i, point in enumerate(control_points):
            distance = np.linalg.norm(point - np.array([opengl_x, opengl_y]))
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        control_points[closest_index] = [opengl_x, opengl_y]

        glutPostRedisplay()

# Function to handle keyboard events
def keyboard(key, x, y):
    global degree
    if key == b'd':
        if degree > 0:
            degree -= 1
    elif key == b'D':
        degree += 1
    glutPostRedisplay()

# Function to handle window resizing
def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("B-Splines Demo")
    glClearColor(1.0, 1.0, 1.0, 1.0)  # White background color
    glPointSize(10.0)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glutDisplayFunc(draw_curve)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
