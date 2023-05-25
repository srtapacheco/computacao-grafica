import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import pyrr

# Variáveis globais
window_width = 800
window_height = 600
scaling = False
scale_start_x = 0
scale_start_y = 0
scale_center_x = 0
scale_center_y = 0
scale_factor_x = 1.0
scale_factor_y = 1.0
previous_scale_factor_x = 1.0
previous_scale_factor_y = 1.0
rotation_angle = 0.0
dragging = False
drag_start_x = 0
drag_start_y = 0

# Função para desenhar um losango ou retângulo
def draw_shape(x, y, width, height):
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

    # Desenha o losango ou retângulo
    glColor3f(1.0, 0.0, 0.0)  # Cor vermelha
    glTranslatef(window_width / 2, window_height / 2, 0.0)  # Translada para o centro da janela
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotaciona em relação ao eixo z
    glTranslatef(-50.0, -50.0, 0.0)  # Translada para o canto superior esquerdo da forma
    glTranslatef(50.0, 50.0, 0.0)  # Translada para o centro da forma
    glScalef(scale_factor_x, scale_factor_y, 1.0)  # Aplica a escala nos eixos X e Y
    glTranslatef(-50.0, -50.0, 0.0)  # Translada para o canto superior esquerdo da forma
    draw_shape(0, 0, 100, 100)

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


# Função para lidar com os eventos do mouse
def mouse(button, state, x, y):
    global scaling, scale_start_x, scale_start_y, scale_center_x, scale_center_y, scale_factor_x, scale_factor_y, previous_scale_factor_x, previous_scale_factor_y, dragging, drag_start_x, drag_start_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            scaling = True
            scale_start_x = x
            scale_start_y = y
            scale_center_x = window_width / 2
            scale_center_y = window_height / 2
            previous_scale_factor_x = scale_factor_x
            previous_scale_factor_y = scale_factor_y
            drag_start_x = x
            drag_start_y = y
        elif state == GLUT_UP:
            scaling = False
            dragging = False


# Função para lidar com o arraste do mouse
def mouse_motion(x, y):
    global scaling, scale_start_x, scale_start_y, scale_factor_x, scale_factor_y

    if scaling:
        dx = x - scale_start_x
        dy = y - scale_start_y

        # Calcula o fator de escala em cada eixo
        scale_speed = 0.01  # Fator de escala
        scale_factor_x = previous_scale_factor_x + (dx * scale_speed)
        scale_factor_y = previous_scale_factor_y + (dy * scale_speed)

        glutPostRedisplay()


# Função para lidar com o arraste do mouse para rotação
def mouse_motion_rotation(x, y):
    global dragging, drag_start_x, drag_start_y, rotation_angle

    if dragging:
        dx = x - drag_start_x
        dy = y - drag_start_y
        drag_start_x = x
        drag_start_y = y

        rotation_speed = 0.5  # Fator de escala para a velocidade de rotação

        rotation_angle += (dx + dy) * rotation_speed

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
    glutPassiveMotionFunc(mouse_motion_rotation)
    glutMainLoop()


if __name__ == "__main__":
    main()
