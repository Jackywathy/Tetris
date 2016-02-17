import random
import copy


def convert(list_of_tuples, zero):  # converts a relative value to an absolute one
    out = []
    for i in list_of_tuples:
        out.append(plus_tuple(i, zero))
    return out


def plus_tuple(tuple, origin):
    return ((origin[0] + tuple[0] * -1, origin[1] + tuple[1]))




class Board:
    def __init__(self, height, width):  # creates the board, with height and width
        # create some attributes
        self.gameover = False
        self.score = 0
        self.randlist = []  # a list containing all the .txts to load
        self.hash_sort = []
        self.rotate_ok = False # is this item eligable for rotating?
        self.hash = []  # where hashes are, it should never be erased. NEVER!
        self.zero = ()  # where zero is, erased every time something is moved.
        self.list = []  # list representation of the board, with every element put in. Erased every .write()
        self.xs = []  # where x's are on the board, represented as tuples coordinates. Is erased with zero
        self.relative = []  # where x's are relative to self.zero. Created every time a new file is loaded
        self.columns = width  # width of the board. Never changed
        self.rows = height  # height of the board. Never changed
        self.file = None  # which tetris piece is loaded
        #
        #
        #
        #
        # creates the random list
        self.randlist = []
        temp = [
            "1.txt","1.txt","1.txt","1.txt",
            "2.txt","2.txt","2.txt","2.txt",
            "3.txt","3.txt","3.txt","3.txt",
            "4.txt","4.txt","4.txt","4.txt",
            "5.txt","5.txt","5.txt","5.txt",
            "6.txt","6.txt","6.txt","6.txt",
            "7.txt","7.txt","7.txt","7.txt"
            ]
        all = 28
        for i in range(all):
            all -= 1
            randint = random.randint(0,all)
            self.randlist.append(temp.pop(randint))

        #
        # create a board the size specified
        #
        self.create_list()
        #
        # append lots of lists to self.hash_sort
        for item in range(self.rows):
            self.hash_sort.append([])
        self.hash_original = copy.deepcopy(self.hash_sort)
        self.colors = {
            "1.txt": (255,0,0),
            "2.txt": (255,0,255),
            "3.txt": (255,255,0),
            "4.txt": (0,255,255),
            "5.txt": (0,0,255),
            "6.txt": (160,160,160),
            "7.txt": (0,255,0)
        }



        self.loadfile2()


    def loadfile(self, file):  # loads x's and 0's from a file into self.xs and self.zero
        # clear out the xs and zero and set file to whatever
        self.delete_x()
        self.file = file

        # find the width and length of file and se
        with open(file) as temp:
            width = len(temp.readline().rstrip())
        with open(file) as temp:
            # noinspection PyUnusedLocal
            height = sum(1 for abc in temp)
        if height > self.rows or width > self.columns:
            raise IndexError("File dimensions are too big")

        offset = int((self.columns - height)/2)

        # open file and put x's in it.
        with open(file) as f:
            row = -1
            for line in f:
                row += 1
                col = -1
                for letter in line:
                    col += 1
                    coord = (row, col+offset)
                    if letter == "x":  # if the letter is x, append  a tuple it to .xs
                        self.test(coord)
                        self.xs.append(coord)
                    elif letter == "0":  # do it with 0'x as well
                        self.test(coord)
                        self.zero = coord
            if self.zero:   # if zero exists we create a relative list of tuples
                for coordinate in self.xs:
                    self.relative.append((self.zero[0] - coordinate[0], coordinate[1] - self.zero[1]))
                self.rotate_ok = True
            else:
                self.zero = ()  #  else, we set it as an empty tuple and turn rotating off
                self.rotate_ok = False


        self.write()

    def test(self, tuple):
        if tuple in self.hash:
            self.gameover = True

    def move(self, string):  # moves the string left or right
        if string == "r":
            # create duplicates to test for legality
            _xs = []
            for element in self.xs:
                _xs.append((element[0], element[1] + 1))
            if not self.zero:
                if not self.legal(_xs):
                    self.write()
                    return True
                else:
                    self.xs = _xs
                    self.write()
                    return True


            _zero = (self.zero[0], self.zero[1] + 1)
            if not self.legal(_xs) or not self.legal(_zero):
                self.write()
                return False



            self.xs = _xs
            self.zero = _zero

        elif string == "l":
            # create a duplicate.. to test for legality. No
            _xs = []

            for element in self.xs:
                _xs.append((element[0], element[1] - 1))
                if element[1] - 1 == - 1: # make sure the tetromeno doesnt go through the board
                    self.write()
                    return False

            if not self.zero:
                if self.legal(_xs):
                    self.xs = _xs
                    self.write()
                    return True
                else:
                    self.write()
                    return True

            _zero = (self.zero[0], self.zero[1] - 1)
            if not self.legal(_xs) or not self.legal(_zero):
                self.write()
                return False
            self.xs = _xs
            self.zero = _zero

        else:
            return ("String must be 'r' or 'l', " + "not string")

        self.write()

    def write(self, string = "l"):  # writes the self.xs and self.zero to self.list. putting in any string makes it silent
        #  first, destroy self.list
        self.create_list()

        # and then, put x's in from self.x
        for element in self.xs:
            self.list[element[0]][element[1]] = "x"

        # finally!, put the zero in its location
        if self.zero:  # if it exists
            self.list[self.zero[0]][self.zero[1]] = "0"


        # then, put in the hashes, from self.hash
        if self.hash:
            for element in self.hash:
                self.list[element[0]][element[1]] = "#"

        # FINALLY! NO.2: recreate the relative coordinates in self.relative

        if self.rotate_ok:
            self.relative = []
            for coordinate in self.xs:
                self.relative.append((self.zero[0] - coordinate[0], coordinate[1] - self.zero[1]))

        # and then....



        # finally No.3, check if any rows are full!
        # TODO finish self.delete_rows(), only prints this row is full now.



        #if string == "l":
        #print(self)  # TODO PRINT USED FOR DEBUG

    def __str__(self):
        out = ""
        for line in self.list:
            out += "".join(line) + "\n"
        return out

    def rotate(self, string="r"):  # rotates the board,
        """
        if self.file == "1.txt":
            print(self.xs)
        """

        # first first check if rotating is ok
        if not self.rotate_ok:
            self.write()
            return False
        # first create a temporary object and check if it is legal
        temp = []
        if string == "r":
            for relative in self.relative:
                z, y = relative[0], relative[1]
                temp.append((-y, z))
        elif string == "l":
            for relative in self.relative:
                z, y = relative[0], relative[1]
                temp.append((y, -z))
        else:
            return ("Accepts only 'r' or 'l', not " + string)

        # the temporary object is relative to self.zero, convert it to absolute values
        _xs = convert(temp, self.zero)  # test if it works
        # print(temp, "|", _xs)
        if not self.legal(_xs):
            self.write()
            return False

        self.xs = _xs
        #self.write()
        self.write()

    def remove_x(self, tuple):
        el = -1
        for element in self.xs:
            el += 1
            if element == tuple:
                self.xs.pop(el)

    def legal(self, list_of_tuples):
        if type(list_of_tuples) == tuple:
            if list_of_tuples[0] > self.rows - 1 or list_of_tuples[1] > self.columns - 1:  # if list of tup is a tuple,
                return False

            if list_of_tuples in self.hash:
                return False

            if list_of_tuples[0] < 0 or list_of_tuples[1] < 0:
                return False
            return True

        elif type(list_of_tuples) == list:
            for element in list_of_tuples:
                if element[0] > self.rows - 1 or element[1] > self.columns - 1:  # if list of tup is a tuple,
                    return False

                if element in self.hash:
                    return False

                if element [0] < 0 or element[1] < 0:
                    return False
            # if it passes every thest
            return True
        else:
            raise ValueError ("Here")

    def drop(self):  # drop the tetromeno down by ONE
        # create a copy of .xs
        _xs = []
        for element in self.xs:
            _xs.append((element[0] + 1, element[1]))

        if not self.zero:
            if self.legal(_xs):
                self.xs = _xs
            else:
                self.solidify()
            self.write()
            return "Nozero"
        else:
            _zero = (self.zero[0] + 1, self.zero[1])




        if self.legal(_xs) and self.legal(_zero):  # if the move is not legal for some reason
            self.zero = _zero
            self.xs = _xs

        else:
            self.solidify()



        self.write()

    def solidify(self):
        for element in self.xs:
            self.hash.append((element[0], element[1]))
        if self.zero:
            self.hash.append(self.zero)
        self.delete_x()
        self.delete_rows()







        self.loadfile2() # TODO removetthis

    def create_list(self):  # delete the list and re-initializes it. Mainly used in .write()
        self.list = []
        for foo in range(self.rows):
            temp = []
            for bar in range(self.columns):
                temp.append(".")
            self.list.append(temp)

    def delete_x(self):  # deletes the xs and zero
        self.xs = []
        self.zero = ()

    def check_touch(self):
        # first check if it is at the bottom of the grid
        bottom = self.rows - 1
        for element in self.xs:
            if element[0] >= bottom:
                self.solid_next = True
                return True
        if self.zero:
            if self.zero[0] >= bottom:
                self.solid_next = True
                return True

        for element in self.xs:
            if (element[0] + 1, element[1]) in self.hash:
                return True
        if self.zero:
            if (self.zero[0] + 1, self.zero[1]) in self.hash:
                return True


    def loadfile2(self):
        self.loadfile(self.randlist.pop(0))  # removes the first element of the list

        if len(self.randlist) == 0:
            self.randlist = []
            temp = [
                "1.txt","1.txt","1.txt","1.txt",
                "2.txt","2.txt","2.txt","2.txt",
                "3.txt","3.txt","3.txt","3.txt",
                "4.txt","4.txt","4.txt","4.txt",
                "5.txt","5.txt","5.txt","5.txt",
                "6.txt","6.txt","6.txt","6.txt",
                "7.txt","7.txt","7.txt","7.txt"
            ]
            all = 28
            for i in range(all):
                all -= 1
                randint = random.randint(0,all)
                self.randlist.append(temp.pop(randint))


        if self.randlist:
            #TODO MAKE THIS WORK ! print("Next shape is", self.randlist[0])
            self.next = self.randlist[0]
        else:
            raise Exception ("WHAT THE HELLLE")

    def delete_rows(self):
        # first create hash_sort form x.hash
        self.hash_sort = copy.deepcopy(self.hash_original)
        for element in self.hash:
            self.hash_sort[element[0]].append(element)
        del element

        row = - 1
        for element in self.hash_sort:
            row += 1
            if len(element) == 10:
                print(element, "row" , row, "is full")
                # increase the score by one
                self.score += 1
                # erase the row into a list
                self.hash_sort[row] = []
                #  now update self.hash from self.hash_sort
                self.hash = []
                for element5 in self.hash_sort:
                    if element5:
                        for element6 in element5:
                            self.hash.append(element6)
                # then finally move all the hashes down
                temp = []
                for bar in self.hash:
                    if bar[0] < row:
                        temp.append((bar[0]+1, bar[1]))
                    else:
                        temp.append(bar)
                self.hash = copy.deepcopy(temp)
                del temp

                # finally recreate hash_sort #again...
                self.hash_sort = copy.deepcopy(self.hash_original)
                for element2 in self.hash:
                    self.hash_sort[element2[0]].append(element2)
        self.write("s")






