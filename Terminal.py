import History
import sys

class TColumn:


	def __init__(self, colNum, totalSegs):
		self.tabSize = 20
		self.segDownloaded = []
		self.toalSegs = totalSegs
		self.activities = []
		self.activityCounter = 0
		self.colNum = colNum
		self.printSegs = False
		self.history = History.History()

	def reachedEnd(self):
		return self.activityCounter == len(self.activities)-1

	def getTabSize(self):
		return " " * self.tabSize * self.colNum

	def update(self):
		self.activities = self.history.getHistory(self.colNum)
		#print self.activities

	def __gt__(self,other):
		if not isinstance(other,TColumn):
			raise Exception("Incomparable")
			sys.exit(1)
		if self.reachedEnd():
			return True
		return self.getTopTimestamp() > other.getTopTimestamp()

	def __lt__(self,other):
		if not isinstance(other,TColumn):
			raise Exception("Incomparable")
		if self.reachedEnd():
			return False
		return self.getTopTimestamp() < other.getTopTimestamp()

	def getTopTimestamp(self):
		return self.activities[self.activityCounter][0]

	def addSegment(self, segId):
		self.segDownloaded.append(segId)

	def __str__(self):
		if self.printSegs:
			return self.getTabSize() + str(self.segDownloaded)
			self.printSegs = False
		else:
			self.activityCounter += 1
			return self.getTabSize()  + str(self.activities[self.activityCounter-1][1])


class Terminal :

	def __init__(self, numProcs, numSegs):
		self.numProcs = numProcs
		self.numSegs = numSegs
		self.columns = []
		self.initColumns()

	def initColumns(self):
		self.columns = [ TColumn(numProc, self.numSegs) for numProc in range(self.numProcs) ]

	def update(self):
		for col in self.columns:
			col.update()

	def show(self):
		print "show"
		while True:
			#print [str(x) for x in self.columns]
			#sys.exit(1)
			nColumn = self.findNextColumn()
			if  nColumn:
				print str(nColumn)
			else:
				break


	def findNextColumn(self):
		nextCol = self.columns[0]
		for col in self.columns[1:]:
			if col < nextCol:
				nextCol = col		
		return nextCol