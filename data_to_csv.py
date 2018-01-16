#!/usr/local/bin/python2.7

# Python Libraries
import os
import sys
import json
from collections import OrderedDict
from pprint import pprint
import csv

# Customized Python Libraries
import py_jsonlib as jsonlib
import py_configlib as configlib
import py_csvlib as csvlib


# Description: converts data (JSON file type) to CSV.

# Command Line Argument
cl_argument = sys.argv[1].replace('.json','')
cl_projectcode = sys.argv[2]

# Main function
def main():
	data_directory = configlib.get_datadirectory(cl_projectcode)
	#print data_directory
	
	#open
	data = jsonlib.open_json(data_directory, cl_argument+'.json')
	
	# Timestamp
	str_timestamp = data["Head"]["Timestamp"]
	str_date = str_timestamp[0:10]
	str_time = str_timestamp[11:19]
	str_datetime = str_date+" "+str_time

	# Sensor Card Data #1
	sensorCard_length = len(data["Body"]["1"])
	print "Number of Sensor Cards: "+str(sensorCard_length)

	# Sensor Card #1
	list_kSensorCard = []
	list_vSensorCard = []

	value_sensorCard = data["Body"]["1"]["2"]["Value"]
	print "Sensor Card 1: "+str(value_sensorCard)

	list_vSensorCard.append(value_sensorCard)

	#WRITE TO CSV
	csvlib.writecsv_vSensor(data_directory, str_date.replace('-','')+'_'+str(cl_argument).replace(data_directory,'')+'.csv', sensorCard_length, str_datetime, '1', list_vSensorCard)
	
# End main function

# Call main function
if __name__ == "__main__":
	main()