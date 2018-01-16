#!/usr/local/bin/python2.7

# Python Libraries
import os
import sys
import time
from datetime import datetime
import csv
import pandas as pd

# Customized Python Libraries
import py_jsonlib as jsonlib
import py_configlib as configlib
import py_csvlib as csvlib

# Description: calculates PR% using Day Energy and Irradiance

# Insert TRY / EXCEPT statement here!
# If else on file 1 and file 2

# Directory
data_directory = ''

# Command Line Argument
cl_args_energy = sys.argv[1]
cl_args_irradiance = sys.argv[2]
cl_args_projcode = sys.argv[3]
#print cl_args_energy
#print cl_args_irradiance

cl_args_energysplit = [] 
cl_args_energysplit = cl_args_energy.split("/")
num_of_tokens = len(cl_args_energysplit)
cl_arg_token = cl_args_energysplit[num_of_tokens-1]
panel_efficiency, num_of_panels_per_inv, panel_area = configlib.get_pr_settings(cl_args_projcode, cl_arg_token[9:len(cl_arg_token)])

# Main function
def main():
	
	data_directory = configlib.get_PRdatadirectory(cl_args_projcode)
	print data_directory
	
	# Control Variables
	inv_id_array = []
	inv_id_array = configlib.get_inverter_id(cl_args_projcode, cl_arg_token[9:len(cl_arg_token)])
	buffer_dtime = time.strftime("%Y-%m-%d %H:%M:%S")

	for inv_id_ctr in range(0, len(inv_id_array)):
		buffer_inv_id = inv_id_array[inv_id_ctr]
		buffer_sensor_id = 1

		# Inverter CSV data assigned to Python Variables
		inv_dtime, inv_invid, inv_pac, inv_dEne, inv_tEne, inv_yEne, inv_dataCount = csvlib.csvdata_inverter(cl_args_energy, buffer_inv_id)
		# Sensor Card CSV data assigned to Python Variables
		sensor_dtime, sensor_id, sensor_irri, sensor_dataCount = csvlib.csvdata_sensorCard(cl_args_irradiance, buffer_sensor_id)

		# Try to compute for PR
		# Using timestamp, check for data integrity
		#	Inverter
		chkd_inv_dtime = []
		chkd_inv_id = []
		chkd_inv_tEne = []
		#	Sensor
		chkd_sensr_dtime = []
		chkd_sensr_id = []
		chkd_sensr_irri = []

		#print buffer_inv_id
		for i in range(0,len(inv_dtime)):
			try:
				# inverter data is also found on CSV data
				# assign data to another list
				buff_invdtime = inv_dtime[i]
				buff_sendtime = sensor_dtime[sensor_dtime.index(inv_dtime[i])]
				buff_sensorIndexAt = sensor_dtime.index(inv_dtime[i])

				# Time
				chkd_inv_dtime.append(inv_dtime[i])
				chkd_sensr_dtime.append(sensor_dtime[buff_sensorIndexAt])
				# IDs
				chkd_inv_id.append(inv_invid[i])
				chkd_sensr_id.append(sensor_id[buff_sensorIndexAt])
				# Data
				chkd_inv_tEne.append(inv_tEne[i])
				chkd_sensr_irri.append(sensor_irri[buff_sensorIndexAt])

				#print "index: "+str(i)+" | "+str(buff_invdtime)+" | "+str(buff_sendtime)
				#print "energy: "+str(inv_dEne[i])+" | irradiance: "+str(sensor_irri[buff_sensorIndexAt])
			except ValueError:
				# inverter data is not found on CSV data
				#print "index: "+str(i)+" "+str(inv_dtime[i])
				placeholder = 0
				#print "index "+str(i)+" not found."

		# Using new data list, compute for the PR
		energy_to_deduct = 0
		energy_first_data = 0
		energy_last_data = 0
		energy_for_the_day = 0
		chkd_energy = 0
		performance_ratio = 0
		sum_of_irradiance = sum(chkd_sensr_irri)

		for ctr_b in range(0, len(chkd_inv_dtime)):
			if (chkd_inv_dtime[ctr_b] == chkd_sensr_dtime[ctr_b]):
				if ctr_b == 0:
					# first data do nothing special
					#print "1 [first data]: "+str(chkd_inv_dtime[ctr_b])+","+str(chkd_inv_tEne[ctr_b])+","+str(chkd_sensr_irri[ctr_b])
					energy_first_data = chkd_inv_tEne[ctr_b]
				elif ctr_b == len(chkd_inv_dtime)-1:
					# last data do nothing special
					#print "2 [last data]: "+str(chkd_inv_dtime[ctr_b])+","+str(chkd_inv_tEne[ctr_b])+","+str(chkd_sensr_irri[ctr_b])
					energy_last_data = chkd_inv_tEne[ctr_b]
				else:
					# middle data check timestamp if gap

					# if the time difference between the current data and the before data is > 5 minutes: do something
					#	do something:
					#	get current dEnergy -> curr_dEne
					#	get before dEnergy -> before_dEne
					#	subtract current to before -> sub_dEne
					# else: do something

					bfr_dtime_buffer = str(chkd_inv_dtime[ctr_b-1][0:16]+':00')
					bfr_dtime_format = datetime.strptime(bfr_dtime_buffer, '%Y-%m-%d %H:%M:%S')
					bfr_tEnergy_data = chkd_inv_tEne[ctr_b-1]
					
					cur_dtime_buffer = str(chkd_inv_dtime[ctr_b][0:16]+':00')
					cur_dtime_format = datetime.strptime(cur_dtime_buffer, '%Y-%m-%d %H:%M:%S')
					cur_tEnergy_data = chkd_inv_tEne[ctr_b]

					time_diff = cur_dtime_format - bfr_dtime_format
					sec_time_diff = time_diff.total_seconds()
					tEnergy_diff = cur_tEnergy_data - bfr_tEnergy_data
					
					if sec_time_diff > 300:
						#print "-----"
						#print str(cur_dtime_format)+" - "+str(bfr_dtime_format)+" time difference: "+str(sec_time_diff)+"secs"
						#print str(cur_tEnergy_data)+" - "+str(bfr_tEnergy_data)+" energy to deduct: "+str(tEnergy_diff)
						energy_to_deduct = energy_to_deduct + tEnergy_diff
						#print "-----"
					elif sec_time_diff < 300:
						#print "-----"
						#print str(cur_dtime_format)+" - "+str(bfr_dtime_format)+" time difference: "+str(sec_time_diff)+"secs"
						#print str(cur_tEnergy_data)+" - "+str(bfr_tEnergy_data)+" energy to deduct: "+str(tEnergy_diff)
						energy_to_deduct = energy_to_deduct + tEnergy_diff
						#print "-----"
					else:
						#print "time difference: "+str(sec_time_diff)+"secs | do nothing"
						else_buffer = 0

		#print "------------------------"
		energy_for_the_day = (energy_last_data - energy_first_data)
		chkd_energy = energy_for_the_day - energy_to_deduct
		#print "----- first tEnergy data: "+str(energy_first_data)
		#print "----- last tEnergy data: "+str(energy_last_data)
		#print "----- energy for the day: "+str(energy_for_the_day)
		#print "----- energy to deduct: "+str(energy_to_deduct)
		#print "----- [summation of irradiance: "+str(sum_of_irradiance)+"]"
		#print "----- [energy used for calculation: "+str(chkd_energy)+"]"
		#print "----- [panel efficiency: "+str(panel_efficieny)+"]"
		#print "----- [number of panels: "+str(num_of_panels_per_inv)+"]"
		#print "----- [area of panels: "+str(panel_area)+"]"
		#print "------------------------"
		
		try:
			performance_ratio = ((chkd_energy) / ( (sum_of_irradiance/12) * panel_efficiency * num_of_panels_per_inv * panel_area) * 100)
		except ZeroDivisionError:
			print "Error - Division by Zero"
			print "Please check area: "+str(cl_arg_token[9:len(cl_arg_token)].replace('.csv',''))+" and inverter:"+str(inv_id_array[inv_id_ctr])
			performance_ratio = -1
			
		print data_directory
		print cl_arg_token[9:len(cl_arg_token)]
		
		csvlib.csvdata_pratio(data_directory, cl_arg_token[9:len(cl_arg_token)].replace('.csv',''), buffer_dtime, inv_id_array[inv_id_ctr], performance_ratio)
	#	csvdata_pratio(cl_args_energy[53:len(cl_args_energy)].replace('.csv',''), buffer_dtime, inv_id_array[inv_id_ctr], performance_ratio)
		print "----- [performance ratio: "+str(round(performance_ratio,4))+"%]"
# End main function

# Call main function
if __name__ == "__main__":
	main()