import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

window_width = 800
window_height = 600
degree = 1  # Grau inicial
control_points = np.zeros((6, 2))  # Array para armazenar os pontos de controle
selected_point = None  # Ponto de controle selecionado para movimento

# Definir os pontos de controle iniciais
control_points[0] = [100, 446.99128263114306]
control_points[1] = [220, 415.8660901426639]
control_points[2] = [340, 417.2893298502736]
control_points[3] = [460, 115.47194365537226]
control_points[4] = [580, 407.7135285679133]
control_points[5] = [700, 160.53058364604104]

# Função para desenhar a B-Spline
def draw_curve():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(0.0, 0.0, 0.0)  # Cor preta

    # Desenhar os pontos de controle como círculos e seus números
    for i, point in enumerate(control_points):
        x, y = point
        glPushMatrix()
        glTranslatef(x, y, 0.0)
        glBegin(GL_TRIANGLE_FAN)
        for angle in range(0, 360, 10):
            rad = np.deg2rad(angle)
            glVertex2f(5 * np.cos(rad), 5 * np.sin(rad))
        glEnd()
        glPopMatrix()
        # Desenhar o número do ponto de controle com espaçamento adicional
        draw_text(x + 10, y - 10, str(i))

    if 0 < degree <= 5:
        glColor3f(1.0, 0.0, 0.0)  # Cor vermelha

        # Amostrar a B-Spline
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

        # Desenhar a B-Spline
        glBegin(GL_LINE_STRIP)
        for point in curve:
            glVertex2f(point[0], point[1])
        glEnd()

    glutSwapBuffers()

# Função para calcular a função de base
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

# Função para desenhar texto com espaçamento adicional
def draw_text(x, y, text):
    offset = 10  # Espaçamento adicional
    glRasterPos2f(x + offset, y)  # Ajuste a posição do texto para adicionar o espaçamento
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(character))


# Função para lidar com eventos do mouse
def mouse(button, state, x, y):
    global selected_point
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Converter as coordenadas do mouse para coordenadas OpenGL
            opengl_x = x
            opengl_y = window_height - y

            # Verificar se algum ponto de controle foi selecionado para movimento
            for i, point in enumerate(control_points):
                distance = np.linalg.norm(point - np.array([opengl_x, opengl_y]))
                if distance < 5:
                    selected_point = i
                    break
        elif state == GLUT_UP:
            selected_point = None

# Função para lidar com o movimento do mouse
def motion(x, y):
    if selected_point is not None:
        # Converter as coordenadas do mouse para coordenadas OpenGL
        opengl_x = x
        opengl_y = window_height - y

        # Atualizar a posição do ponto de controle selecionado
        control_points[selected_point] = [opengl_x, opengl_y]

    glutPostRedisplay()

# Função para lidar com eventos do teclado
def keyboard(key, x, y):
    global degree
    if key == b'd':
        if 0 < degree <= 5:
            degree -= 1
    elif key == b'D':
        if 0 <= degree < 5:
            degree += 1
    glutPostRedisplay()

# Função para lidar com redimensionamento da janela
def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# Função principal
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Demo B-Splines")
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Cor de fundo branca
    glPointSize(10.0)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glutDisplayFunc(draw_curve)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
