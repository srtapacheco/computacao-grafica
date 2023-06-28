import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import random

# Selected object
selected = None

# Set of removed objects
removed = set()

# size of cube array
n = 3

# rotation angle
angle = 0

# Variables for mouse dragging
is_dragging = False
prev_x = 0
prev_y = 0

def loadTexture(filename):
    # Carrega uma imagem de arquivo como uma textura
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

def draw_scene(flatColors = False):
    "Draws the scene emitting a 'name' for each cube"
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0,0,-3)
    glRotatef (-80, 1,0,0)
    glRotatef (angle,0,1,1)
    size = 1/n
    for i in range(n):
        x = i - (n-1)/2 
        for j in range(n):
            y = j - (n-1)/2 
            for k in range(n):
                z = k - (n-1)/2 
                name = (i*n + j) * n + k
                if flatColors:
                    glColor3f((i+1)/n, (j+1)/n, (k+1)/n)
                # Ignore removed objects
                if name in removed: 
                    continue 
                glLoadName(name)
                glPushMatrix()
                glTranslatef(x*size,y*size,z*size)
                glutSolidCube(size*0.8)
                glPopMatrix()
            
def display():
    draw_scene();
    glutSwapBuffers ()

def init ():
    glClearColor (0.0, 0.0, 0.0, 0.0);
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLight(GL_LIGHT0, GL_POSITION, [.5,.2,1,0])
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [0.2,0.2,0.2,1])
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    # Helps with antialiasing
    glEnable(GL_MULTISAMPLE)

    # Inicializa a texturização
    global textureId
    textureId = loadTexture("arrow.jpg")
    glEnable(GL_TEXTURE_2D)


def reshape(width,height):
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity()
    global projectionArgs, windowSize
    windowSize = width,height
    projectionArgs = 50, width/height, 0.1,20
    gluPerspective (*projectionArgs)
    glViewport (0,0,width,height)
 
def pick(x,y):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)  # Desativa a texturização temporariamente
    draw_scene(True)
    glFlush()
    glEnable (GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)  # Reativa a texturização
    buf = glReadPixels (x,windowSize[1]-y,1,1,GL_RGB,GL_FLOAT)
    pixel = buf[0][0]
    r,g,b = pixel
    i,j,k = int(r*n-1),int(g*n-1),int(b*n-1)
    if i >= 0: return (i*n + j) * n + k
    return -1 

def mousePressed(button,state,x,y):
    global selected, is_dragging, prev_x, prev_y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            is_dragging = True
            prev_x, prev_y = x, y
        elif state == GLUT_UP:
            is_dragging = False
    if state == GLUT_DOWN:
        selected = pick(x, y)
        if selected >= 0:
            removed.add(selected)
    glutPostRedisplay()

def mouseMoved(x, y):
    global angle, prev_x, prev_y
    if is_dragging:
        delta_x = x - prev_x
        delta_y = y - prev_y
        angle += delta_x * 0.1
        prev_x = x
        prev_y = y
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize (400, 400); 
    glutInitWindowPosition (100, 100)
    glutCreateWindow ("picking")
    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMouseFunc(mousePressed)
    glutMotionFunc(mouseMoved)
    glutMainLoop()

main()
