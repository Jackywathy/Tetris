import boarddrop as game
import copy
import itertools
board = game.Board(20,10)

def lines_fill(board_item):
    point = 0
    for item in board_item.hash:
        print(item)
        point += item[0]
    return point

def av_square(int): #-5 then square, if negative do nothing
    compare = int - 2
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
    while dup1.move("l"):
        point = 0
        left += 1
        before_score = dup1.score
        board3 = copy.deepcopy(dup1)
        board3.drop_down()
        print(board3)
        print(lines_fill(board3))
        after_score = board3.score
        if after_score - before_score > 0:
            print('line cleared')
            point += 100
        for element in board3.hash_sort:
            if element:
                point += av_square(len(element))
        print(point)
        allpoints.append((point, ("l", left)))



    # test with "r"
    right = 0
    while dup2.move("r"):
        point = 0
        right += 1
        before_score = dup2.score
        board3 = copy.deepcopy(dup2)
        board3.drop_down()
        print(board3)
        print(lines_fill(board3))
        after_score = board3.score
        if after_score - before_score > 0:
            print('line cleared')
            point += 100
        for element in board3.hash_sort:
            if element:
                point += av_square(len(element))
        print(point)
        allpoints.append((point, ("r", right)))

    return allpoints

def do_loop(iterations, direction, rotate=None): #move board left or right iteration times
    for i in range(iterations):
        print("once")
        board.move(direction)
    board.drop_down()


def one_move():
    x = (move_test(board))
    print(x)
    largest = max(x, key = lambda y:y[0])
    print(largest)
    do_loop(largest[1][1], largest[1][0])
    print(board)

def detect_unfillable():


while True:
    put = input("")
    if not put:
        one_move()
    else:
        break

