# pythonstuff
<b>[Performance Ratio] - Data Translation, Data Calculation, and Data Alerts</b>

<b>[Brief Description:]</b>
All files are part of a computation of a Performance Ratio in which an email will be sent to the list indicated in the JSON files based on the treshold value assigned in the Python file.
The application is also run on a BASH script on a Linux server and set to automate at certain points in time to compute and send alerts.

<b>[Python Files:]</b>
The Python files are separated into two groups, the actual app and the library.

<b>[- Python -]</b>

1) PR_calculator_global.py -
  Script used for calculating the Performance Ratio of a project site and writes the output to a CSV file.
2) PR_alert_global.py -
  Script used for reading the Performance Ratio (through a CSV file) and sends email to a list based on the treshold indicated.
3) data_to_csv.py -
  Script used for translating JSON data to CSV file.
4) csv_to_mysqldb.py -
  Script used to convert a device's CSV output into a MySQL database entry.
  
<b>[- Python Libraries -]</b>

1) py_jsonlib.py -
  Library to open, read, and store the data from the specified JSON file.
  
2) py_configlib.py -
  Library to get directories, filenames, configuration settings used for computation of the <b>Performance Ratio</b>
  
3) py_csvlib.py -
  Library used to read and write CSV files used for the computation of the <b>Performance Ratio</b>
  
4) py_emaillib.py -
  Library used send email to the list specified in the JSON file.
  
<b>[JSON Files:]</b>
The JSON files are mostly used for directory and configuration handling.
This also removes the need for a database server for accessing some configurations used for data management.

1) data_directory.json -
   contains the location of the files needed by the Python files to properly compute the data and perform certain action (ie: sending of emails).
   
2) projcode2_email.json -
  contains a list of filenames associated to the project which are needed to compute data.
  also contains a list of email addresses to send alerts based on the specified treshold.
  
3) projcode3_email.json -
  contains a list of filenames associated to the project which are needed to compute data.
  also contains a list of email addresses to send alerts based on the specified treshold.
  
4) projcode4_email.json -
  contains a list of filenames associated to the project which are needed to compute data.
  also contains a list of email addresses to send alerts based on the specified treshold.
