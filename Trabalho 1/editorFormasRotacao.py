import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import pyrr
import math

# Variáveis globais
window_width = 800
window_height = 600
rotation_angle = 0.0
dragging = False
drag_start_x = 0
drag_start_y = 0

# Função para desenhar um retângulo com cores diferentes em cada vértice
def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    # Vértice superior esquerdo (vermelho)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)

    # Vértice superior direito (verde)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x + width, y)

    # Vértice inferior direito (azul)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + width, y + height)

    # Vértice inferior esquerdo (amarelo)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x, y + height)

    glEnd()

# Função para desenhar a cena
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Desenha o retângulo
    glColor3f(1.0, 0.0, 0.0)  # Cor vermelha
    glTranslatef(window_width / 2, window_height / 2, 0.0)  # Translada para o centro da janela
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotaciona em relação ao eixo z
    glTranslatef(-50.0, -50.0, 0.0)  # Translada para o canto superior esquerdo do retângulo
    draw_rectangle(0, 0, 100, 100)

    glutSwapBuffers()

# Função para lidar com o redimensionamento da janela
def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, window_height, 0.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

# Função para verificar se as coordenadas (x, y) estão dentro do retângulo
def point_inside_rectangle(x, y, rect_x, rect_y, rect_width, rect_height):
    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height

# Função para lidar com os eventos do mouse
def mouse(button, state, x, y):
    global dragging, drag_start_x, drag_start_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if point_inside_rectangle(x, y, window_width / 2 - 50, window_height / 2 - 50, 100, 100):
                dragging = True
                drag_start_x = x
                drag_start_y = y
        elif state == GLUT_UP:
            dragging = False

# Função para lidar com o arraste do mouse
def mouse_motion(x, y):
    global dragging, rotation_angle, drag_start_x, drag_start_y

    if dragging:
        dx = x - drag_start_x
        dy = y - drag_start_y
        drag_start_x = x
        drag_start_y = y

        rotation_speed = 0.5  # Fator de escala para a velocidade de rotação

        rotation_angle -= dx * rotation_speed
        rotation_angle %= 360.0

        glutPostRedisplay()

# Função principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Editor de Formas Geométricas 2D")
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Cor de fundo branca
    glutDisplayFunc(draw_scene)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutMainLoop()

if __name__ == "__main__":
    main()
