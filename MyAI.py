# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

	class Tile():
		covered = True
		flag = False
		num = -1

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.board = [[self.Tile() for i in range(rowDimension)] for j in range(colDimension)]
		self.board[startX][startY].covered = False
		self.board[startX][startY].num = 0
		self.parentTile = (startX, startY)
		self.childTile = None
		# self.frontier = []
		# self.frontierTiles = []
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# debugging
	def printTileInfo(self, c: int, r: int):
		if not self.board[c][r].covered:
			print(str(self.board[c][r].num) + ' ', end=" ")
		elif self.board[c][r].flag:
			print('? ', end=" ")
		elif self.board[c][r].covered:
			print('. ', end=" ")

	def printBoard(self):
		board_as_string = ""
		print("", end=" ")
		for r in range(self.rowDimension - 1, -1, -1):
			print(str(r+1).ljust(2) + '|', end=" ")
			for c in range(self.colDimension):
				self.printTileInfo(c, r)
			if (r != 0):
				print('\n', end=" ")
		
		column_label = "     "
		column_border = "   "
		for c in range(1, self.colDimension+1):
			column_border += "---"
			column_label += str(c).ljust(3)
		print(board_as_string)
		print(column_border)
		print(column_label)

	# get covered and unmarked neighbor count
	def getCUN(self, x: int, y: int):
		count = 0
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if x + i >= 0 and x + i < self.rowDimension and y + j >= 0 and y + j < self.colDimension and not (i == 0 and j == 0):
					tile = self.board[x + i][y + j]
					if tile.covered and not tile.flag:
						count += 1
		return count
	
	# get covered and marked neighbor count
	def getCMN(self, x: int, y: int):
		count = 0
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if x + i >= 0 and x + i < self.rowDimension and y + j >= 0 and y + j < self.colDimension and not (i == 0 and j == 0):
					tile = self.board[x + i][y + j]
					if tile.covered and tile.flag:
						count += 1
		return count
	
	# choose valid neighbor and return coords
	def chooseVN(self, x: int, y: int):
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if x + i >= 0 and x + i < self.rowDimension and y + j >= 0 and y + j < self.colDimension and not (i == 0 and j == 0):
					tile = self.board[x + i][y + j]
					if tile.covered and not tile.flag:
						return (x+i, y+j)
					
	# loop through board and return new parent and child
	def newPandC(self):
		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				number = self.board[i][j].num
				cun = self.getCUN(i,j)
				cmn = self.getCMN(i,j)
				if cun > 0 and (number == 0 or number == cmn):
					return (i, j), self.chooseVN(i, j), False
				elif number > 0 and number == cun + cmn and not number == cmn:
					return (i, j), self.chooseVN(i, j), True
		return None, None, None
	
	# loop through board and guess new parent and child based on probability
	def guessNewPandC(self):
		parent, child = None, None
		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				number = self.board[i][j].num
				cun = self.getCUN(i,j)
				if (self.board[i][j].covered == False and cun > 0):
					if parent != None:
						parentNumber = self.board[parent[0]][parent[1]].num
						parentCUN = self.getCUN(parent[0], parent[1])
					if parent == None or number < parentNumber or (number == parentNumber and cun > parentCUN):
						parent = (i,j)
						child = self.chooseVN(i,j)
		return parent, child


	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		#self.printBoard()

		px, py = self.parentTile[0], self.parentTile[1]
		pnum = self.board[px][py].num
		cun = self.getCUN(px,py)
		cmn = self.getCMN(px,py)

		if (self.childTile != None):
			self.board[self.childTile[0]][self.childTile[1]].num = number

		if cun == 0:
			self.parentTile, self.childTile, flag = self.newPandC()
			if flag == None:	# ambiguous case
				self.parentTile, self.childTile = self.guessNewPandC()
				if self.parentTile == None:		# game is done, no more tiles left to uncover
					return Action(AI.Action.LEAVE)
				self.board[self.childTile[0]][self.childTile[1]].covered = False
				return Action(AI.Action.UNCOVER, self.childTile[0], self.childTile[1])
			if flag: 
				self.board[self.childTile[0]][self.childTile[1]].flag = True
				return Action(AI.Action.FLAG, self.childTile[0], self.childTile[1])
			else: 
				self.board[self.childTile[0]][self.childTile[1]].covered = False
				return Action(AI.Action.UNCOVER, self.childTile[0], self.childTile[1])

		if pnum == 0 or pnum == cmn:
			self.childTile = self.chooseVN(px,py)
			self.board[self.childTile[0]][self.childTile[1]].covered = False
			return Action(AI.Action.UNCOVER, self.childTile[0], self.childTile[1])
		
		if pnum == cun + cmn:
			self.childTile = self.chooseVN(px,py)
			self.board[self.childTile[0]][self.childTile[1]].flag = True
			return Action(AI.Action.FLAG, self.childTile[0], self.childTile[1])
		
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
