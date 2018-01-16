#!/usr/local/bin/python2.7
import py_jsonlib as jsonlib

# Settings
config_filename = '/path/to/datadirectory.json'

# Get data1 directory
def get_datadirectory(dir_code):
	try:
		jsonData = jsonlib.open_json('', config_filename)
		directory = jsonData["Directories"]["JSON-Directories"][dir_code]["Value"]
	except KeyError:
		print "[Data] Invalid project code."
		exit()
	except AttributeError:
		print "[Data] No JSON file to look at."
		exit()
	return directory

# Get data2 directory
def get_PRdatadirectory(dir_code):
	try:
		prData = jsonlib.open_json('', config_filename)
		directory = prData["Directories"]["PR-Directories"][dir_code]["Value"]
	except KeyError:
		print "[PR] Invalid project code."
		exit()
	return directory

# apply project code or place on JSON file
def get_inverter_id(dir_code, area_name):
	try:
		pid_array = []
		jsonData = jsonlib.open_json('', config_filename)
		inv_id = jsonData["Inverters"][dir_code][area_name]["ID"]
		#convert OrderedDict to list
		list_inv_id = inv_id.items()
		#traverse through list
		for list_ctr in range(0,len(list_inv_id)):
			pid_array.append(list_inv_id[list_ctr][1])
	except KeyError:
		print "Invalid project code."
		exit()
	return pid_array
	
def get_pr_settings(dir_code, area_name):
	p_eff = 0
	p_per_inv = 0
	p_area = 0
	try:
		jsonData = jsonlib.open_json('', config_filename)
		p_eff = jsonData["PR_Settings"][dir_code][area_name]["P_Efficiency"]
		p_per_inv = jsonData["PR_Settings"][dir_code][area_name]["P_Count"]
		p_area = jsonData["PR_Settings"][dir_code][area_name]["P_Area"]
	except KeyError:
		print "Invalid project code."
		exit()
	return p_eff, p_per_inv, p_area
	
def get_pr_filenames(dir_code, emaillist):
	pr_filenames = []
	try:
		jsonData = jsonlib.open_json('',emaillist+'.json')
		pr_fnames = jsonData["PR-Filenames"]
		list_prfnames = pr_fnames.items()
		
		for ctr in range(0, len(list_prfnames)):
			pr_filenames.append(list_prfnames[ctr][1])
	except KeyError:
		print "Invalid project code."
		exit()

	return pr_filenames

def get_email_projname(emaillist):
	try:
		jsonData = jsonlib.open_json('',emaillist+'.json')
		projname = jsonData["File Info"]["Project"]
	except KeyError:
		print "Invalid email code"
		exit()
	return projname