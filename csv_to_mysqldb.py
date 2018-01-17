#!/usr/local/bin/python2.7
import os.path
import MySQLdb as mdb
import sys
import pandas as pd
import time

#MySQL part
con=mdb.connect('MySQL server ip address','MySQL username','MySQL password','MySQL database')
date_today = (time.strftime("%Y%m%d"))
#manual override
#date_today="20150215"
print "Date: "+date_today
cur=con.cursor()

#CSV part
directory='/directory/to/csv/file/'

system_key='6'
table_name='SYSTEM_MISC_DATA'
cur.execute("SELECT FK_SYSTEM_MISC,DATETIME_MISC_DATA,SYS_AC_POWER,SYS_AC_POWER_2,SYS_AC_POWER_3,SYS_AC_ENERGY,SYS_AC_ENERGY_2,SYS_AC_ENERGY_3,W_IRRADIANCE_POA_1 FROM "+table_name+" WHERE FK_SYSTEM_MISC ="+system_key+" ORDER BY DATETIME_MISC_DATA DESC LIMIT 1;")
results=cur.fetchall()

for row in results:
	dtime_last = row[1]
print "last datetime: "+str(dtime_last)

i=0	
if os.path.isfile(directory+date_today+"_misc.csv"):
	print "File found."
	data=pd.read_csv(directory+date_today+"_misc.csv")		
	sys_datetime=[]
	sys_ac_power=[]
	sys_ac_power2=[]
	sys_ac_power3=[]
	sys_ac_energy=[]
	sys_ac_energy2=[]
	sys_ac_energy3=[]
	sys_wirrad1=[]
	sys_va=[]
	sys_ia=[]
	sys_pfa=[]
	sys_vb=[]
	sys_ib=[]
	sys_pfb=[]
	sys_vc=[]
	sys_ic=[]
	sys_pfc=[]
	sys_kwtot=[]
	sys_kwhtot=[]
	#Reading the CSV
	str_query=''
	for x in range(0,len(data)):
		t1_last=time.strptime(str(dtime_last),"%Y-%m-%d %H:%M:%S")
		t2_last=time.strptime(str(data['DATETIME_MISC_DATA'][x]).replace("%20"," "),"%Y-%m-%d %H:%M:%S")
		if(t1_last < t2_last):
			sys_datetime.append(data['DATETIME_MISC_DATA'][x])
			sys_ac_power.append(data['SYS_AC_POWER'][x])
			sys_ac_power2.append(data['SYS_AC_POWER_2'][x])
			sys_ac_power3.append(data['SYS_AC_POWER_3'][x])
			sys_ac_energy.append(data['SYS_AC_ENERGY'][x])
			sys_ac_energy2.append(data['SYS_AC_ENERGY_2'][x])
			sys_ac_energy3.append(data['SYS_AC_ENERGY_3'][x])
			sys_wirrad1.append(data['W_IRRADIANCE_POA_1'][x])
			sys_va.append(data['VAS'][x])
			sys_ia.append(data['IA'][x])
			sys_pfa.append(data['PFA'][x])
			sys_vb.append(data['VB'][x])
			sys_ib.append(data['IB'][x])
			sys_pfb.append(data['PFB'][x])
			sys_vc.append(data['VC'][x])
			sys_ic.append(data['IC'][x])
			sys_pfc.append(data['PFC'][x])
			sys_kwtot.append(data['kWtot'][x])
			sys_kwhtot.append(data['kWhtot'][x])				
			i=i+1
	for j in range(0,i-1):
		str_query+="('"+system_key+"','"+str(sys_datetime[j]).replace("%20"," ")+"','"+str(sys_ac_power[j])+"','"+str(sys_ac_power2[j])+"','"+str(sys_ac_power3[j])+"','"+str(sys_ac_energy[j])+"','"+str(sys_ac_energy2[j])+"','"+str(sys_ac_energy3[j])+"','"+str(sys_wirrad1[j])+"','"+str(sys_va[j])+"','"+str(sys_ia[j])+"','"+str(sys_pfa[j])+"','"+str(sys_vb[j])+"','"+str(sys_ib[j])+"','"+str(sys_pfb[j])+"','"+str(sys_vc[j])+"','"+str(sys_ic[j])+"','"+str(sys_pfc[j])+"','"+str(sys_kwtot[j])+"','"+str(sys_kwhtot[j])+"')"
		str_query+=','
	str_query=str_query[:-1]
	str_query+=';'
	ins_statement="INSERT INTO SYSTEM_MISC_DATA (FK_SYSTEM_MISC,DATETIME_MISC_DATA,SYS_AC_POWER,SYS_AC_POWER_2,SYS_AC_POWER_3,SYS_AC_ENERGY,SYS_AC_ENERGY_2,SYS_AC_ENERGY_3,W_IRRADIANCE_POA_1,SYS_VA,SYS_IA,SYS_PFA,SYS_VB,SYS_IB,SYS_PFB,SYS_VC,SYS_IC,SYS_PFC,SYS_KWTOT,SYS_KWHTOT) VALUES "
	sql_query=ins_statement+str_query
	if (len(str_query)<=1):
		print "Up to date"
	else:
		print "Updating"
		print sql_query
		cur.execute(sql_query)
		con.commit()
else:
	print "File not found"
	sys.exit()
