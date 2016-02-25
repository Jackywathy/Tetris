import boarddrop as game
import copy
import re

board = game.Board(20,10)
stuck = re.compile(r'#.{9}(#|\|)\.#')

def lines_fill(board_item):
    print("-----Start----")
    total = 0
    point = 0
    for item in board_item.hash_sort:
        if item:
            total += 1
            point -= 10
    print("total lines =",total)
    print("losing =", point)
    print("---")
    return point

def av_square(int, row = None): #-3 then square, if negative do nothing
    compare = int - 3
    if row:
        print("row No.", row, "exists")
    if compare > 0:
        return compare**2
    else:
        return 0



def move_test(board_object):
    allpoints = []
    dup1 = copy.deepcopy(board_object)
    dup2 = copy.deepcopy(board_object)
    # test with "l"
    left = 0
    board3 = None
    while dup1.move("l"):
        row = 0
        point = 0
        left += 1



        before_score = dup1.score
        board3 = copy.deepcopy(dup1)
        board3.drop_down()
        point += lines_fill(board3)
        after_score = board3.score
        if after_score - before_score > 0:
            print('line cleared +', 200*(after_score-before_score))
            point += 200 * (after_score - before_score)
        for element in board3.hash_sort:
            row += 1
            if element:
                point += av_square(len(element), row)
        point -= detect_unfillable(board3)
        print(point, "TOTAT POINTS")
        print(board3) # TODO get rid
        allpoints.append((point, ("l", left)))


    del board3
    # test with "r"
    right = 0
    while dup2.move("r"):
        point = 0
        right += 1
        before_score = dup2.score
        board3 = copy.deepcopy(dup2)
        board3.drop_down()
        point += (lines_fill(board3))
        after_score = board3.score
        if after_score - before_score > 0:
            print('line cleared +', 200*(after_score-before_score))
            point += 200 * (after_score - before_score)
        for element in board3.hash_sort:
            if element:
                point += av_square(len(element))
        point -= detect_unfillable(board3)
        print(point, "p")
        print(board3) # TODO get rid
        allpoints.append((point, ("r", right)))

    return allpoints

def do_loop(iterations, direction, rotate=None): #move board left or right iteration times
    for i in range(iterations):
        board.move(direction)
    board.drop_down()


def one_move():
    x = (move_test(board))
    largest = max(x, key = lambda y:y[0])
    print("-----")
    print("PROPER BOARD")
    print(largest, "board")

    do_loop(largest[1][1], largest[1][0])
    print(board)
    print("---+_--")


def detect_unfillable(board_object):
    print(repr(board_object))
    if (stuck.findall(repr(board_object))):
        print("ARRGE BAD ERRO, r, unfillable detected")
    return (len(stuck.findall(repr(board_object)))*50)



while True:
    put = input("")
    if not put:
        one_move()
    else:
        break
print(board)
print(repr(board))
print(stuck.findall(repr(board)))