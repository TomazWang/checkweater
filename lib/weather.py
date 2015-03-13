# coding=utf-8
# weather.py

import urllib.request as urllib2
import xml.etree.ElementTree as ET
import datetime
import wData

# api from CWB, Central Weather Bureau
# 一週縣市天氣預報
wApiUrl = 'http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-005.xml' 

# Tags
NAMESPACE = '{urn:cwb:gov:tw:cwbcommon:0.1}'
TAG_dataset = NAMESPACE+'dataset'
TAG_location = NAMESPACE+'location'
TAG_locationName = NAMESPACE+'locationName'
TAG_weatherElement = NAMESPACE+'weatherElement'
TAG_elementName = NAMESPACE+'elementName'
TAG_time = NAMESPACE+'time'
TAG_startTime = NAMESPACE+'startTime'
TAG_endTime = NAMESPACE+'endTime'
TAG_parameter = NAMESPACE+'parameter'
TAG_parameterName = NAMESPACE+'parameterName'
TAG_parameterValue = NAMESPACE+'parameterValue'
TAG_parameterUnit = NAMESPACE+'parameterUnit'

E_TYPE_Wx = 'Wx'
E_TYPE_MaxT = 'MaxT'
E_TYPE_MinT = 'MinT'


# getWeatherDate return a list of loc_data
def getWeatherData():
	xml = getRawXml()
	return parsingXml(xml)



# get raw xml data from CWB
def getRawXml():
	response = urllib2.urlopen(wApiUrl)
	xml  = response.read()
	return xml

# parsing xml into a list of loc_data
def parsingXml(xml):

	root = ET.fromstring(xml)
	dataset = root.find('.//'+TAG_dataset)

	# a empty list of location data (loc_data)
	locDatas = []

	allLocation = dataset.findall(TAG_location)

	for loc in allLocation:
	# 1. get loc_name
	# 2. get a list of wData
	# 3. store into locDatas

		# getting location name
		locName = loc.find(TAG_locationName).text

		wDatas = []

		weatherElements = loc.findall(TAG_weatherElement)

		for weatherElement in weatherElements:

			elementType = weatherElement.find(TAG_elementName).text
			timeElements = weatherElement.findall(TAG_time)

			for te in timeElements:

				startTimeStr = te.find(TAG_startTime).text
				endTimeStr = te.find(TAG_endTime).text

				startDateTime = covertToDateAndTime(startTimeStr)
				endDateTime = covertToDateAndTime(endTimeStr)

				# a temp wdata 
				wdata = None

				# find if wdata for this time range already exist
				# if wdata already exist, than replace the temp wdata
				for wd in wDatas:
					if wd.startDate == startDateTime[0] and wd.startTime == startDateTime[1]:
						wdata = wd

				# if wdata still None, than make a new one
				if wdata == None :	
					wdata = wData.wData(
						startDateTime[0],
						startDateTime[1],
						endDateTime[0],
						endDateTime[1]
					)
					wDatas.append(wdata)	

				# put parameter into wdata
				pn = getParameterName(te)

				if elementType == E_TYPE_Wx:
					wdata.wx = pn
				elif elementType == E_TYPE_MaxT:
					wdata.maxT = int(pn)
				elif elementType == E_TYPE_MinT:
					wdata.minT = int(pn)

		loc_data = wData.loc_data(locName,wDatas)
		locDatas.append(loc_data)

	return locDatas
			


def covertToDateAndTime(timeStr):
	dateAndTimeStr = timeStr.split('T')

	dateStr = dateAndTimeStr[0]
	timeStr = (dateAndTimeStr[1].spilt('+'))[0]

	date = datetime.datetime.strptime(dateStr,'%Y-%m-%d').date()
	time = datetime.datetime.strptime(timeStr,'%X').time()

	return (date,time)


def getParameterName(timeElement):
	return timeElement.find('.//'+TAG_parameter+'/'+TAG_parameterName).text