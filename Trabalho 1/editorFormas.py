import sys
import math
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyrr.matrix44 import *

shapes = []

class Rect(object):
    def __init__(self, points, m=create_identity()):
        self.points = points
        self.set_matrix(m)
    
    def set_point(self, i, p):
        self.points[i] = p
    
    def set_matrix(self, t):
        self.m = t
        self.invm = inverse(t)
    
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
        
        glColor3f(1, 1, 1)  # Define a cor da borda como branco
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.points[0])
        glVertex2f(self.points[1][0], self.points[0][1])
        glVertex2f(*self.points[1])
        glVertex2f(self.points[0][0], self.points[1][1])
        glEnd()
        
        glColor3f(0.5, 0.5, 0.5)  # Define a cor do preenchimento como cinza
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
    
    def contains(self, p):
        p = apply_to_vector(self.invm, [p[0], p[1], 0, 1])
        distance = math.sqrt((p[0] - self.center[0]) ** 2 + (p[1] - self.center[1]) ** 2)
        return distance <= self.radius
    
    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.m)
        
        glColor3f(1, 1, 1)  # Define a cor da borda como branco
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
        
        glColor3f(0.5, 0.5, 0.5)  # Define a cor do preenchimento como cinza
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.center)
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.center[0] + (self.radius - 1) * math.cos(theta)  # Define um raio
            y = self.center[1] + (self.radius - 1) * math.sin(theta)  # ligeiramente menor para o preenchimento
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
        self.modeConstants = ["CREATE_RECTANGLE", "CREATE_CIRCLE", "TRANSLATE", "ROTATE", "SCALE"]
        self.menu_items = ["Create Rectangle", "Create Circle", "Translate", "Rotate", "Scale"]
    
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
        elif self.mode == "SCALE":
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
            radius = math.sqrt(dx ** 2 + dy ** 2)
            self.shapes[-1].radius = radius
        elif self.mode == "TRANSLATE":
            if self.selected_shape:
                dx = x - self.last_x
                dy = y - self.last_y
                t = create_from_translation([dx, dy, 0])
                self.selected_shape.set_matrix(multiply(self.selected_shape.m, t))
                self.last_x = x
                self.last_y = y
        elif self.mode == "ROTATE":
            if self.selected_shape:
                dx = x - self.selected_shape.center[0]
                dy = y - self.selected_shape.center[1]
                angle = math.atan2(dy, dx)
                current_angle = math.atan2(self.last_y - self.selected_shape.center[1], self.last_x - self.selected_shape.center[0])
                rotation_angle = angle - current_angle
                t = create_from_axis_rotation([0, 0, 1], rotation_angle)
                self.selected_shape.set_matrix(multiply(self.selected_shape.m, t))
                self.last_x = x
                self.last_y = y
        elif self.mode == "SCALE":
            if self.selected_shape:
                dx = x - self.selected_shape.center[0]
                dy = y - self.selected_shape.center[1]
                scale_x = abs(dx) / abs(self.last_x - self.selected_shape.center[0])
                scale_y = abs(dy) / abs(self.last_y - self.selected_shape.center[1])
                t = create_from_scale([scale_x, scale_y, 1], self.selected_shape.center)
                self.selected_shape.set_matrix(multiply(self.selected_shape.m, t))
                self.last_x = x
                self.last_y = y
        
        glutPostRedisplay()

    def keyboard(self, key, x, y):
        if key == b"1":
            self.mode = "CREATE_RECTANGLE"
        elif key == b"2":
            self.mode = "CREATE_CIRCLE"
        elif key == b"3":
            self.mode = "TRANSLATE"
        elif key == b"4":
            self.mode = "ROTATE"
        elif key == b"5":
            self.mode = "SCALE"

    def create_menu(self):
        def domenu(item):
            self.mode = self.modeConstants[item]
            return 0
        
        glutCreateMenu(domenu)
        for i, name in enumerate(self.menu_items):
            glutAddMenuEntry(name, i)
        glutAttachMenu(GLUT_RIGHT_BUTTON)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for s in self.shapes:
            glColor3f(0.5, 0.5, 0.5)  # Define a cor do preenchimento como cinza
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            s.draw()
            glColor3f(1, 1, 1)  # Define a cor da borda como branco
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            s.draw()
        glutSwapBuffers()

    def run(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(800, 600)
        glutCreateWindow("Shape Editor")
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.mouse_drag)
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutReshapeFunc(self.reshape)
        self.create_menu()
        glutMainLoop()


if __name__ == "__main__":
    editor = ShapeEditor()
    editor.run()
