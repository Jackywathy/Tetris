import boarddrop as game
import copy
import re
from operator import itemgetter
import time
import sys

board = game.Board(20,10)
stuck = re.compile(r'#.{9}(#|\|)\.#')
stuck2 = re.compile(r'#.{9}#')
stuck3 = re.compile(r'#.{11}#')
no_space = re.compile(r'#.{10}\.')
block_top = re.compile(r'#.{10}')
side1 = re.compile(r'#\|')
side2 = re.compile(r'\|#')
stuck4 = re.compile(r'#(.{10}){2-4}\.')
no_space_above = re.compile(r'#.{10}\.')


def continuous(board_object):
    """Gives more points depending on how continuous the lines are. If a line has"""
    ret = 0
    for line in board_object:
        isLine = False
        items = 0
        all_results = []
        for letter in line:
            if letter == "#" and isLine:
                items += 1
            elif letter == "#":
                items += 1
                isLine = True
            else:
                isLine = False
                if items:
                    all_results.append(items)
                items = 0
        if items:
            all_results.append(items)
        print(all_results)
        for i in all_results:
            if i-3 > 0:
                ret += i**2
        return ret



def detect_unfillable(board_object):
    out = 0
    w = (repr(board_object))
    if (stuck.findall(w)):
        out += (len(stuck.findall(repr(board_object)))*50)
        #print("ARRGE BAD ERRO, r, unfillable detected. losing 50 poijnts")
    if no_space.findall(w):
        out += (len(no_space.findall(w))*10)
        #print("no space, losing", (len(no_space.findall(w))*20) ,"points")
    out += len(no_space_above.findall(repr(board_object))) * 50
    if (no_space_above.findall(repr(board_object))):
        print('nospace')
    out += len(stuck2.findall(repr(board_object))) * 50
    out += len(stuck3.findall(repr(board_object))) * 50
    if stuck4.findall(w):
        print("multistuck")
        out += (len(no_space.findall(w))*100)
    #print("losing", out, 'Points because of RE"s!')
    return out


def detect_side(board_item):
    """Looks for hash tags that are the side of the board"""
    assert type(board_item) == game.Board
    return len(side1.findall(repr(board_item)))+len(side2.findall(repr(board_item)))

def lines_fill(board_item):
    """finds how many lines of the tetris board is being used, losing 5 points for each line occupied"""
    assert type(board_item) == game.Board
    total = 0
    point = 0
    for item in board_item.hash_sort:
        if item:
            total += 1
            point += 5
    return point

def av_square(board_object):
    """Given a board_object, loop through each line, looking for lines that are more filled"""
    assert type(board_object) == game.Board
    ret = 0
    for line in board_object.hash_sort:
        if line:
            if len(line)-3>0:
                ret += (len(line)-3)**2

    return ret

def compare_score(board_object, score):
    """Compares the original score with the score of the board_object given. Returns 100*line difference"""
    assert type(board_object) == game.Board
    assert type(score) == int

    return board_object.score - score * 100

def do_test(test, before_score=0):
    """Run all tests with the board object"""
    assert type(test) == game.Board
    assert type(before_score) == int
    point = 0
    #
    point -= lines_fill(test)
    #
    point += compare_score(test,before_score)
    #
    point += av_square(test)
    #
    point -= detect_unfillable(test)
    #
    point += detect_side(test)
    #
    point += continuous(test)
    return point


def print_fancy(original, *args):
    return 0
    print("------START----")
    print(original)
    print("score =", score)
    print("-------END-----")


def wiggle(board_object, move_direction, move_number, rotate_direction, rotate_number, before_score):
    """Given a board object, wiggles it left and right and returns a list of lists of data"""
    test = copy.deepcopy(board_object)
    if type(move_number) == int:
        for i in range(int(move_number)):
            test.move(move_direction)

        moveall = str(move_direction) + str(move_number)
    else:
        moveall = None

    if type(rotate_number) == int:
        for i in range(int(rotate_number)):
            test.rotate(rotate_direction)

        rotateall = str(rotate_direction) + str(rotate_number)
    else:
        rotateall = None
    test.drop_down_less()
    test1 = copy.deepcopy(test)
    test.move('l')
    test1.move('r')
    return [[do_test(test, before_score), moveall, rotateall, "l", True],
            [do_test(test1, before_score), moveall, rotateall, "r", True]]



def move_test(original):
    """Does all left then right moves given a board object"""
    assert type(original) == game.Board


    allpoints = []
    #create a duplicates
    test = copy.deepcopy(original)
    temp = copy.deepcopy(original)

    before_score = original.score
    """Just test from dropping down and rotating, no LR movement"""
    # first wiggling it though
    allpoints += wiggle(temp,None, None, None, None, before_score)
    #
    temp.drop_down()
    final = do_test(temp,before_score)
    allpoints.append([final,None,None,None,False])
    print(temp,before_score, final,"ALLTEMPS WRONG")

    #
    for i in range(1,4): #rotates it left thrice
        after_move = copy.deepcopy(original)
        for w in range(i):
            after_move.rotate("l")
        #Then wiggle it
        allpoints += wiggle(after_move,None,None,'l',i ,before_score)
        #
        after_move.drop_down()
        allpoints.append([do_test(after_move,before_score), None, "l"+str(i), None, False])
        print_fancy(after_move, final)

    for i in range(1,4): #rotates it right thrice
        after_move = copy.deepcopy(original)
        for w in range(i):
            after_move.rotate("r")
        #Then wiggle it
        allpoints += wiggle(after_move,None,None,'r',i ,before_score)
        #
        after_move.drop_down()
        allpoints.append([do_test(after_move,before_score),None,"r"+str(i), None, False])
        print_fancy(after_move, final)

    """structure of a formula
    [ [points, move dir e.g."l1", rotate dir e.g. "r1", wiggle amount, if wiggle]
    """

    """TESTING WTH LEFT AND RIGHT"""
    left = 0
    right = 0

    # the ingame tetris score before testing
    # keep moving left
    """FIRST WITH LEFT"""
    while test.move("l"):
        left += 1
        #then create another board to test with
        after_move = copy.deepcopy(test)
        #wiggle test it
        allpoints += wiggle(after_move,"l", left, None, None, before_score)
        #
        after_move.drop_down()
        allpoints.append([do_test(after_move, before_score), "l"+str(left), None, None, False])
        print_fancy(after_move, final)
        #
        #
        for i in range(1,4): #rotates it left thrice
            after_move = copy.deepcopy(test)
            for w in range(i):
                after_move.rotate("l")
            #
            allpoints += wiggle(after_move,"l", left, 'l', i, before_score)
            #
            after_move.drop_down()
            final = do_test(after_move,before_score)
            allpoints.append([final,"l"+str(left),"l"+str(i), None, False])
            print_fancy(after_move)

        for i in range(1,4): #rotates it right thrice
            after_move = copy.deepcopy(test)
            for w in range(i):
                after_move.rotate("r")
            #yoloswag
            #wiggle a shape
            allpoints += wiggle(after_move,'l',left,'r',i ,before_score)
            #
            #

            after_move.drop_down()
            allpoints.append([do_test(after_move,before_score),"l"+str(left),"r"+str(i), None, False])
            print_fancy(after_move)

    del test
    """THIS IS FOR TESTING WITH ALL LEFTS!"""
    # test with "r"
    test = copy.deepcopy(original)
    """THIS TESTS FOR RIGHTS"""
    while test.move("r"):
        right += 1
        #then create another board to test with
        after_move = copy.deepcopy(test)
        # first wiggle it tho
        allpoints += wiggle(after_move,"r", right, None, None, before_score)
        #
        after_move.drop_down()
        #
        allpoints.append([do_test(after_move,before_score),"r"+str(right),None, None, False])
        #
        #
        for i in range(1,4): #rotates it left thrice
            after_move = copy.deepcopy(test)
            for w in range(i):
                after_move.rotate("l")
            # wiggle it
            allpoints += wiggle(after_move,"r", right, 'l', i, before_score)
            #

            after_move.drop_down()
            final = do_test(after_move, before_score)
            allpoints.append([final,"r"+str(right),"l"+str(i), None, False])

        for i in range(1,4): #rotates it right thrice
            after_move = copy.deepcopy(test)
            for w in range(i):
                after_move.rotate("r")
            #wiggle it
            allpoints += wiggle(after_move,"r", right, 'r', i, before_score)
            #

            after_move.drop_down()
            final = do_test(after_move,before_score)
            allpoints.append([final,"r"+str(right),"r"+str(i), None, False])
    del test
    return allpoints


def do_formula(values):
    """Takes in a listof 3 strings[Point of the formula(not used), amount moved 'l4'=left 4, rotation 'r4' = right 4, wiggle amount, if wiggle]"""
    global board
    print(values)
    assert type(values) == list
    assert len(values) == 5
    print("BEFORE")
    print(board)
    if values[1]:
        for i in range(int(values[1][1])):
            board.move(values[1][0])
    if values[2]:
        for i in range(int(values[2][1])):
            board.rotate(values[2][0])
    if values[3]:
        print(values[3])
        board.drop_down_less()
        board.move(values[3])
        board.drop()
        print(board)
    else:
        board.drop_down()
    print("After")
    print(board)

w = 0
while True:
    rep = copy.deepcopy(board)
    z = (move_test(board))
    big = (max(z,key=itemgetter(0)))
    noMove = []
    for i in z:
        if not i[3]:
            noMove.append(i)
    bigNoMove = max(noMove,key=itemgetter(0))
    print('--List--')
    for i in z:
        print(i)
    print("--list--")
    print("largest no wiggle",bigNoMove)
    print("largest wiggle", big)
    if big[0] == bigNoMove[0]:
        big = bigNoMove
    do_formula(big)
    if board.gameover:
        print("score =", board.score)
        break


    if w:
        break
    w = True
    time.sleep(1)

