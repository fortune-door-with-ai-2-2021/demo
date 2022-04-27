import tracemalloc
import time
import random


class solver:
    def __init__(self, board):
        self.board = board
        self.max_level = len(board)
        self.max_ch = len(board[0])
        self.filteredtree = {}

    def a_star(self, tree):
        front = []  # array of dict
        path = []

        front_num = []
        parent_num = []

        front = tree['start']  # expand start to frontier
        path.append('start')

        parent = 'start'
        parent_sub = tree['start']

        # print("front before pop:",front)
        
        ptr = 0
        while ptr < len(front):
            word = front[ptr]
            # print("front[i][4] =='0':", front[ptr][4], "or int(front[i][0:1]):", int(front[ptr][0:1]), "<= int(front[i][5:6]):",int(front[ptr][5:6]))
            if front[ptr][4] =='0' or (front[ptr][4] =='1' and int(front[ptr][5:6]) <= int(front[ptr][0:1])) :
                # print("front[i][4] =='0':", front[i][4], "or int(front[i][0:1]):", int(front[i][0:3]), "<= int(front[i][5:6]):",int(front[i][5:6]))
                front.remove(word)
                ptr = 0
                # print("front after pop:", front)
            ptr += 1 
        # print("front after pop:", front)

        # while()

        for i in range(len(front)):
            # substring from node and convert to int
            front_num.append( pow(int(front[i][7:]), 2) + 1 + int(front[i][7:]) + 1)
        # print("front:", front)
        # print("front_num:", front_num)
        # print("----------")

        for i in range(len(parent_sub)):
            # substring from node and convert to int
            parent_num.append(pow(int(parent_sub[i][7:]), 2) + 1 + int(parent_sub[i][7:]) + 1)
        # print("parent_sub:", parent_sub)
        # print("parent_num:", parent_num)
        # print("----------")

        while(1):

            # print("front_num before least:",front_num)
            least = min(front_num)


            # new path insetad of path of "parent"
            if (min(parent_num) > least):
                path.pop()
            
            # print("++++++++++")
            # print("least:",least)
            # print("front:", front)
            # print("front_num:", front_num)
            parent = front[front_num.index(least)]
            parent_sub = tree[parent]

            
            path.append(parent)
            # print("path:", path)
            # print("----------")

            # print(front[front_num.index(least)])
            # print("dest:", front[front_num.index(least)][4])
            if (front[front_num.index(least)][4] == '3'):
                return path
            
            insert = front_num.index(least)
            front.pop(insert)
            # print("front before remove:", front)
            # print("front_num:", front_num)
            # print("----------")
            # print(insert)
            

            for i in range(len(parent_sub)):
                front.append(parent_sub[i])

            
            front_num.clear()
            parent_num.clear()

            ptr = 0
            while ptr < len(front):
                word = front[ptr]
                # print("front[i][4] =='0':", front[ptr][4], "or int(front[i][0:1]):", int(front[ptr][0:1]), "<= int(front[i][5:6]):",int(front[ptr][5:6]))
                if front[ptr][4] =='0' or (front[ptr][4] =='1' and int(front[ptr][5:6]) <= int(front[ptr][0:1])) :
                # print("front[i][4] =='0':", front[i][4], "or int(front[i][0:1]):", int(front[i][0:3]), "<= int(front[i][5:6]):",int(front[i][5:6]))
                    front.remove(word)
                    ptr = 0
                # print("front after pop:", front)
                ptr += 1 

            for i in range(len(front)):
            # substring from node and convert to int
                front_num.append( pow(int(front[i][7:]), 2) + 1 + int(front[i][7:]) + 1)
            # print("front:", front)
            # print("front_num:", front_num)
            # print("----------")

            for i in range(len(parent_sub)):
            # substring from node and convert to int
                parent_num.append(pow(int(parent_sub[i][7:]), 2) + 1 + int(parent_sub[i][7:]) + 1)
            # print("parent_sub:", parent_sub)
            # print("parent_num:", parent_num)
            # print("----------")

            # print("***************")


            
            
            




    def genFilteredTree(self):
        for a in self.filteredtree.copy():
            for b in self.filteredtree.get(a):
                out = []
                ia = int(b[0:2])    # Level
                ic = int(b[4])      # Door type
                id = int(b[5:7])    # Warped Level
                ie = int(b[7])      # Door Cost
                level = ia
                if ic == 2:
                    level = level + 1
                if ic == 1:
                    if id - 1 > level:
                        level = id - 1
                for c in board[level]:
                    if c[4] == '3':
                        out.append(c)
                        break
                    if c[4] == '2':
                        out.append(c)
                    if c[4] == '1':
                        if int(c[5:]) > level + 1:
                            out.append(c)
                self.filteredtree[b] = out
        return

    def solve(self):
        out = []

        for x in range(self.max_ch):
            if self.board[0][x][4] == '2':
                out.append(self.board[0][x])
            if self.board[0][x][4] == '1':
                if int(self.board[0][x][5:]) > 1:
                    out.append(self.board[0][x])

        self.filteredtree['start'] = out

        for x in range(10):
            self.genFilteredTree()
        print("filtered tree\n",self.filteredtree)
        print("--------------")

        result = self.a_star(self.filteredtree)
        print('PATH TO GOAL FOUNDED!', result)
        return


def print_board():
    i = 0
    for row in board:
        print(i+1, row)
        i += 1
    print("-------------------")


def engine(door_ch):
    # data for the player
    lvl_player = 1  # leved pos. of player
    while(1):
        # choose the door number from 1 to max door.
        num = input("Enter door number, 1 to {} (Press e to give up): ".format(
            door_ch)).strip()  # choose door
        if num == 'e' or num == 'E':
            print("Easy mode activated, please wait AI solving!")
            print_board()
            ai = solver(board)
            start = time.time()
            tracemalloc.start()
            ai.solve()
            end = time.time()
            current, peak = tracemalloc.get_traced_memory()
            print(
                f"Memory usage is {peak / 10**6}MB")
            print("The time of execution of above program is :", end-start)
            break
        elif int(num) in range(1, door_ch+1):
            choose = int(num) - 1
        elif int(num) >= 1 and int(num) <= 5:
            choose = int(num) - 1
            print(num)
        else:
            print('Invalid input, Please try again.')
        # else:
        #     if int(num) in range(1, door_ch+1):
        #         choose = int(num) - 1
        #     else:
        #         print('Invalid input')
        #         continue

        get_type = board[lvl_player - 1][choose].type  # get type of door
        # get dest. level of the door
        get_value = board[lvl_player - 1][choose].value

        if get_type == 0:  # death
            lvl_player = 1
            print("you die, go back to level", lvl_player)
        elif get_type == 1:  # warp
            lvl_player = get_value
            print("you are warped to level", lvl_player)
        elif get_type == 2:  # forward
            lvl_player += 1
            print("you are level", lvl_player)
        elif get_type == 3:  # goal
            print("You win.")
            break
        print("----------")


def genBoard(level, channel):
    matrix = [['00000000' for x in range(level)] for y in range(channel)]
    if channel <= 5:
        maxtypetwo = 1
        maxtypezero = 2
    else:
        maxtypetwo = channel // 5
        maxtypezero = channel // 3

    for d in range(level):
        typeTwoCount = 0
        typeZeroCount = 0
        listtypetwo = []
        listtypezero = []
        for c in range(channel):
            getWarpedLevel = random.randint(1, level)
            matrix[d][c] = str(f"{d:02d}") + \
                str(f"{c:02d}") + '1' + str(f"{getWarpedLevel:02d}") + \
                str(random.randint(1, 5))
            if typeTwoCount <= maxtypetwo:
                getDispatchTypeTwo = random.randint(1, channel)
                listtypetwo.append(getDispatchTypeTwo)
                typeTwoCount += 1
            if typeZeroCount <= maxtypezero:
                getDispatchTypeZero = random.randint(1, channel)
                listtypezero.append(getDispatchTypeZero)
                typeZeroCount += 1
        if d != level - 1:
            for t in listtypetwo:
                ba = matrix[d][t-1]
                matrix[d][t-1] = ba[0] + ba[1] + ba[2] + \
                    ba[3] + '200' + str(random.randint(1, 5))
        for z in listtypezero:
            bb = matrix[d][z-1]
            matrix[d][z-1] = bb[0] + bb[1] + bb[2] + \
                bb[3] + '000' + str(random.randint(1, 5))
        if d == level-1:
            getDispatchTypeThree = random.randint(1, channel)
            bc = matrix[d][getDispatchTypeThree-1]
            matrix[d][getDispatchTypeThree-1] = bc[0] + \
                bc[1] + bc[2] + bc[3] + '300' + str(random.randint(1, 5))
    return matrix


def main():
    global door_ch, lvl_max, board
    # pass for variable access: modify

    door_ch = 10
    lvl_max = 10

    board = genBoard(10, 10)

    while(1):
        text = input("Press p to play, press x to exit: ").strip()
        if text == "p":
            engine(door_ch)
            break
        elif text == "x":
            break
        else:
            print("Please try again.")


if __name__ == "__main__":
    main()

