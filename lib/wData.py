# wData.py

import datetime

class loc_data:

	def __init__(self, locName, wDatas):
		self.locName = locName
		sorted(wDatas,key= lambda wdata:wdata.startDateTime)
		self.wDatas = wDatas


	# get a list of weather info between timeRange(startTime,endTime)
	def getWx(timeRange):
		pass

	# get a list of max temp data between timeRange(startTime,endTime)
	def getMaxT(timeRange):
		pass

	# get a list of min temp data between timeRange(startTime,endTime)
	def getMinT(timeRange):
		pass

	def getLocName():
		return self.locName


class wData:

	def __init__(self,startDate,startTime,endDate,endTime,wx='',maxT=0,minT=0):
		
		self.startDate = startDate
		self.startTime = startTime
		self.endDate = endDate
		self.endTime = endTime

		self.wx = wx
		self.maxT = maxT
		self.minT = minT

		self.timeSection = timeAMorPM(startTime)

	def timeAMorPM(time):
		if time.hour >= 12:
			return 'PM'
		else :
			return 'AM'