#!/usr/local/bin/python2.7

# Python Libraries
from email.mime.text import MIMEText
from datetime import datetime

import smtplib
import csv
import sys
import os
import math
import time
import pandas as pd

# Customized Python Libraries
import py_jsonlib as jsonlib
import py_configlib as configlib
import py_csvlib as csvlib
import py_emaillib as emaillib

# Main function
def main():
	try:
		cl_args_projcode = sys.argv[1]
		cl_args_emaillist = sys.argv[2].replace('.json','')
	
		# Initialize List and Variable
		pr_dtime = []
		pr_invID = []
		pr_val = []
		pr_rowCnt = 0
	
		# up = under performing
		up_pr_dtime = []
		up_pr_invID = []
		up_pr_val = []
		up_pr_rowCnt = 0
		
		#collection of the list of under performing inverters (list of up variables)
		upl_filename = []
		upl_pr_dtime = []
		upl_pr_id = []
		upl_pr_val = []
		upl_pr_rowCnt = []
		list_of_prfname = configlib.get_pr_filenames(cl_args_projcode, cl_args_emaillist)
		
		data_directory = configlib.get_PRdatadirectory(cl_args_projcode)
		proj_name = configlib.get_email_projname(cl_args_emaillist)
		print proj_name
		print data_directory
		
		date_today = time.strftime("%Y%m%d")
		#Date override
		#date_today = '20170327'
		
		for fname_ctr in range(0, len(list_of_prfname)):
			pr_filename = str(date_today)+'_'+str(list_of_prfname[fname_ctr].replace('.csv',''))
			
			file_exist = os.path.isfile(data_directory+pr_filename+'.csv')
			if file_exist:
				# Store PR Data
				pr_dtime, pr_invID, pr_val, pr_rowCnt = csvlib.get_fromPRcsv(data_directory, pr_filename)
				# Get under performing values
				up_pr_dtime, up_pr_invID, up_pr_val, up_pr_rowCnt = csvlib.get_upPRvalues(pr_dtime, pr_invID, pr_val, pr_rowCnt)
				
				upl_filename.append(list_of_prfname[fname_ctr])
				upl_pr_dtime.append(up_pr_dtime)
				upl_pr_id.append(up_pr_invID)
				upl_pr_val.append(up_pr_val)
				upl_pr_rowCnt.append(up_pr_rowCnt)
				
			else:
				pass
		# Send under performing inverters on an email
		emaillib.send_mail_PR(proj_name, cl_args_projcode, cl_args_emaillist, upl_filename, upl_pr_dtime, upl_pr_id, upl_pr_val, upl_pr_rowCnt)
	except IndexError:
		print "Invalid arguments"
# End main function

# Call main function
if __name__ == "__main__":
	main()