import pygame, time
from copy import deepcopy
from random import choice, randrange

Tile = 40
W = 9 
H = 15
pygame.init()
Game_Res = (W * Tile, H * Tile)
sc = pygame.display.set_mode(Game_Res)
clock = pygame.time.Clock()   

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],      #Aca estan las 7 figuras: l, o, s, L, T, J, z
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


#rect(120, 120, 38, 38)>, <rect(120, 160, 38, 38)>, <rect(160, 120, 38, 38)>, <rect(160, 80, 38, 38)
#figures = [[pygame.Rect((figures_pos[j][i][0]+4)*(Tile),(figures_pos[j][i][1]+3)*(Tile),Tile-2,Tile-2) for i in range(4)] for j in range(7)]
figures = [[pygame.Rect(x + W //2 ,y+1,Tile-2,Tile-2) for x,y in fig_pos] for fig_pos in figures_pos]   #1. "x + W//2"Para que quede centrado
figure_Rect = pygame.Rect(0, 0, Tile - 2, Tile - 2)
field = [[0 for i in range(W)] for j in range(H)]

get_color = lambda : (randrange(30,256), randrange(30,256), randrange(30,256))
figure = deepcopy(choice(figures))
color = get_color()
score = 0
anim_count, anim_speed, anim_limit = 0, 60, 2000



def down():
        global figure, color

        for i in range(4):
                figure[i].y += 1

        if check_borders():
                figure = figurold
                for i in range(4):  
                        field[figurold[i].y][figurold[i].x] = color

                figure = deepcopy(choice(figures))
                color = get_color()
def up():
        global figure
        axis = figure[0]
        for i in range(4):
                x = figure[i].y - axis.y
                y = figure[i].x - axis.x

                figure[i].x = axis.x - x
                figure[i].y = axis.y + y

        if check_borders():
                figure = figurold
def mov_x(dx):
        global figure
        for i in range(4):
                figure[i].x += dx

        if check_borders():
                figure = figurold

def space():        
        global figure, figurold
        while not check_borders():
                figurold = deepcopy(figure)
                for i in range(4):
                        figure[i].y += 1
                check_borders()
        down()
 
def normal():
        global anim_count, anim_limit, anim_speed, figurold
        anim_count += anim_speed    #Count es la velocidad de bajada
        if anim_count > anim_limit:
                anim_count = 0
                figureold = deepcopy(figure) 
                down()

def check_borders():
        global figure, color
        for i in range(4):
                if figure[i].x < 0 or figure[i].x > W - 1:
                        return True
                if figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
                        return True
                        
        return False
        
def check_lines():
        global field, score
        cont = 0
        for yn,y in enumerate(field):
                for xn,x in enumerate(y): 
                        if x:
                                cont += 1
                
                if field[0][3]:
                        field = [[0 for i in range(W)] for j in range(H)]
                        time.sleep(0.8) #Pausa programa
                if cont == 9:
                        time.sleep(0.3)

                        for inverse in range(yn,0,-1):
                                field[inverse] = field[inverse-1]

                        score += 1
                        print("Score: ",score)
                        
                else:
                        cont =0

while True:
        normal()
        
        figurold = deepcopy(figure)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                mov_x(-1)
                        if event.key == pygame.K_RIGHT:
                                mov_x(1)
                        if event.key == pygame.K_DOWN:
                                down()
                        if event.key == pygame.K_UP:
                                up()
                        if event.key == pygame.K_SPACE:
                                space()
                
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                                        ...

        check_borders()
        sc.fill((0,0,0))
        grid = [pygame.draw.rect(sc,(255,0,0),(Tile*i,Tile*j,Tile,Tile),1) for i in range(W) for j in range(H)] #Grid
        check_lines()
        #Draw figure
        for i in range(4):
                figure_Rect.x = figure[i].x * Tile
                figure_Rect.y = figure[i].y * Tile
                pygame.draw.rect(sc, color, figure_Rect)
        
        #Draw field
        for yn,y in enumerate(field):
                for xn,x in enumerate(y): 
                        if x:
                                #print(xn, yn)
                                figure_Rect.x = xn*Tile
                                figure_Rect.y = yn *Tile
                                pygame.draw.rect(sc, x, figure_Rect)
        
        

        pygame.display.update()
        clock.tick(200)