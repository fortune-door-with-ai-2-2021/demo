import random
import tracemalloc
import time


class solver:
    def __init__(self, board):
        self.board = board
        self.max_depth = 0
        self.max_level = len(board)
        self.max_ch = len(board[0])

    def depthLimitedSearch(self, max_depth, depth=0, level=0, channel=1):
        if depth == max_depth:
            if board[level][channel-1][4] == '3':
                print('\n***GOAL FOUND***\n')
                return [board[level][channel-1]]

        else:
            for c in range(1, self.max_ch+1):
                if board[level][c-1][4] == '2':
                    path = self.depthLimitedSearch(
                        max_depth, depth+1, level+1, c)
                    if path:
                        return [board[level][c-1]] + path
                if board[level][c-1][4] == '1' and int(board[level][c-1][5:])-1 > level:
                    path = self.depthLimitedSearch(
                        max_depth, depth+1, int(board[level][c-1][5:])-1, c)
                    if path:
                        return [board[level][c-1]] + path
                if board[level][c-1][4] == '3':
                    print('\n***GOAL FOUND***\n')
                    return [board[level][c-1]]

    def solve(self):
        # self.max_level+1
        for i in range(10):
            self.max_depth = i
            rpath = self.depthLimitedSearch(self.max_depth)
            if rpath:
                return rpath


def print_board():
    i = 0
    for row in board:
        print(i+1, row)
        i += 1
    print("----------")


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
            print('PATH-TO-GOAL ' + str(ai.solve()))
            end = time.time()
            current, peak = tracemalloc.get_traced_memory()
            print(
                f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
            tracemalloc.stop()
            print("The time of execution of above program is :", end-start)
            break
        elif int(num) in range(1, door_ch+1):
            choose = int(num) - 1
        elif int(num) >= 1 and int(num) <= 5:
            choose = int(num) - 1
            print(num)
        else:
            print('Invalid input, Please try again.')
            continue
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
