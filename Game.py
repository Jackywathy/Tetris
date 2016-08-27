import time, pygame as pg, os, boardre, sys
from constants import *
from pygame.locals import *
#os.chdir("/Users/jackjiang/Desktop/Tetris")

gameover = False

pg.init()
#colourse


with open('out.txt','w') as f:
    print(os.getcwd(), file=f)
fontObj4 = pg.font.Font("freesansbold.ttf",10)
fontObj2 = pg.font.Font("Papyrus.ttc",50)
fontObj3 = pg.font.Font("Comic.ttf", 50)
fontObj = pg.font.Font("freesansbold.ttf", 35)



print(os.getcwd()) # Log this line.
pg.mixer.music.load("Tetris2.wav")
    #("cool.mid")
#pg.mixer.music.play(-1)
current_color = light_green


def show_score():
    global screen
    screen.fill(current_color)
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
    time.sleep(2)

pg.mouse.set_visible(False)
pg.display.set_caption("Tetris")
fpsClock = pg.time.Clock()
screen = pg.display.set_mode((500, 700))
screen.fill(aqua)
border = pg.Rect(88,28,323,643)
inside_border = pg.Rect(90,30,319,639)
next_shape = pg.Rect(435,49,40,40)
next_shape_inside = pg.Rect
pg.draw.rect(screen, darkpurple, border, 2)
pg.draw.rect(screen, darkpurple, next_shape, 1)

render = fontObj4.render("Next Shape", True, darkpurple)
screen.blit(render, (428,20))

pg.display.update()
picture = pg.image.load("dog1.jpeg")
picture.convert()
picture = pg.transform.scale(picture, (135,90))


#print(os.listdir())
x = boardre.BetterBoard(10, 20)

_square = pg.Rect(420,100, 100,30)

def render_next_shape(item):
    global screen
    screen.fill(white, (436, 50,38,38))
    with open(item) as f:
        for y,line in enumerate(f):
            for x,letter in enumerate(line):
                if letter == 'x' or letter == '0':
                    pg.draw.rect(screen,boardre.BetterBoard.Colors[item],pg.Rect(438+x*9,52+y*9,9,9))





def update_graphics():



    rand = 0
    global screen
    global fps
    global _square
    if x.randlist:
        render_next_shape(x.randlist[0])
    ren = fontObj.render(str(round(fps,1)), True, darkpurple)


    screen.fill((255,255,255), inside_border)
    height1 = -2
    for y_,element in enumerate(x.board.array):
        height1 += 32
        width1 = 58
        for x_,element2 in enumerate(element):
            if rand < 250:
                rand += 1
            width1 += 32
            box_border =  pg.Rect(width1, height1, 32, 32)
            if (element2) == "x" or element2 == "0":
                pg.draw.rect(screen, boardre.BetterBoard.Colors[x.color_dict[(x_,y_)]], (width1, height1, 30, 30))
                pg.draw.rect(screen, black, box_border, 1)
            elif element2 == "#":
                pg.draw.rect(screen, boardre.BetterBoard.Colors[x.color_dict[(x_,y_)]], (width1, height1, 30, 30))
                pg.draw.rect(screen, black, box_border, 1)
            else:

                pg.draw.rect(screen, black, box_border, 1)
    screen.fill(aqua, _square)
    screen.blit(ren, (420,100))
    # create a next shape

fps = 0
pg.event.clear()
update_graphics()
y = 0
norotate = 0 # frames before being allowed to rotate
nospam = 0 # frames before being allowed to press space again

pg.key.set_repeat(2,100)
try:
    while True:

        # noinspection PyRedeclaration
        fps = (fpsClock.get_fps())

        # draw.rect(screen, color, (wdith from left side, width from top side, width of rect, height of rect
        y += 1
        if y > 15:
            y = 0
            x.drop()
            update_graphics()

        if x.gameover:
            print("GAMEMOVER!")
            show_score()
            pg.quit()
            sys.exit()


        #pygame.draw.rect(screen,(255,0,0),
        for event in pg.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    print("QUITTING")
                    print("SCORE =", x.score)
                    show_score()
                    pg.quit()
                    sys.exit()
                elif event.key == K_a or event.key == K_LEFT: # = a
                    x.move("l")
                    update_graphics()
                elif event.key == K_d or event.key == K_RIGHT: # = d
                    x.move("r")
                    update_graphics()
                elif event.key == K_j or event.key == K_q: # = j
                    if norotate:
                        continue
                    x.rotate("l")
                    update_graphics()
                    norotate = 3
                elif event.key == K_l or event.key == K_e or event.key == K_UP:  # = e
                    if norotate:
                        print("nope")
                        continue
                    print("ere")
                    x.rotate("r")
                    update_graphics()
                    norotate = 3
                elif event.key == K_SPACE or event.key == K_RETURN: # = space
                    if nospam:
                        continue
                    x.drop_down()
                    update_graphics()
                    nospam = 10
                elif event.key == K_s or event.key == K_DOWN: # s
                    x.drop()
                    update_graphics()
                else:
                    print(event.key)
        pg.display.update()
        fpsClock.tick(20)
        if norotate:
            norotate -= 1
        if nospam:
            nospam -= 1

except boardre.GameOverException:
    show_score()
    raise