# ComputacaoGrafica
3o Trabalho: Demo B-Splines

Sua tarefa é implementar uma demonstração de curvas B-Spline seguindo as linhas gerais do notebook B-splines[https://observablehq.com/@esperanc/b-splines] mostrado em aula. Em particular, você deve desenhar B-splines uniformes de grau entre 0 e 5. Use o mouse para movimentar 6 pontos de controle numa tela bi-dimensional. Use o teclado para aumentar o diminuir o grau: tecla "d" diminui o grau e tecla "D" aumenta o grau. O código do notebook pode ser usado como referência, mas sua implementação deve usar OpenGL. 

Dicas:

Use os seguintes comandos OpenGL para obter pontos "redondos":
glPointSize(tamanho)
glEnable (GL_POINT_SMOOTH)
glEnable (GL_BLEND) 
glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
Use glutBitmapCharacter() para desenhar as legendas dos pontos de controle.
O código do notebook é um tanto ineficiente. Você pode fazer melhor! Em particular, nem todas as funções de base precisam ser computadas para todos os pontos plotados. 

