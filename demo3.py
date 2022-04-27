import tracemalloc
import time


class solver:
    def __init__(self, board):
        self.board = board
        self.max_level = len(board)
        self.max_ch = len(board[0])
        self.filteredtree = {}

    def breadthFirstSearch(self, start, end):
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
            if node == end:
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
                ia = int(b[0])
                ic = int(b[2])
                id = int(b[3])
                level = ia
                if ic == 2:
                    level = level + 1
                if ic == 1:
                    if id - 1 > level:
                        level = id - 1
                for c in board[level]:
                    if c[2] == '3':
                        out.append(c)
                        break
                    if c[2] == '2':
                        out.append(c)
                    if c[2] == '1':
                        if int(c[3]) > level + 1:
                            out.append(c)
                self.filteredtree[b] = out
        return

    def solve(self):
        out = []

        for x in range(5):
            if self.board[0][x][2] == '2':
                out.append(self.board[0][x])
            if self.board[0][x][2] == '1':
                if int(self.board[0][x][3]) > 1:
                    out.append(self.board[0][x])

        self.filteredtree['start'] = out

        for x in range(10):
            self.genFilteredTree()

        print(self.filteredtree, '\n')

        result = self.breadthFirstSearch('start', '9130')
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
        try:
            if num == 'e' or num == 'E':
                print("Easy mode activated :)")
                print_board()
                ai = solver(board)
                start = time.time()
                tracemalloc.start()
                ai.solve()
                end = time.time()
                current, peak = tracemalloc.get_traced_memory()
                print(
                    f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
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
        except:
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


def main():
    global door_ch, lvl_max, board
    # pass for variable access: modify

    door_ch = 5
    lvl_max = 10

    board = [
        ['0000', '0114', '0211', '0318', '0420'],
        ['1000', '1120', '1211', '1319', '1400'],
        ['2000', '2114', '2211', '2319', '2400'],
        ['3000', '3114', '3211', '3320', '3400'],
        ['4000', '4114', '4220', '4319', '4400'],
        ['5000', '5114', '5211', '5319', '5420'],
        ['6000', '6114', '6211', '6319', '6420'],
        ['7020', '7114', '7211', '7319', '7400'],
        ['8000', '8114', '8220', '8319', '8400'],
        ['9000', '9130', '9211', '9319', '9400']
    ]

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
