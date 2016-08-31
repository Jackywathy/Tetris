class twoDimArray:
    def __init__(self,x,y,start='*'):
        self.width = x
        self.height = y
        self.array = [[start]*x for _i in range(y)]
        # when indexing, y is first then x

    def get(self,x,y):
        return self.array[y][x]

    def get_tuple(self,x_y_tuple):
        return self.array[x_y_tuple[1]][x_y_tuple[0]]

    def get_multiple(self, arglist):
        ret = []
        for i in arglist:
            if isinstance(i, tuple) or isinstance(i, list):
                ret.append(self.get_tuple(i))
            else:
                raise BaseException(i,"Is NOT A TUPLE OR LIST!!!!!!!")
        return ret


    def set_tuple(self,*args):
        """Tuples must be (x,y,item)"""
        for i in args:
            x,y,item = i
            if x < 0 or y < 0:
                print('Negative x or y')
                raise Exception
            else:
                try:
                    self.array[y][x] = item
                except IndexError:
                    print(i, 'is TOO BIG')
                    raise

    def set_tuple_item(self,item,*args):
        """Tuples must be (x,y), item must be specified"""
        for i in args:
            x,y = i
            if x < 0 or y < 0:
                print('Negative x or y')
                raise Exception
            else:
                try:
                    self.array[y][x] = item
                except IndexError:
                    print(i, 'is TOO BIG')
                    raise

    def __str__(self):
        return self.__repr__()#'\n'.join(list(map(' '.join,self.array)))
    def __repr__(self):
        return "[] (%d x %d)" % (self.width, self.height)

    def set(self, x,y,item):
        if x < 0 or y < 0:
            print('Negative x or y')
            raise Exception
        else:
            try:
                self.array[y][x] = item
            except IndexError:
                    print(x,y,item, 'is TOO BIG')
                    raise
    def getArray(self):
        return self.array


def bin_search(sortedlist, item):
    first = 0
    last = len(sortedlist)-1
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        if sortedlist[midpoint] == item:
            found = True
        else:
            if item < sortedlist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1

    return found


with open('input.txt','r',encoding='UTF8') as f:
    length = int(f.readline())
    for line in f:
        ...
with open("out.txt", 'w', encoding='UTF8') as f:
    ...

