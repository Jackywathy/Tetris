import boarddrop as game
import copy
import re

board = game.Board(20,10)
stuck = re.compile(r'#.{9}(#|\|)\.#')
no_space = re.compile(r'#.{10}\.')
block_top = re.compile(r'#.(10)')
side1 = re.compile(r'#|')
side2 = re.compile(r'|#')
def detect_unfillable(board_object):
    out = 0
    w = (repr(board_object))
    print(w)
    if (stuck.findall(w)):
        out += (len(stuck.findall(repr(board_object)))*50)
        print("ARRGE BAD ERRO, r, unfillable detected. losing 50 poijnts")
    if no_space.findall(w):
        print(no_space.findall(w))
        out += (len(no_space.findall(w))*10)
        print("no space, losing", (len(no_space.findall(w))*10) ,"points")
    print("losing", out, 'Points because of RE"s!')
    return out


def detect_side(board_item):
    """Looks for hash tags that are the side of the board"""
    return len(side1.findall(repr(board_item)))+len(side2.findall(repr(board_item)))

def lines_fill(board_item):
    """finds how many lines of the tetris board is being used, losing 5 points for each line occupied"""
    total = 0
    point = 0
    for item in board_item.hash_sort:
        if item:
            total += 1
            point += 5
    print(total,"lines")
    return point

def av_square(board_object):
    """Given a board_object, loop through each line, looking for lines that are more filled"""
    ret = 0
    for line in board_object.hash_sort:
        if line:
            if len(line)-3>0:
                ret += len(line-3)**2

    return ret

def compare_score(board_object, score):
    """Compares the original score with the score of the board_object given. Returns 20*line difference"""
    return board_object.score - score


def do_test(test, before_score):
    """Run all tests with the board object"""
    point = 0
    #
    point -= lines_fill(test)
    #
    point += compare_score(test,before_score) * 100
    #
    point += av_square(test)
    #
    point -= detect_unfillable(test)
    #
    point += detect_side(test)
    #
    return point


def move_test(original):
    """Does all left then right moves given a board object"""

    allpoints = []
    #create a duplicates
    test = copy.deepcopy(original)

    #
    # test with "l"
    #

    left = 0
    # the ingame tetris score before testing
    before_score = original.score
    # keep moving left
    while test.move("l"):
        left += 1
        #then create another board to test with
        after_move = copy.deepcopy(test)
        after_move.drop_down()
        #
        final = do_test(after_move,before_score)
        allpoints.append([final,"l"+str(left)])
        #
        print((after_move))
        print("points =",final)
    del test
    # test with "r"


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





move_test(board)