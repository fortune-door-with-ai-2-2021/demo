class door:
	def __init__(self, type = None, value = 0):
		self.type = type	# 0 = death, 1 = warp, 2 = forward, 3 = goal (last level only)
		self.value = value		# 1 <= value <= door_ch, 0 when door != warp

	def __repr__(self):	#print value of doors	(t,v)
		mess = ""
		mess += "(" + str(self.type)

		if self.type == 1:
			mess += "," + str(self.value)
		
		mess += ")"

		return mess

# default size is 0
lvl_max = 0
door_ch = 0


#data for the player
lvl_player = 1 #leved pos. of player
get_goal = False #are you the goal

board = [] #map

def create_board(): #create map with 2d array
	global board
	board = [ [ door() for i in range(door_ch) ] for j in range(lvl_max) ]
	#column x row

def print_board():

	i = 0

	for row in board:
		print(i,row)
		i += 1
	print("----------")


def main():
	global door_ch, lvl_max, board, lvl_player, board
	# pass for variable access: modify

	while(1):
		# choose game mode
		text = input("Choose your mode, Easy(e) or Hard(h): ").strip()
		
		# convert to lower alphabet
		mess = text.lower()

		# input must be a character thai is "e" or "h" and length = 1.
		if len(mess) == 1 and (mess == "e" or mess == "h"):
			print("You chose mode:",mess)
			break #if condition is all true, exit from the loop

		print("Please try again.") # if condition is false

		
	# set the map size by mode 

	# if mess == "e":
	# 	door_ch = 3
	# 	lvl_max = 4
	if mess == "h": #for demo version only
	# elif mess == "h":
		door_ch = 5
		lvl_max = 10

	create_board()		

	# create_board()
	print_board()

	# random zone, in this point, use temp level.
	board[0] = [door(0), door(1,4), door(1,1), door(1,8), door(2)]
	board[1] = [door(0), door(2), door(1,1), door(1,9), door(0)]
	board[2] = [door(0), door(1,4), door(1,1), door(1,9), door(0)]
	board[3] = [door(0), door(1,4), door(1,1), door(2), door(0)]
	board[4] = [door(0), door(1,4), door(2), door(1,9), door(0)]
	board[5] = [door(0), door(1,4), door(1,1), door(1,9), door(2)]
	board[6] = [door(0), door(1,4), door(1,1), door(1,9), door(2)]
	board[7] = [door(2), door(1,4), door(1,1), door(1,9), door(0)]
	board[8] = [door(0), door(1,4), door(2), door(1,9), door(0)]
	board[9] = [door(0), door(1,1), door(3), door(1,9), door(0)]
	# end of temp level zone

	print_board()

	while(1):
		while(1):
			# choose the door number from 1 to max door.
			num = input("Enter your door number, from 1 to {}: ".format(door_ch) ).strip() #choose door
			if len(num) == 1 and num.isdecimal():
				choose = int(num) - 1 # convert to index interval -> 0 to max_door - 1
				if choose >= 0 and choose < door_ch:
					break
			print("Please try again.")

		get_type = board[lvl_player - 1][choose].type #get type of door
		get_value = board[lvl_player - 1][choose].value #get dest. level of the door
		
		if get_type == 0: #death
			lvl_player = 1
			print("you die, go back to level",lvl_player)
		elif get_type == 1: #warp
			lvl_player = get_value
			print("you are warped to level",lvl_player)
		elif get_type == 2: #forward
			lvl_player += 1
			print("you are level",lvl_player)
		elif get_type == 3: #goal
			print("You win.")
			break
	
		print("----------")

			
if __name__ == "__main__":
    main()
