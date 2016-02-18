import boarddrop as game
import copy
board = game.Board(20,10)


board2 = copy.deepcopy(board)
left = 0
while board2.move("l"):
    left += 1
    before_score = board2.score
    board3 = copy.deepcopy(board2)
    board3.drop_down()
    print(board3)
    print(board3.hash)
    after_score = board3.score
    if after_score - before_score > 0:
        print('line cleared')


board2 = copy.deepcopy(board)
while board2.move("l"):
    before_score = board2.score
    board3 = copy.deepcopy(board2)
    board3.drop_down()
    print(board3)
    print(board3.hash)
    after_score = board3.score
    if after_score - before_score > 0:
        print('line cleared')


