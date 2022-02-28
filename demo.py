import random


class door:
    def __init__(self, type=None, value=0):
        # 0 = death, 1 = warp, 2 = forward, 3 = goal (last level only)
        self.type = type
        self.value = value		# 1 <= value <= door_ch, 0 when door != warp

    def __repr__(self):  # print value of doors	(t,v)
        mess = ""
        mess += "(" + str(self.type)

        if self.type == 1:
            mess += "," + str(self.value)

        mess += ")"

        return mess


class solver:
    def __init__(self, board):
        self.board = board
        self.max_depth = 0
        self.max_level = len(board)
        self.max_ch = len(board[0])

    def depthLimitedSearch(self, max_depth, depth=0, level=0, channel=1):
        if depth == max_depth:
            print('Max depth reached:', depth, '\n')
            if board[level][channel-1].type == 3:
                print('\n***GOAL FOUND***\n')
                return [channel]

        else:
            for c in range(1, self.max_ch+1):
                print('Max depth:', max_depth, '| Depth:',
                      depth, '| Level:', level, '| Channel:', c)
                if board[level][c-1].type == 2:
                    # print('Max depth:', max_depth, '| Depth:', depth, '| Level:', level, '| Channel:', c)
                    print('<<Forward>>')
                    path = self.depthLimitedSearch(
                        max_depth, depth+1, level+1, c)
                    if path:
                        return [c] + path
                if board[level][c-1].type == 1 and board[level][c-1].value-1 > level:
                    # print('Max depth:', max_depth, '| Depth:', depth, '| Level:', level, '| Channel:', c)
                    print('<<Warp to level', board[level][c-1].value-1, '>>')
                    path = self.depthLimitedSearch(
                        max_depth, depth+1, board[level][c-1].value-1, c)
                    if path:
                        return [c] + path
                if board[level][c-1].type == 3:
                    print('\n***GOAL FOUND***\n')
                    return [c]

    def solve(self):
        # self.max_level+1
        for i in range(1, 5):
            self.max_depth = i
            print('\n***MAX DEPTH HAS BEEN INCREASED***\n')
            rpath = self.depthLimitedSearch(self.max_depth)
            if rpath:
                return rpath
            else:
                print('Path not found')


def create_board():  # create map with 2d array
    global board
    board = [[door() for i in range(door_ch)] for j in range(lvl_max)]
    # column x row


def print_board():
    i = 0
    for row in board:
        print(i + 1, row)
        i += 1
    print("----------")


def engine(door_ch):
    # data for the player
    lvl_player = 1  # leved pos. of player
    while(1):
        # choose the door number from 1 to max door.
        num = input("Enter door number, 1 to {} (Press e for help): ".format(
            door_ch)).strip()  # choose door
        if num == 'e':
            print("Easy mode activated :)")
            print_board()
            ai = solver(board)
            print('PATH-TO-GOAL ' + str(ai.solve()))
            break
        else:
            if int(num) in range(1, door_ch+1):
                choose = int(num) - 1
            else:
                print('Invalid input')
                continue

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


def main():
    global door_ch, lvl_max, board
    # pass for variable access: modify

    door_ch = 5
    lvl_max = 10

    create_board()

    warp_target1, warp_target2, warp_target3 = random.randrange(
        1, lvl_max-1), random.randrange(1, lvl_max-1), random.randrange(1, lvl_max-1)

    # random zone, in this point, use temp level.
    board[0] = [door(0), door(1, warp_target1), door(
        1, warp_target2), door(1, warp_target3), door(2)]
    board[1] = [door(0), door(2), door(1, warp_target2),
                door(1, warp_target3), door(0)]
    board[2] = [door(0), door(1, warp_target1), door(
        1, warp_target2), door(1, warp_target3), door(0)]
    board[3] = [door(0), door(1, warp_target1), door(
        1, warp_target2), door(2), door(0)]
    board[4] = [door(0), door(1, warp_target1), door(2),
                door(1, warp_target3), door(0)]
    board[5] = [door(0), door(1, warp_target1), door(
        1, warp_target2), door(1, warp_target3), door(2)]
    board[6] = [door(0), door(1, warp_target1), door(
        1, warp_target2), door(1, warp_target3), door(2)]
    board[7] = [door(2), door(1, warp_target1), door(
        1, warp_target2), door(1, warp_target3), door(0)]
    board[8] = [door(0), door(1, warp_target1), door(2),
                door(1, warp_target3), door(0)]
    board[9] = [door(0), door(1, warp_target2), door(3),
                door(1, warp_target3), door(0)]
    # end of temp level zone

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
