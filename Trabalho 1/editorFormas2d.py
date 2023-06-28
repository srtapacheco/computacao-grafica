import sys
import math
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *
from pyrr.matrix44 import create_from_translation as translate, inverse

shapes = []

class Rect(object):
    def __init__(self, points, m=create_identity()):
        self.points = points
        self.set_matrix(m)
        self.calculate_center()
        self.rotation = 0.0  # Add rotation property

    def set_point(self, i, p):
        self.points[i] = p

    def set_matrix(self, t):
        self.m = t
        determinant = np.linalg.det(t)
        if determinant == 0:
            # Handle the case of a singular matrix here
            return
        self.invm = np.linalg.inv(t)

    def calculate_center(self):
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        self.center = [(x1 + x2) / 2, (y1 + y2) / 2]

    def contains(self, p):
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1])
        xmin = min(self.points[0][0], self.points[1][0])
        xmax = max(self.points[0][0], self.points[1][0])
        ymin = min(self.points[0][1], self.points[1][1])
        ymax = max(self.points[0][1], self.points[1][1])
        return xmin <= p[0] <= xmax and ymin <= p[1] <= ymax

    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.m)

        glTranslatef(self.center[0], self.center[1], 0)  # Translate to the center of the rectangle
        glRotatef(self.rotation, 0, 0, 1)  # Apply rotation around the Z-axis
        glTranslatef(-self.center[0], -self.center[1], 0)  # Translate back to the original position

        glColor3f(1, 1, 1)  # Set the border color to white
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.points[0])
        glVertex2f(self.points[1][0], self.points[0][1])
        glVertex2f(*self.points[1])
        glVertex2f(self.points[0][0], self.points[1][1])
        glEnd()

        glColor3f(0.5, 0.5, 0.5)  # Set the fill color to gray
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.points[0])
        glVertex2f(self.points[1][0], self.points[0][1])
        glVertex2f(*self.points[1])
        glVertex2f(self.points[0][0], self.points[1][1])
        glEnd()

        glPopMatrix()

class Circle(object):
    def __init__(self, center, radius, m=create_identity()):
        self.center = center
        self.radius = radius
        self.set_matrix(m)

    def set_matrix(self, t):
        self.m = t
        self.invm = inverse(t)

    def calculate_center(self):
    # O círculo já possui o centro definido, então não é necessário calcular novamente
        pass

    def contains(self, p):
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1])
        distance = math.sqrt((p[0] - self.center[0]) ** 2 + (p[1] - self.center[1]) ** 2)
        return distance <= self.radius

    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.m)

        glColor3f(1, 1, 1)  # Set the border color to white
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        num_segments = 100
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.center)
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.center[0] + self.radius * math.cos(theta)
            y = self.center[1] + self.radius * math.sin(theta)
            glVertex2f(x, y)
        glEnd()

        glColor3f(0.5, 0.5, 0.5)  # Set the fill color to gray
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.center)
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.center[0] + (self.radius - 1) * math.cos(theta)  # Define a slightly smaller radius for the fill
            y = self.center[1] + (self.radius - 1) * math.sin(theta)  # color
            glVertex2f(x, y)
        glEnd()

        glPopMatrix()



class ShapeEditor(object):
    def __init__(self):
        self.mode = "CREATE_RECTANGLE"
        self.shapes = []
        self.selected_shape = None
        self.last_x = 0
        self.last_y = 0
        self.modeConstants = ["CREATE_RECTANGLE", "CREATE_CIRCLE", "TRANSLATE", "ROTATE"]
        self.menu_items = ["Create Rectangle", "Create Circle", "Translate", "Rotate"]
        self.rotation_angle = 0.0

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)

    def mouse(self, button, state, x, y):
        if state != GLUT_DOWN:
            return

        if self.mode == "CREATE_RECTANGLE":
            self.shapes.append(Rect([[x, y], [x, y]]))
        elif self.mode == "CREATE_CIRCLE":
            self.shapes.append(Circle([x, y], 0))
        elif self.mode == "TRANSLATE":
            self.selected_shape = None
            for s in self.shapes:
                if s.contains([x, y]):
                    self.selected_shape = s
                    self.last_x = x
                    self.last_y = y
                    break
        elif self.mode == "ROTATE":
            self.selected_shape = None
            for s in self.shapes:
                if s.contains([x, y]):
                    self.selected_shape = s
                    self.last_x = x
                    self.last_y = y
                    break

    def mouse_drag(self, x, y):
        if self.mode == "CREATE_RECTANGLE":
            self.shapes[-1].set_point(1, [x, y])
        elif self.mode == "CREATE_CIRCLE":
            dx = x - self.shapes[-1].center[0]
            dy = y - self.shapes[-1].center[1]
            self.shapes[-1].radius = math.sqrt(dx ** 2 + dy ** 2)
        if self.mode == "TRANSLATE":
            if self.selected_shape:
                dx = x - self.last_x
                dy = y - self.last_y
                translation_matrix = create_from_translation([dx, dy, 0])
                self.selected_shape.set_matrix(np.matmul(self.selected_shape.m, translation_matrix))
                self.selected_shape.calculate_center()
                self.last_x = x
                self.last_y = y
        elif self.mode == "ROTATE":
            if self.selected_shape:
                dx = x - self.selected_shape.center[0]
                dy = y - self.selected_shape.center[1]
                angle = math.degrees(math.atan2(dy, dx))
                self.rotation_angle = angle
                self.selected_shape.rotation = self.rotation_angle
                self.selected_shape.calculate_center()

        glutPostRedisplay()


    def menu_select(self, value):
        self.mode = self.modeConstants[value]
        glutPostRedisplay()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        for s in self.shapes:
            s.draw()

        glFlush()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Shape Editor")

    shape_editor = ShapeEditor()

    glutReshapeFunc(shape_editor.reshape)
    glutMouseFunc(shape_editor.mouse)
    glutMotionFunc(shape_editor.mouse_drag)
    glutDisplayFunc(shape_editor.draw)

    glutCreateMenu(shape_editor.menu_select)
    for i, item in enumerate(shape_editor.menu_items):
        glutAddMenuEntry(item, i)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    glClearColor(0, 0, 0, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
