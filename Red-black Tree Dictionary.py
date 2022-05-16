import enum
from time import sleep


class Colour(enum.Enum):
    RED = 1
    BLACK = 2


def proceed():
    answer = int(input('Do you wish to proceed ? (1 or 0): '))
    if answer == 1:
        print("\n" * 100)
    elif answer == 0:
        exit()


def menu_selection():
    print('-------------------DICTIONARY MENU--------------------')
    print('Select a choice regarding operations on the dictionary')
    print('1-Insert a word')
    print('2-Look up a word')
    print('3-Dictionary size')
    print('4-Tree height')
    print('------------------------------------------------------')


def menu_operation_manager():
    choice = int(input())
    if choice == 1:
        word = input('Enter word you wish to enter: ')
        exist = RedBlackTree.search(RedBlackTree.root, word)
        if exist is False:
            RedBlackTree.insert(RedBlackTree.root, word, None)
        elif exist is True:
            print('ERROR: Word already in dictionary!')
    elif choice == 2:
        word = input('Enter word you wish to search for: ')
        RedBlackTree.search(RedBlackTree.root, word)
    elif choice == 3:
        RedBlackTree.print_tree_size()
    elif choice == 4:
        RedBlackTree.print_tree_height()
    print('----------------------------------------------')
    RedBlackTree.print_tree_size()
    RedBlackTree.print_tree_height()


class Node:
    def __init__(self, data, parent, left, right, colour):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        self.colour = colour


class RedBlackTree:
    root = Node(None, None, None, None, None)
    tree_size = 1

    def __init__(self):
        self.self = self
        RedBlackTree.root.colour = Colour.BLACK
        RedBlackTree.root.left = Node(None, RedBlackTree.root, None, None, Colour.BLACK)
        RedBlackTree.root.right = Node(None, RedBlackTree.root, None, None, Colour.BLACK)

    @classmethod
    def insert(cls, root, data, parent_temp):
        temp = root
        if parent_temp is None:
            RedBlackTree.tree_size += 1
        if temp.data.lower() < data.lower():
            if temp.right.data is None:
                temp.right = Node(data, temp, None, None, Colour.RED)
                temp.right.left = Node(None, temp.right, None, None, Colour.BLACK)
                temp.right.right = Node(None, temp.right, None, None, Colour.BLACK)
                RedBlackTree.fix_insert(temp.right)
            else:
                RedBlackTree.insert(temp.right, data, temp)
        else:
            if temp.left.data is None:
                temp.left = Node(data, temp, None, None, Colour.RED)
                temp.left.left = Node(None, temp.left, None, None, Colour.BLACK)
                temp.left.right = Node(None, temp.left, None, None, Colour.BLACK)
                RedBlackTree.fix_insert(temp.left)
            else:
                RedBlackTree.insert(temp.left, data, temp)

    @classmethod
    def tree_height(cls, root):
        temp = root
        if temp.data is None:  # tree height calculates the number of nodes excluding the NULL nodes
            return 0
        left_height = RedBlackTree.tree_height(temp.left)
        right_height = RedBlackTree.tree_height(temp.right)
        return max(left_height, right_height) + 1

    @classmethod
    def search(cls, root, data):
        temp = root
        if temp.data.lower() == data.lower():
            print('YES')
            return True
        elif temp.data.lower() < data.lower():
            if temp.right.data is not None:
                return RedBlackTree.search(temp.right, data)
            else:
                print('NO')
                return False
        elif temp.data.lower() > data.lower():
            if temp.left.data is not None:
                return RedBlackTree.search(temp.left, data)
            else:
                print('NO')
                return False

    @classmethod
    def load_tree(cls):
        print('Loading Dictionary .........')
        temp = RedBlackTree.root
        f = open('EN-US-Dictionary.txt', 'r')
        text = f.readline().rstrip('\n')
        initial = True
        while text != '':
            if initial is True:
                temp.data = text
                initial = False
            else:
                RedBlackTree.insert(RedBlackTree.root, text, None)
            text = f.readline().rstrip('\n')
        print('')
        print('**** Dictionary loaded successfully ****')
        print('')
        sleep(1)

    @classmethod
    def fix_insert(cls, k):
        while k.parent.colour == Colour.RED:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.colour == Colour.RED:
                    u.colour = Colour.BLACK
                    k.parent.colour = Colour.BLACK
                    k.parent.parent.colour = Colour.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        RedBlackTree.right_rotate(k)
                    k.parent.colour = Colour.BLACK
                    k.parent.parent.colour = Colour.RED
                    RedBlackTree.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.colour == Colour.RED:
                    u.colour = Colour.BLACK
                    k.parent.colour = Colour.BLACK
                    k.parent.parent.colour = Colour.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        RedBlackTree.left_rotate(k)
                    k.parent.colour = Colour.BLACK
                    k.parent.parent.colour = Colour.RED
                    RedBlackTree.right_rotate(k.parent.parent)
            if k == RedBlackTree.root:
                break
        RedBlackTree.root.colour = Colour.BLACK

    @classmethod
    def left_rotate(cls, x):
        y = x.right
        x.right = y.left
        if y.left.data is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            RedBlackTree.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    @classmethod
    def right_rotate(cls, x):
        y = x.left
        x.left = y.right
        if y.right.data is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            RedBlackTree.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    @classmethod
    def print_tree_size(cls):
        print('Number of nodes in tree is equal to ' + str(RedBlackTree.tree_size))

    @classmethod
    def print_tree_height(cls):
        print('Height of tree is equal to ' + str(RedBlackTree.tree_height(RedBlackTree.root)))


# main code
T = RedBlackTree()
T.load_tree()
while True:
    menu_selection()
    menu_operation_manager()
    proceed()
