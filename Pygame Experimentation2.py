import time, pygame as pg, os, boardreloser, sys
from pygame.locals import *
#os.chdir("/Users/jackjiang/Desktop/Tetris")

gameover = False

pg.init()
#colourse
darkpurple = (36,7,41)
white = (255,255,255)
black = (0,0,0)
yellow = (0,255,255)
red = (255, 0 , 0)
pink = (255, 0 ,255)
plurple = (179,42,232)
light_green = (11,255,44)
dark_blue = (16,17,255)


fontObj4 = pg.font.Font("Papyrus.ttc",10)
fontObj2 = pg.font.Font("Papyrus.ttc",50)
fontObj3 = pg.font.Font("Comic.ttf", 50)
fontObj = pg.font.Font("freesansbold.ttf", 35)




def show_score():
    global screen
    screen.fill((255,255,255))
    ren = fontObj.render("Score = " + str(x.score),True, black)
    ren2 = fontObj3.render("WELL, game over", True, black)
    ren3 = fontObj2.render("PLAY AGAIN?", True, black)
    #ren4 = fontObj.render("© ?inc", True, black)
    screen.blit(ren, (10,10))
    screen.blit(ren3, (50, 500))
    screen.blit(ren2, (50 ,200))
    screen.blit(picture, (150, 300))
    #screen.blit(ren4, (150, 600))
    pg.display.update()


pg.display.set_caption("Tetris")
fpsClock = pg.time.Clock()
screen = pg.display.set_mode((500, 700))
screen.fill(white)
border = pg.Rect(88,28,323,643)
inside_border = pg.Rect(90,30,319,639)
next_shape = pg.Rect(435,49,40,40)
next_shape_inside = pg.Rect
pg.draw.rect(screen, darkpurple, border, 2)
pg.draw.rect(screen, darkpurple, next_shape, 1)

render = fontObj4.render("Next Shape", True, darkpurple)
render2 = fontObj4.render("COMNG SOON!", True, darkpurple)
screen.blit(render2, (428, 40))
screen.blit(render, (428,20))

pg.display.update()
picture = pg.image.load("dog1.jpeg")
picture.convert()
picture = pg.transform.scale(picture, (135,90))


#print(os.listdir())
x = boardreloser.Board(20, 10)

_square = pg.Rect(420,100, 100,30)

def update_graphics():
    if x.file == "1.txt":
        box_color = yellow
    elif x.file == "2.txt":
        box_color = red
    elif x.file == "3.txt":
        box_color = pink
    elif x.file == "4.txt":
        box_color = plurple
    elif x.file == "5.txt":
        box_color = light_green
    elif x.file == "6.txt":
        box_color = dark_blue



    else:
        box_color = black



    rand = 0
    global screen
    global fps
    global _square

    ren = fontObj.render(str(round(fps,1)), True, darkpurple)


    screen.fill(white, inside_border)
    height1 = -2
    for element in x.list:
        height1 += 32
        width1 = 58
        for element2 in element:
            if rand < 250:
                rand += 1
            width1 += 32
            box_border =  pg.Rect(width1, height1, 32, 32)
            if (element2) == "x" or element2 == "0":
                pg.draw.rect(screen, box_color, (width1, height1, 30, 30))
                pg.draw.rect(screen, yellow, box_border, 1)
            elif element2 == "#":
                pg.draw.rect(screen, (255-rand,0, 255-rand), (width1, height1, 30, 30))
                pg.draw.rect(screen, yellow, box_border, 1)
            else:

                pg.draw.rect(screen, yellow, box_border, 1)
    screen.fill(white, _square)
    screen.blit(ren, (420,100))
    # create a next shape




fps = 0
pg.event.clear()
update_graphics()

pg.key.set_repeat(2)
y = 0
while True:
    # noinspection PyRedeclaration
    fps = (fpsClock.get_fps())
    fpsClock.tick(20)
    # draw.rect(screen, color, (wdith from left side, width from top side, width of rect, height of rect
    y += 1
    if y > 15:
        y = 0
        x.drop()
        update_graphics()

    if x.gameover:
        print("GAMEMOVER!")
        show_score()
        time.sleep(5)
        pg.quit()
        sys.exit()







    #pygame.draw.rect(screen,(255,0,0),
    pg.display.update()
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == 27:
                print("QUITTING")
                print("SCORE =", x.score)
                show_score()
                time.sleep(10)
                pg.quit()
                sys.exit()
            elif event.key == K_a or event.key == K_LEFT: # = a
                x.move("l")
                update_graphics()
            elif event.key == K_d or event.key == K_RIGHT: # = d
                x.move("r")
                update_graphics()
            elif event.key == K_j or event.key == K_q: # = j
                x.rotate("l")
                update_graphics()
            elif event.key == K_l or event.key == K_e: # = e
                x.rotate("r")
                update_graphics()
            elif event.key == K_SPACE or event.key == K_RETURN: # = space
                pg.key.set_repeat()
                _n = False
                num = 0
                while True:
                    if x.check_touch():
                        _n = True
                    if _n:
                        _n = False
                        x.drop()
                        pg.key.set_repeat(2)
                        break

                    x.drop()
                update_graphics()
            elif event.key == K_s or event.key == K_DOWN: # s
                x.drop()
                update_graphics()
            else:
                print(event.key)


update_graphics()
pg.display.update()
