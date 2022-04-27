import tracemalloc
import time
import random


class solver:
    def __init__(self, board):
        self.board = board
        self.max_level = len(board)
        self.max_ch = len(board[0])
        self.filteredtree = {}

    def breadthFirstSearch(self, start):
        # maintain a queue of paths
        queue = []
        # push the first path into the queue
        queue.append([start])
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            # get the last node from the path
            node = path[-1]
            # path found
            if node[4] == '3':
                return path
            # enumerate all adjacent nodes, construct a
            # new path and push it into the queue
            for adjacent in self.filteredtree.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
        return

    def genFilteredTree(self):
        for a in self.filteredtree.copy():
            for b in self.filteredtree.get(a):
                out = []
                ia = int(b[0:2])  # Level
                ic = int(b[4])   # Door type
                id = int(b[5:])  # Warped Level
                # print('ia:', ia, '| ic:', ic, '| id:', id)
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

        result = self.breadthFirstSearch('start')
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
    matrix = [['0000000' for x in range(level)] for y in range(channel)]
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
                str(f"{c:02d}") + '1' + str(f"{getWarpedLevel:02d}")
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
                matrix[d][t-1] = ba[0] + ba[1] + ba[2] + ba[3] + '200'
        for z in listtypezero:
            bb = matrix[d][z-1]
            matrix[d][z-1] = bb[0] + bb[1] + bb[2] + bb[3] + '000'
        if d == level-1:
            getDispatchTypeThree = random.randint(1, channel)
            bc = matrix[d][getDispatchTypeThree-1]
            matrix[d][getDispatchTypeThree-1] = bc[0] + \
                bc[1] + bc[2] + bc[3] + '300'
    return matrix


def main():
    global door_ch, lvl_max, board
    # pass for variable access: modify

    door_ch = 50
    lvl_max = 50

    board = genBoard(50, 50)

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
