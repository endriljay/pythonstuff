#!/usr/local/bin/python2.7
import os
import sys
import csv
import time
import pandas as pd
from datetime import datetime

def writecsv_vInverter(data_directory, csv_filename, inv_count, csv_datetime, csv_key, csv_valuePAC, csv_valuedEne, csv_valuetEne, csv_valueyEne):
	print data_directory
	print csv_filename
	
	file_exist = os.path.isfile(data_directory+csv_filename)
	#file exists
	if file_exist:
		#check last line
		with open(data_directory+csv_filename) as csv_fn:
			last = None
			for line in (line for line in csv_fn if line.rstrip('\n')):
				last = line
		csvfn_dtime = last.replace('\n','')[0:19]

		#compare last line timestamp of CSV to timestamp of JSON
		if csv_datetime == csvfn_dtime:
			print "csv file is updated"
		else:
			print "csv file is not updated"
			with open(data_directory+csv_filename, 'a') as csv_file:
				spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				inv_ctr = 0
				#write data
				for inv_ctr in range(0, inv_count):
					spamwriter.writerow([csv_datetime, csv_key[inv_ctr], csv_valuePAC[inv_ctr], csv_valuedEne[inv_ctr], csv_valuetEne[inv_ctr], csv_valueyEne[inv_ctr]])
					inv_ctr = inv_ctr + 1
	else:
	#file does not exist
		with open(data_directory+csv_filename, 'wb') as csv_file:
			spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			inv_ctr = 0
			#write header
			spamwriter.writerow(['Datetime','Inverter_ID','PAC_Value','dEnergy_Value','tEnergy_Value','yEnergy_Value'])
			#write data
			for inv_ctr in range(0, inv_count):
				spamwriter.writerow([csv_datetime, csv_key[inv_ctr], csv_valuePAC[inv_ctr], csv_valuedEne[inv_ctr], csv_valuetEne[inv_ctr], csv_valueyEne[inv_ctr]])
				inv_ctr = inv_ctr + 1

def writecsv_vSensor(data_directory, csv_filename, sensor_count, csv_datetime, irradiance_key, irradiance_value):
	file_exist = os.path.isfile(data_directory+csv_filename)
	#file exists
	if file_exist:
		#cxheck last line
		with open(data_directory+csv_filename) as csv_fn:
			last = None
			for line in (line for line in csv_fn if line.rstrip('\n')):
				last = line
		csvfn_dtime = last.replace('\n','')[0:19]
		
		#compare last line timestamp of csv to timestamp of JSON
		if csv_datetime == csvfn_dtime:
			print "csv file is updated"
		else:
			print "csv file is not updated"
			with open(data_directory+csv_filename, 'a') as csv_file:
				spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				sensor_ctr = 0
				#write data
				for sensor_ctr in range(0, sensor_count):
					spamwriter.writerow([csv_datetime, irradiance_key[sensor_ctr], irradiance_value[sensor_ctr]])
					sensor_ctr = sensor_ctr+1
	#file does not exist
	else:
		with open(data_directory+csv_filename, 'wb') as csv_file:
			spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			sensor_ctr = 0
			#write header
			spamwriter.writerow(['Datetime','Sensor_ID','Irradiance'])
			#write data
			for sensor_ctr in range(0, sensor_count):
				spamwriter.writerow([csv_datetime, irradiance_key[sensor_ctr], irradiance_value[sensor_ctr]])
				sensor_ctr = sensor_ctr + 1

def csvdata_inverter(csvinverter_file, inverter_id):
	# Inverters
	row_count_inverter = 0
	inverter_datetime = []
	inverter_inverterID = []
	inverter_pacValue = []
	inverter_dEneValue = []
	inverter_tEneValue = []
	inverter_yEneValue = []

	inv_id = inverter_id
	
	try:
		dataframe_inverters = pd.read_csv(csvinverter_file)
		
		for index, row in dataframe_inverters.iterrows():
			#print row['Datetime'], row['Inverter_ID'], row['PAC_Value'], row['dEnergy_Value'], row['tEnergy_Value'], row['yEnergy_Value']
			# converts (string) date to datetime; splits hour and minute for conditional statement which controls the scope of the data to be read.
			dtime_buffer = str(row['Datetime'][0:16]+':00')
			dtime_format = datetime.strptime(dtime_buffer, '%Y-%m-%d %H:%M:%S')
			dtime_hour = dtime_format.hour
			dtime_minute = dtime_format.minute

			if ((row['Inverter_ID'] == inv_id) and ((dtime_hour >= 6 and dtime_hour <= 17) or (dtime_hour == 18 and dtime_minute == 0))):
				inverter_datetime.append(dtime_buffer)
				inverter_inverterID.append(row['Inverter_ID'])
				inverter_pacValue.append(row['PAC_Value'])
				inverter_dEneValue.append(row['dEnergy_Value'])
				inverter_tEneValue.append(row['tEnergy_Value'])
				inverter_yEneValue.append(row['yEnergy_Value'])
				row_count_inverter = row_count_inverter + 1
	except IOError:
		print str(csvinverter_file)+" file not found."
		exit()
	
	return inverter_datetime, inverter_inverterID, inverter_pacValue, inverter_dEneValue, inverter_tEneValue, inverter_yEneValue, row_count_inverter

def csvdata_sensorCard(csvsensorCard_file, sensorCard_ID):
	# Sensor Card
	row_count_sensorCard = 0
	sensorCard_datetime = []
	sensorCard_cardID = []
	sensorCard_irradiance = []

	try:
		dataframe_sensorCard = pd.read_csv(csvsensorCard_file)
		for index, row in dataframe_sensorCard.iterrows():
			# converts (string) date to datetime; splits hour and minute for conditional statement which controls the scope of the data to be read.
			dtime_buffer = str(row['Datetime'][0:16]+':00')
			dtime_format = datetime.strptime(dtime_buffer, '%Y-%m-%d %H:%M:%S')
			dtime_hour = dtime_format.hour
			dtime_minute = dtime_format.minute

			if ((dtime_hour >= 6 and dtime_hour <= 17) or (dtime_hour == 18 and dtime_minute == 0)):
				sensorCard_datetime.append(dtime_buffer)
				sensorCard_cardID.append(row['Sensor_ID'])
				sensorCard_irradiance.append(row['Irradiance'])
				row_count_sensorCard = row_count_sensorCard + 1
	except IOError:
		print str(csvsensorCard_file)+" file not found."
		exit()
		
	return sensorCard_datetime, sensorCard_cardID, sensorCard_irradiance, row_count_sensorCard

def csvdata_pratio(data_directory, area, buff_dtime, inv_id, pratio_data):
	csv_inv_date = time.strftime("%Y%m%d")
	csv_inv_dtime = buff_dtime
	
	csv_filename = csv_inv_date+"_PR_"+area+".csv"
	
	csv_inv_id = inv_id
	csv_pratio_data = round(pratio_data, 4)
	
	file_exist = os.path.isfile(data_directory+csv_filename)
	#file exists
	if file_exist:
		with open(data_directory+csv_filename) as csv_fn:
			last = None
			for line in (line for line in csv_fn if line.rstrip('\n')):
				last = line
		csvfn_dtime = last.replace('\n', '')[0:19]
		
		with open(data_directory+csv_filename, 'a') as csv_file:
			spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			sw_ctr = 0
			#write data
			for sw_ctr in range(0, 1):
				spamwriter.writerow([csv_inv_dtime, csv_inv_id, csv_pratio_data])
	#file does not exist
	else:
		with open(data_directory+csv_filename, 'wb') as csv_file:
			spamwriter = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			sw_ctr = 0
			#write header
			spamwriter.writerow(['Datetime','Inverter ID','Performance Ratio'])
			#write data
			for sw_ctr in range(0, 1):
				spamwriter.writerow([csv_inv_dtime, csv_inv_id, csv_pratio_data])

# used by email script
# for reading PR values from CSV
def get_fromPRcsv(data_directory, csvPRfile):
	pr_datetime = []
	pr_inverterID = []
	pr_value = []
	row_count_pr = 0
	
	try:
		pr_file_row = pd.read_csv(data_directory+csvPRfile+'.csv')
		for index, row in pr_file_row.iterrows():
			#print row['Datetime'], row['Inverter ID'], row['Performance Ratio']
			
			#converts the CSV data to python list
			dtime_buffer = str(row['Datetime'][0:16]+':00')
			
			pr_datetime.append(row['Datetime'])
			pr_inverterID.append(row['Inverter ID'])
			pr_value.append(row['Performance Ratio'])
			row_count_pr = row_count_pr + 1
	except IOError:
		print str(data_directory+csvPRfile+'.csv')+" file not found."
	return pr_datetime, pr_inverterID, pr_value, row_count_pr

# used by email script
# for storing under performing values
pr_lowerlimit = 70
def get_upPRvalues(datetime_pr, invID_pr, val_pr, rowCount_pr):
	row_itr = 0
	up_dtime_pr = []
	up_invID_pr = []
	up_val_pr = []
	up_pr_rowCnt = 0
	
	if(rowCount_pr > 0):
		for row_itr in range(0, rowCount_pr):
			# Check if under performing
			if(val_pr[row_itr] < pr_lowerlimit):
				# Under performing
				# log data into a separate list
				up_dtime_pr.append(datetime_pr[row_itr])
				up_invID_pr.append(invID_pr[row_itr])
				up_val_pr.append(val_pr[row_itr])
				up_pr_rowCnt = up_pr_rowCnt + 1
	else:
		exit()	
	return up_dtime_pr, up_invID_pr, up_val_pr, up_pr_rowCnt