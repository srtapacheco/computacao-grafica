

import sys
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import random

# Objeto selecionado
selected = None

# Conjunto de objetos removidos
removed = set()

# Tamanho do array de cubos
n = 3

# Ângulos de rotação
angle_x = 0
angle_y = 0

# Variáveis para arrastar o mouse
is_dragging = False
prev_x = 0
prev_y = 0

# Largura e altura da tela
width, height = 500, 500

# Caminho da imagem de vitória
win_image_path = "youwin.png"
win_image = None

# Direção da ejeção
ejection_direction = [0, 0, 0]

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

def load_image(path):
    # Carrega uma imagem a partir de um arquivo e retorna os dados da imagem
    image = Image.open(path)
    image_data = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    return image.size[0], image.size[1], image_data

def draw_image(image_width, image_height, image_data):
    # Desenha uma imagem na tela
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)  # Desativa o teste de profundidade
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)  # Define uma projeção ortográfica 2D
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Cria uma textura temporária
    temp_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, temp_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # Desenha um quadrilátero com a textura
    glColor3f(1.0, 1.0, 1.0)  # Define a cor como branco
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2i(0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex2i(0, image_height)
    glTexCoord2f(1.0, 1.0)
    glVertex2i(image_width, image_height)
    glTexCoord2f(1.0, 0.0)
    glVertex2i(image_width, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Limpa a textura temporária
    glDeleteTextures(1, [temp_texture])

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)  # Reativa o teste de profundidade

def draw_cube(size, texture_id):
    # Desenha um cubo com textura
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)  # Começa a desenhar o cubo

    # Face frontal
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, -size, size)  # Canto inferior esquerdo
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, -size, size)  # Canto inferior direito
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, size, size)  # Canto superior direito
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, size, size)  # Canto superior esquerdo

    # Face traseira
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-size, -size, -size)  # Canto inferior direito
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-size, size, -size)  # Canto superior direito
    glTexCoord2f(0.0, 1.0)
    glVertex3f(size, size, -size)  # Canto superior esquerdo
    glTexCoord2f(0.0, 0.0)
    glVertex3f(size, -size, -size)  # Canto inferior esquerdo

    # Face superior #Branco
    glTexCoord2f(0.75, 1.0)    # Canto superior esquerdo da região
    glVertex3f(-size, size, -size)  # Canto superior esquerdo
    glTexCoord2f(0.75, 0.75)   # Canto inferior esquerdo da região
    glVertex3f(-size, size, size)  # Canto inferior esquerdo
    glTexCoord2f(1.0, 0.75)    # Canto inferior direito da região
    glVertex3f(size, size, size)  # Canto inferior direito
    glTexCoord2f(1.0, 1.0)     # Canto superior direito da região
    glVertex3f(size, size, -size)  # Canto superior direito

    # Face inferior # Azul
    glTexCoord2f(0.30, 0.10)
    glVertex3f(-size, -size, -size)  # Canto superior direito
    glTexCoord2f(0.30, 0.10)
    glVertex3f(size, -size, -size)  # Canto superior esquerdo
    glTexCoord2f(0.30, 0.10)
    glVertex3f(size, -size, size)  # Canto inferior esquerdo
    glTexCoord2f(0.30, 0.10)
    glVertex3f(-size, -size, size)  # Canto inferior direito

    # Face direita
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, -size, -size)  # Canto inferior direito
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, size, -size)  # Canto superior direito
    glTexCoord2f(0.0, 1.0)
    glVertex3f(size, size, size)  # Canto superior esquerdo
    glTexCoord2f(0.0, 0.0)
    glVertex3f(size, -size, size)  # Canto inferior esquerdo

    # Face esquerda
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, -size, -size)  # Canto inferior esquerdo
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-size, -size, size)  # Canto inferior direito
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-size, size, size)  # Canto superior direito
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, size, -size)  # Canto superior esquerdo

    glEnd()  # Finaliza o desenho do cubo

def generate_rotation_angles():
    # Gera ângulos de rotação aleatórios para cada cubo
    rotation_axes = [['x' if random.random() < 0.5 else 'y' for _ in range(n)] for _ in range(n)]
    rotation_angles = [[[random.choice([0, 90, 180, 270]) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    return rotation_angles, rotation_axes

rotation_angles, rotation_axes = generate_rotation_angles()  # Gera novos ângulos de rotação e eixos


def draw_scene(flatColors=False):
    # Desenha a cena, emitindo um 'nome' para cada cubo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -3)
    glRotatef(-80, 1, 0, 0)
    glRotatef(angle_x, 1, 0, 0)  # Rotação em torno do eixo X (vertical)
    glRotatef(angle_y, 0, 1, 0)  # Rotação em torno do eixo Y (horizontal)
    size = 1 / n
    for i in range(n):
        x = i - (n - 1) / 2
        for j in range(n):
            y = j - (n - 1) / 2
            for k in range(n):
                z = k - (n - 1) / 2
                name = (i * n + j) * n + k
                if flatColors:
                    glColor3f((i + 1) / n, (j + 1) / n, (k + 1) / n)
                # Ignora objetos removidos
                if name in removed:
                    continue
                glLoadName(name)
                glPushMatrix()
                glTranslatef(x * size, y * size, z * size)
                if rotation_axes[i][j] == 'x':
                    glRotatef(rotation_angles[i][j][k], 1, 0, 0)  # Aplica a rotação específica do cubo no eixo X
                else:
                    glRotatef(rotation_angles[i][j][k], 0, 0, 1)  # Aplica a rotação específica do cubo no eixo Y
                draw_cube(size * 0.4, textureId)
                glPopMatrix()

    if len(removed) == n * n * n:
        draw_image(win_image[0], win_image[1], win_image[2])

def display():
    # Função de callback para exibição da cena
    draw_scene()
    glutSwapBuffers()

def init():
    # Inicializa o ambiente gráfico
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLight(GL_LIGHT0, GL_POSITION, [.5, .2, 1, 0])
    glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, [0.2, 0.2, 0.2, 1])
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    # Auxilia na suavização de bordas
    glEnable(GL_MULTISAMPLE)

    # Carrega a imagem de vitória
    global win_image
    win_image = load_image(win_image_path)

    # Inicializa a texturização
    global textureId
    textureId = loadTexture("arrow2.jpg")
    glEnable(GL_TEXTURE_2D)

def reshape(width, height):
    # Função de callback para redimensionamento da janela
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    global projectionArgs, windowSize
    windowSize = width,height
    projectionArgs = 50, width / height, 0.1, 20
    gluPerspective(*projectionArgs)
    glViewport(0, 0, width, height)

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
    if i >= 0: 
        return (i*n + j) * n + k
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
    # Função de callback para movimento do mouse
    global angle_x, angle_y, prev_x, prev_y
    if is_dragging:
        delta_x = x - prev_x
        delta_y = y - prev_y
        angle_x += delta_y * 0.5  # Rotação em torno do eixo X (vertical)
        angle_y += delta_x * 0.5  # Rotação em torno do eixo Y (horizontal)
        prev_x = x
        prev_y = y
    glutPostRedisplay()

def idle():
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Tap Away 3D")
    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutMouseFunc(mousePressed)
    glutMotionFunc(mouseMoved)
    glutMainLoop()

main()