from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from PIL import Image
import random

def loadTexture(filename):
    "Loads an image from a file as a texture"
    imagefile = Image.open(filename)
    sx, sy = imagefile.size[0:2]
    global pixels
    pixels = imagefile.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    image = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, image)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, sx, sy, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return image

def drawCube():
    glBegin(GL_QUADS)
    
    # Face frontal
    glNormal3f(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    
    # Face traseira
    glNormal3f(0, 0, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    
    # Face superior
    glNormal3f(0, 1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    
    # Face inferior
    glNormal3f(0, -1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    
    # Face direita
    glNormal3f(1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    
    # Face esquerda
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    
    glEnd()

def animate_cube_movement(cube):
    def animate():
        nonlocal cube
        if cube['position'][1] >= 2.0:
            cube['visible'] = False
            glutPostRedisplay()
            return
        cube['position'][1] += 0.01
        glutTimerFunc(10, animate, 0)
        glutPostRedisplay()

    glutTimerFunc(10, animate, 0)

cubes = []

def create_cubes():
    size = 0.5
    for i in range(10):
        x = random.uniform(-1.5, 1.5)
        y = random.uniform(-1.5, 1.5)
        z = random.uniform(-1.5, 1.5)
        cube = {
            'position': [x, y, z],
            'size': size,
            'texture_id': loadTexture("arrow.jpg"),
            'visible': True
        }
        cubes.append(cube)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -5)

    for cube in cubes:
        if cube['visible']:
            glPushMatrix()
            glTranslatef(cube['position'][0], cube['position'][1], cube['position'][2])
            glRotatef(-270, 1, 0, 0)  # Rotação para cima
            glBindTexture(GL_TEXTURE_2D, cube['texture_id'])
            drawCube()
            glPopMatrix()

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h, 1, 10)

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        viewport = glGetIntegerv(GL_VIEWPORT)
        winX = x
        winY = viewport[3] - y
        z = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        for cube in cubes:
            if cube['visible'] and cube['position'][0] - cube['size'] <= winX <= cube['position'][0] + cube['size'] and \
                    cube['position'][1] - cube['size'] <= winY <= cube['position'][1] + cube['size']:
                animate_cube_movement(cube)

width, height = 500, 500

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100.0)
    glEnable(GL_TEXTURE_2D)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(width, height)
glutCreateWindow("Textured Cube")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
init()
create_cubes()
glutMainLoop()
