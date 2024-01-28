import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 8, 15
TILE = 45
GAME_RES = W * TILE, H * TILE   #Tamaño ventana del grid
RES = 750, 700  #Tamaño ventana
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]    #Se crean Rectangulos con distintas coordenadas
                                                                                            # For's anidados

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],      #Aca estan las 7 figuras: l, o, s, L, T, J, z
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]   #Asigna coordenada a cada cubo para formar la figura y la pone en []
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2) #Se usara para dibujar unitariamente cada Cubo de la figura
field = [[0 for i in range(W)] for j in range(H)]   #Crea 'H' listas con 'W' 0's en su interior. Es como un grid interno

anim_count, anim_speed, anim_limit = 0, 60, 2000    #Controlan la velocidad. Se le va sumando 'S' a 'C' y cuando este sea
                                                    #mayor que 'L', la figura baja 1

bg = pygame.image.load('/Users/Usuario/Desktop/Python_New/Tetris/Python-Tetris-1/img/bg.jpg').convert()  #Imagenes de fondo 
game_bg = pygame.image.load('/Users/Usuario/Desktop/Python_New/Tetris/Python-Tetris-1/img/bg2.jpg').convert()    
                           
main_font = pygame.font.Font('/Users/Usuario/Desktop/Python_New/Tetris/Python-Tetris-1/font/font.ttf', 65)   #Fuentes
font = pygame.font.Font('/Users/Usuario/Desktop/Python_New/Tetris/Python-Tetris-1/font/font.ttf', 45)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))       #'lambda' es una funcion que ayuda a reducir una funcion simple. Antes de ':' se ponen los parametros y despues lo que se quiere devolver


figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))  #Toca igualarlo asi para asignar 2 variables a la misma variable
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}    #Diccionario

def check_borders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > W - 1:  #Si sale de los bordes X. Dato curioso: la 'i' equivale al for de donde se llame
            return False
        elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:    #Borde inferior y si choca con otra figura
            return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)   #Puntaje maximo
    with open('record', 'w') as f:
        f.write(str(rec))
        

while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_SPACE: #Lo cree
                while check_borders():  
                    figure_old = deepcopy(figure)
                    for i in range(4):
                        figure[i].y += 1
                
                for i in range(4):  
                    field[figure_old[i].y][figure_old[i].x] = color #Colorea cubo x cubo de la figura
                figure, color = next_figure, next_color #Figura actual
                next_figure, next_color = deepcopy(choice(figures)), get_color()    #Figura en 2do plano
                break
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                anim_limit = 2000
            if event.key == pygame.K_SPACE:
                anim_limit = 2000
    
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):  #'4' porque es la cantidad de cubos de cada figura
        figure[i].x += dx   #Le cambia el eje X a la figura
        
        if not check_borders(): 
            figure = deepcopy(figure_old) #Si choca con un borde, la figura se deforma, por lo que requiere volver a su forma original
            break 
    

    # move y
    anim_count += anim_speed    #Count es la velocidad de bajada
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)   #Ya que 'figure' cambia sus propiedades, estas se cambiarian tambien en 'figure_old' si no tuviera 'deepcopy'
        for i in range(4):
            figure[i].y += 1    
            if not check_borders(): #Si choca...
                for i in range(4):  
                    field[figure_old[i].y][figure_old[i].x] = color #Colorea cubo x cubo de la figura
                figure, color = next_figure, next_color #Figura actual
                next_figure, next_color = deepcopy(choice(figures)), get_color()    #Figura en 2do plano
                break
    # rotate
    center = figure[0]  #Le asigna el cubo principal que es el primero
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders(): #Si choca vuelve a su posicion anterior, osea no rota
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):    #De abajo a arriba mira si hay una fila llena
        count = 0
        for i in range(W):
            if field[row][i]:   #Verifica si la casilla esta ocupada. Cualquier numero que no sea 0 lo toma como True
                count += 1
                
            field[line][i] = field[row][i] #Reemplaza fila llena por la de arriba si el contador es mayor a W, cubo x cubo. Mientras se reemplaza a si misma
        if count < W:
            line -= 1       
        else:
            anim_speed += 3 #Le suma a 'anim_Count' y hara que la figura caiga mas rapido
            lines += 1
    # compute score
    score += scores[lines]
    # draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid] #(surface, color, rect, width) | Se crean 
                                                                            #cuadrados que tienen borde y no fondo. Debido a 
                                                                            # la existencia del 4to parametro
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw color field
    for y, raw in enumerate(field): #'y' numero columna, 'raw' fila entera
        for x, col in enumerate(raw):   #'x' numero de casilla de la fila, 'col' valor de casilla de la fila
            if col: #Un numero distinto de cero, es True
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect) #Dibuja las piezas que cayeron
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, (figure_rect.x, figure_rect.y, TILE-2, TILE-2))
    # draw titles
    sc.blit(title_tetris, (485, 10))
    sc.blit(title_score, (525, 550))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 600))
    sc.blit(title_record, (525, 450))
    sc.blit(font.render(record, True, pygame.Color('gold')), (550, 500))
    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid: # Colorea cada cuadro del grid
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(60)