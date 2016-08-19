import random
import copy
from collections import deque
from Board import twoDimArray
try:
    import LOGGER
    log = True
except ImportError:
    log = False


def convert(list_of_tuples, zero):  #
    """converts a relative value to zero to an absolute one"""
    out = []
    for i in list_of_tuples:
        out.append(plus_tuple(i, zero))
    return out

def better_convert(xy, zero):
    return xy[0] + zero[0], xy[1] + zero[1]
def plus_tuple(tuple, origin):
    return ((origin[0] + tuple[0] * -1, origin[1] + tuple[1]))


class BetterBoard:
    Empty = "."
    Moving = 'x'
    Middle = '0'
    Solid = '#'
    bag = [
        "1.txt","1.txt","1.txt","1.txt",
        "2.txt","2.txt","2.txt","2.txt",
        "3.txt","3.txt","3.txt","3.txt",
        "4.txt","4.txt","4.txt","4.txt",
        "5.txt","5.txt","5.txt","5.txt",
        "6.txt","6.txt","6.txt","6.txt",
        "7.txt","7.txt","7.txt","7.txt"
    ]

    Colors = {
        "1.txt": (255,0,0),
        "2.txt": (255,0,255),
        "3.txt": (255,255,0),
        "4.txt": (0,255,255),
        "5.txt": (0,0,255),
        "6.txt": (160,160,160),
        "7.txt": (0,255,0)
    }

    def __init__(self, width, height, maxqueue = 3):
        # create some attributes
        self.gameover = False
        self.score = 0
        self.bag = [] #  a bag of txt's
        self.randlist = deque() # a deque that handles all the random objects. Has 3 in by default
        self.maxqueue = maxqueue


        self.hash = set()    # type:set
        self.can_rotate = True      # Can rotate
        self.xs = set()      # type:set
        #  where x's are on the board, represented as tuples coordinates. Is erased with zero
        self.zero = ()
        self.file_name = None

        self.relative = []      # where x's are relative to self.zero. Created every time a new file is loaded
        self.columns = width    # width of the board. Never changed
        self.rows = height      # height of the board. Never changed
        self.file = []          # which tetris piece is loaded
        self.board = twoDimArray(width,height, start=BetterBoard.Empty) # type: twoDimArray
        self.color_dict = {}

    def populate_rand(self):
        while len(self.randlist) < self.maxqueue:
            if not self.bag:
                self.bag = copy.deepcopy(BetterBoard.bag)
            rani = random.randint(0,len(self.bag)-1)
            print(rani)
            self.randlist.append(
                self.bag.pop(rani)

            )

    def _load_file(self):
        """Loads a file in self.file, taking it off self.randlist"""
        self.populate_rand()
        self.file_name = self.randlist.popleft()
        with open(self.file_name) as f:
            self.file = list((f.readlines()))
            for x,i in enumerate(self.file):
                self.file[x] = i.rstrip('\n')



    def load_part(self):
        self.can_rotate = False
        if not self.file:
            self._load_file()
        part = self.file.pop()

        middle = self.columns//2
        insertpoint = middle-len(part)//2
        for iterate,i in enumerate(part):
            point = insertpoint+iterate
            if self.board.get(point,0) != BetterBoard.Empty and i != BetterBoard.Empty:
                # if the space is not empty and the part is not empty
                raise Exception("die, Die, DIE!")
            elif i == BetterBoard.Moving:
                self.board.set(point, 0, BetterBoard.Moving) # set x and y of board to be that bit
                self.color_dict[(point, 0)] = self.file_name # set x and y of color dict to be that part
                self.xs.add((point,0))
            elif i == BetterBoard.Middle:
                self.board.set(point,0, BetterBoard.Middle)
                self.color_dict[(point,0)] = part
                self.zero = (point,0)
            elif i == BetterBoard.Empty:
                pass

            else:
                raise Exception(i,'is unexpected')
        if not self.file:
            self.can_rotate = True


    # all these tables need to be updated every single move:
    # x's, hashes, color, list and relative

    def drop(self):  # drop the tetromeno down by ONE
        """Drop all the piece by 1"""
        if self.xs: # if there is any bits on the board
            new_xs = set()
            for item in self.xs:
                new_xs.add((item[0], item[1]+1))
                block_color = self.color_dict.pop(item)

            if self.zero:
                new_zero = (self.zero[0], self.zero[1]+1)
                block_color = self.color_dict.pop(self.zero)
                # then test if it is hitting atnyhgin
                if self.board.get_tuple(new_zero) == BetterBoard.Solid:
                    raise Exception(self.zero, 'is zero and hit')
            # now test for if it is going to hit something
            for i in new_xs:
                try:
                    if self.board.get_tuple(i) == BetterBoard.Solid:
                        raise Exception(i, 'is full!!!')
                except IndexError:
                    raise Exception(i, "is bottom of the board")

            # PASSED ALL THE TEST!

            # finally shift everything down
            # first delete all original self.x's
            for i in self.xs:
                self.remove_item(i)
            self.xs = new_xs
            # then set the new self.xs's as x's and update color dict

            if self.zero:
                # if new_zero is set, then do it else, just leave
                self.color_dict[new_zero] = block_color
                self.remove_item(self.zero)
                self.board.set_tuple_item(BetterBoard.Middle, new_zero)
                self.zero = new_zero

            for i in new_xs:
                self.board.set_tuple_item(BetterBoard.Moving, i)
                self.color_dict[i] = block_color
        if not self.xs or self.file:
            self.load_part()
        # TODO REMOVE!
        self.display()
        print()





    def regenerate_board(self):
        """
        Force Regens the board
        :return: NoneType
        """
        rows = range(self.rows)

        for row_num in rows:
            self.board.array[row_num][:] = [BetterBoard.Empty]*self.columns  # set's list to empty
        for i in self.xs:
            self.board.set_tuple_item(BetterBoard.Moving, i)
        for i in self.hash:
            self.board.set_tuple_item(BetterBoard.Solid , i)
        if self.zero:
            self.board.set_tuple_item(BetterBoard.Middle,self.zero)

    def display(self):
        for i in self.board.array:
            print(i)

    def remove_item(self, xy):
        self.board.set_tuple_item(BetterBoard.Empty, xy)


    def rotate(self, dir):
        """
        Rotates the pieces around
        :type dir: string
        """
        if not self.can_rotate or not self.zero:
            return "RET"
        # first make self.relative, a list that shows x's relative to
        print(self.xs, self.zero, self.can_rotate)
        relative = [(coordinate[0] - self.zero[0], coordinate[1] - self.zero[1]) for coordinate in self.xs]
        print(relative)
        if dir == 'l':
            new_xs = [better_convert((item[1], -item[0]), self.zero) for item in relative]
            print(new_xs)
        elif dir == 'r':
            new_xs = [better_convert((-item[1], item[0]), self.zero) for item in relative]
            print(new_xs)
        else:
            raise Exception("Accepts only 'r' or 'l', not " + dir)
        if not self.legal(new_xs):
            return
        else:
            # it's all LEGAL! - remove everything!
            for i in self.xs:
                self.remove_item(i)
                block_color = self.color_dict.pop(i)

            for i in new_xs:
                43uju77



    def legal(self, list_of_tuples):
        if type(list_of_tuples) == list:
            for element in list_of_tuples:
                if element[0] >= self.columns or element[1] >= self.rows:  # list[10] = 11th element, therefore must be smaller
                    return False
                if element in self.hash: # if it hits a hash element
                    return False
                if element [0] < 0 or element[1] < 0: # if it is above/ under
                    return False
            # if it passes every thest
            return True
        else:
            raise ValueError ("Here")



if __name__ == '__main__':
    x = BetterBoard(5,10)
    x.drop()
    x.drop()
    x.drop()

    """
    while True:
        if x.file or not x.xs:
            x.load_part()
        x.display(); input()
        x.drop()
        x.regenerate_board()"""
    z=x.display





    #x.drop()
    #x.drop()
    #x.rotate('r')
    #x.drop()
    #z()





