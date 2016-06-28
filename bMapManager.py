#20160625
#Author: Robert H Cudmore
#Web: http://robertcudmore.org

#for ipython notebook
'''
%matplotlib inline
from plotly.offline import init_notebook_mode
init_notebook_mode() # run at the start of every ipython notebook to use plotly.offline
'''

import os, math
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.dates as md
#from matplotlib.patches import Rectangle

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#import plotly as py
from plotly.graph_objs import Scatter, Layout

#for ipython notebook
#init_notebook_mode() # run at the start of every ipython notebook to use plotly.offline

import tifffile #requires pip install tifffile

class bStack():
	def __init__(self, path='', filePrefix=''):
		self.path = ''
		self.prefix = ''
		self.stackdb = []
		self.line = []
		self.int1 = []
		self.int2 = []

		self.header = {}
		
		self.data = None
		
		if path and filePrefix:
			self.load(path, filePrefix)
			
	def load(self, path, filePrefix):
		'''
		load map manager files from disk (does not load .tif stacks
		'''
		
		#check if path exists

		self.path = path
		self.prefix = filePrefix

		#load stackdb
		stackdbFile = filePrefix + '_db2.txt'
		filepath = path + '/stackdb/' + stackdbFile
		
		header = self.loadHeader(filepath)
		self.header['voxelx'] = header['voxelx']
		self.header['voxely'] = header['voxely']
		self.header['voxelz'] = header['voxelz']
		
		self.stackdb = pd.read_csv(
			filepath,
			header=1)
		
		#load line
		lineFile = filePrefix + '_l.txt'
		filepath = path + '/line/' + lineFile
		header = self.loadHeader(filepath)
		numHeaderRow = int(header['numHeaderRow'])
		numHeaderRow += 2 # 1 for file header, 1 for linedb header
		self.line = pd.read_csv(
			filepath,
			header=numHeaderRow)
		
		#load int 1
		intFile = filePrefix + '_Int1.txt'
		filepath = path + '/stackdb/' + intFile
		self.int1 = pd.read_csv(
			filepath,
			header=1)

		#load int 1
		#IMPLEMENT THIS

	def loadHeader(self, filePath):
		#read header as dict
		with open(filePath, 'U') as f:
			header = f.readline()
		header = header.rstrip()
		if header.endswith(','):
			header = header[:-1] #remove last char ','
		if header.endswith(';'):
			header = header[:-1] #remove last char ';'
		d = dict(s.split('=') for s in header.split(';'))
		return d
			
	def loadtiff(self):
		'''
		for a single stack, .tif is just /Raw/ + self.prefix + '.tif'
		for a map, we need to know session
		for a5n (bSPine), i20110331_a5n_s0_ch1
		'''
		specialPrefix = ''
		if self.prefix.startswith('a5n_'):
			specialPrefix = 	'i20110331_'
		ch1path = self.path + '/Raw/' + specialPrefix + self.prefix + '_ch1.tif'
		if not os.path.isfile(ch1path):
			print 'ERROR: bStack.loadtiff() did not find:', ch1path
			return
		self.data = tifffile.imread(ch1path)
		print 'bStack.loadtiff() loaded', ch1path, 'shape:', self.data.shape, 'dtype:', self.data.dtype
		
	def unloadtiff(self):
		self.data = None
	
	def getSlice(self, num):

		# check sanity of slice num
		if num>=0 and num < self.data.shape[0]-1:
			return self.data[num]
		else:
			return None
					
	def printInfo(self):
		print 'prefix:', self.prefix
		print '   dx,dy,dz:', self.header['voxelx'],self.header['voxely'],self.header['voxelz']
		print '   pnts:', self.numPoints()
		print '   spines:', len(self.getSpines())
		print '   segments:', self.numSegments()
	 
	def numPoints(self): return len(self.stackdb.index)
	#def getStackdb(self,col): return self.stackdb[col]
	
	def getSpines(self, parentID=None):
		return self.getObj(roiType='spineROI', parentID=parentID)

	def getSpinesInt(self, parentID=None):
		objIdx = self.getObj(roiType='spineROI',parentID=parentID).index.tolist()
		return self.int1.loc[objIdx]

	def getObj(self, roiType='spineROI', parentID=None):
		obj = self.stackdb[self.stackdb['roiType']==roiType]
		if parentID>=0:
			obj = obj[obj['parentID']==parentID]
		return obj
	
	def getLine(self, parentID=None):
		obj = self.line
		if parentID>=0:
			obj = obj[obj['ID']==parentID]
		return obj
	
	def numSegments(self):
		#make numSegments a data member and calculate once on load
		df2=self.stackdb[self.stackdb['parentID'] >=0]
		numSeg = max(df2['parentID']) - min(df2['parentID']) + 1
		return math.trunc(numSeg)

	def getMask(self,z, parentID=None):
		#df[df.c > 0.5][['b', 'e']].values
		zTop = z - 1
		zBottom = z + 1
		spines = self.getSpines(parentID=parentID)
		ret = spines[(spines.z >= zTop) & (spines.z <= zTop)][['x','y','z']].values
		return ret
		
class bStackPlot():
	def __init__(self, stack):
		self.stack = stack

	def plot(self, roiType='spineROI', parentID=None, xStat='x', yStat='y'):
		obj = self.stack.getObj(roiType=roiType, parentID=parentID)
		plt.scatter(obj[xStat], obj[yStat])
		plt.ylabel(yStat)
		plt.xlabel(xStat)


	def plotLine(self, roiType='spineROI', parentID=None, xStat='x', yStat='y'):
		obj = self.stack.getLine(parentID=parentID)
		plt.scatter(obj[xStat], obj[yStat])
		plt.ylabel(yStat)
		plt.xlabel(xStat)


	def plotInt(self, roiType='spineROI', parentID=None, yStat='sSum', xStat='dSum'):
		objIdx = self.stack.getObj(roiType=roiType,parentID=parentID).index.tolist()
		tmpInt = self.stack.int1.loc[objIdx]
		plt.scatter(tmpInt[xStat], tmpInt[yStat])
		plt.ylabel(yStat)
		plt.xlabel(xStat)
		
	def plotly(self, roiType='spineROI', parentID=None, xStat='x', yStat='y'):
		obj = self.stack.getObj(roiType=roiType, parentID=parentID)

		fig = {
			'data': [
			{
			'x': obj[xStat], 
			'y': obj[yStat], 
			'text': '', 
			'mode': 'markers', 
			'name': '2007'
			},
			],
			'layout': {
			#'xaxis': {'title': 'GDP per Capita', 'type': 'log'},
			'xaxis': {'title': xStat},
			'yaxis': {'title': yStat},
			'height': 400,
			'width': 400,
			}
			}

		iplot(fig)

		#py.iplot(fig, filename='pandas/multiple-scatter')
		#url = py.plot(fig, filename='myscatter')
		#print url


class bMap():
	def __init__(self, path=''):
		self.stackList = []
		if path:
			self.load(path)
			
	def load(self,path):
		'''
		loads a map manager map, a map is a sequence of stacks
		does NOT load .tif stacks
		'''
		
		#path is path to map folder, it contains folders for (stackdb, line)
		
		#check if path exists
		
		#load stackdb
		stackdb_dir = os.listdir(path + '/stackdb')
		for file in stackdb_dir:
			#files ending in _db2.txt are stackdb files
			if file.endswith('_db2.txt'):
				#print 'loading file:', file
				stackPrefix = file.replace('_db2.txt','')
				#this does not work because aStack is only local?
				#aStack = bStack()
				#aStack = aStack.load(path, stackPrefix)
				self.stackList.append(bStack())
				self.stackList[-1].load(path, stackPrefix)
				
	def printInfo(self):
		print 'number of timepoints:', self.numTimepoints()
		for stack in self.stackList:
			print stack.printInfo()
			
	def numTimepoints(self): return len(self.stackList)
	def stacks(self): return self.stackList
	
	def loadtiff(self, tp):
		self.stacklist[tp].loadtiff()
		