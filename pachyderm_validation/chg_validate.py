import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from dateutil.parser import parse
import datetime
import pyodbc

# Mentioning the storage account name and key
act_name = "crowedemostorage"
act_key = "WWxjJW+GkKIkklkXEuR6nDalogfrriKUG3Ra03Z3/xiwg5EA3lOVutjqqJbxCBCxd9C8HrtAuV6OC0Nzwz1rbQ=="
block_blob_service = BlockBlobService(account_name=act_name, account_key=act_key)

# Database connection

server = 'sql-demo-server.database.windows.net'
database = 'sql-db'
username = 'crowe'
password = 'Practicum_2019'
driver= '{ODBC Driver 17 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
	print (row[0]) 
	row = cursor.fetchone()

# Creating function to move file from one blob container to another

def moveFileToAnotherContainer(source_container,destination_container,file_name):
	# Creating Blob URL
	blob_url = block_blob_service.make_blob_url(source_container,file_name)
	print(blob_url)

	# Copying blob to another container
	block_blob_service.copy_blob(destination_container, file_name, blob_url)

	# Deleting blob from main container
	block_blob_service.delete_blob(source_container, file_name)

# Create Containers within Blob

container_name = "crowe-file"
processed_container_name = "processed-container"
validate_success_container_name="validate-success"
validate_failure_container_name="validate-failure"
block_blob_service.create_container(processed_container_name)
block_blob_service.create_container(validate_success_container_name)
block_blob_service.create_container(validate_failure_container_name)
fields_string = "(ChargeDataID, AccountID, FacilityID, PostingDate, HCPCSCode, ModifierComboCode, ProvidedRVUCode, PlaceOfServiceID, CarrierNumberCode, RevenueCodeID, PhysicianNPIComboCode, DaysUnits, ChargeAmount, TotalCharges)"
value_placeholder_string = "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Iterate through the blobs in the container

generator = block_blob_service.list_blobs(container_name,prefix="2")
print("Running Crowe Industry Practicum Project")

# Function to validate column headers

def validate_title_row(titlerow):
	columns_names = ["LEVEL_1_CODE", "ACCOUNT NUMBER", "DATE_OF_SERVICE", "POST_DATE", "HCPCS_CPT", "MODIFIER_1", "MODIFIER_2", "MODIFIER_3", "MODIFIER_4", "PROVIDER_RVU", "PLACE_OF_SERVICE", "CARRIER_NUMBER", "LOCALITY_NUMBER", "REVENUE_CODE", "REFERING_PROV_NPI", "PERFORMING_PROV_NPI", "BILLING_PROV_NPI", "ATTENDING_PROV_NPI", "DAYS_UNITS", "CHARGE_AMT", "TOTAL_CHARGE_AMT", "CDM_CODE", "CDM_DESC", "DEPT_CODE"]
	validate_status = True
	title_list = titlerow.split("|")
	for column in title_list:
		if(isinstance(column,str)) == False:
			validate_status = False
			print("Validation #5 failed")
			print(column,type(column))
			return validate_status
	for column_index in range(len(title_list)):
		if(title_list[column_index].strip() != columns_names[column_index].strip()):
			validate_status = False
			print("Validation #5 failed")
			print(column,type(column))
			return validate_status
	return validate_status

# Function to validate end of line (Carriage Return (CR) and Line Feed (LF))

def validate_crlf(csvfile):
	validate_status = True
	for line in csvfile:
		if os.name == "nt": # for nt systems (Windows)
			if('\r\n' not in line):
				validate_status = False
				print("Validation #2 failed")
				return validate_status
		else: # for unix systems (macOS, Ubuntu etc)
			if('\n' not in line):
				validate_status = False
				print("Validation #2 failed")
				return validate_status
	return validate_status

# Function to validate file delimiter

def pipe_delimit(csvfile, col_size):
	validate_status = True
	for line in csvfile:
		if(len(line.split("|")) != col_size):
			validate_status = False
			print("Validation #7 failed")
			return validate_status
	return validate_status

# Function to validate data entry

def data_validation(csvfile):
	validate_status = True
	for line in csvfile:
		for field in line.split("|"):
			if(field != "" and "str" == type(field)):
				if(field.strip() == ""):
					validate_status = False
					print("Validation #8 failed")
					return validate_status
				if(field.trim() != field):
					validate_status = False
					print("Validation #9 failed")
					return validate_status
	return validate_status

# Validate date and time fields

def date_and_time_validation(csvfile):
	validate_status = True
	for line in csvfile[1:]:
		columns = line.split("|")
		date_of_service = columns[2].strip()
		validate_status = date_validate(date_of_service, "DATE_OF_SERVICE")
		if(not validate_status):
			validate_status = False
			return validate_status
		post_date = columns[3].strip()
		validate_status = date_validate(post_date, "POST_DATE")
		if(not validate_status):
			validate_status = False
			return validate_status
	return validate_status

def date_validate(value, column_name):
	validate_status = True
	try:
		datetime.datetime.strptime(value, '%m/%d/%Y')
	except ValueError:
		validate_status = False
		print("Validation #14 failed. Incorrect data format, should be MM/DD/YYYY, column", column_name)
	return validate_status

# Master function for file validation

def validate_file(file_name):
	validate_status = True
	open_file = open(path+file_name,'r').readlines()
	print("File is Opened")
	if(len(open_file) > 0):
		no_of_header_cols = len(open_file[0].split("|"))

		# Validating column headers

		validate_status = validate_title_row(open_file[0])
		if(not validate_status):
			return validate_status

		# Validate end of line (Carriage Return (CR) and Line Feed (LF))

		validate_status = validate_crlf(open_file)
		if(not validate_status):
			return validate_status

		# Validate pipe delimiter

		validate_status = pipe_delimit(open_file, no_of_header_cols)
		if(not validate_status):
			return validate_status
		
		# Validate data entry

		validate_status = data_validation(open_file)
		if(not validate_status):
			return validate_status

		# Validate date and time formats

		validate_status = date_and_time_validation(open_file)
		if(not validate_status):
			return validate_status
	else:
		validate_status = False
	return validate_status

# Function to load data into list

def load_data(file_name):
	open_file = open(path+file_name,'r').readlines()
	data_master_array = []
	for line in open_file[1:]:
		current_line = line.strip()
		data_master_array.append(current_line.split("|"))
	return(data_master_array)

# Function to delete all records (Temporary soln)

def delall():
	tem_sql = ("DELETE from dbo.factChargeData")
	cursor.execute(tem_sql)

# Function to insert a record

def insert_record(current_data, counter):
	isvalid = True
	values = []
	values.append(counter + 1)
	values.append(counter + 1)
	values.append(counter + 1)
	if(current_data[3] is not None and current_data[3] != ""):
		try:
			value_date = datetime.datetime.strptime(current_data[3] + " 00:00:00",'%m/%d/%Y %H:%M:%S')
			values.append(value_date)
		except ValueError as ve:
			isvalid = False
			return(isvalid)
	else:
		isvalid = False
		return(isvalid)
	values.append(str(current_data[4]))
	values.append(str(current_data[5]) + "," + str(current_data[6]) + "," + str(current_data[7]) + "," + str(current_data[8]))
	values.append(str(current_data[9]))
	values.append(str(current_data[10]))
	values.append(str(current_data[11]))
	values.append(str(current_data[13]))
	values.append(str(current_data[14]) + "," + str(current_data[15]) + "," + str(current_data[16]) + "," + str(current_data[17]))
	values.append(float(current_data[18]))
	values.append(str(current_data[19]))
	values.append(str(current_data[20]))
	sql_command = "INSERT INTO dbo.factChargeData " + fields_string + " VALUES " +  value_placeholder_string
	print(sql_command)
	print(values)
	cursor.execute(sql_command,values)
	return(isvalid)

# Function to insert data from file

def insert_file(data_master_array):
	isvalid = True
	for counter in range(len(data_master_array)):
		current_data = data_master_array[counter]
		if(isvalid):
			isvalid = insert_record(current_data, counter)
		if(not isvalid):
			return(isvalid)
	return(isvalid)

path = '/pfs/query/'
valid_data = True
for filename in os.listdir(path):
	if validate_file(filename):
		data_master_array = load_data(filename)
		delall()
		valid_data = insert_file(data_master_array)
		if(valid_data):
			connection.commit()
			print(filename,":Success")
			print("{} Records Inserted".format((len(data_master_array))))
			print("Copying file to Validate Success Container")
			print(validate_success_container_name, filename, filename)
			moveFileToAnotherContainer(container_name,validate_success_container_name,filename)
		else:
			print(filename,":Fail")
			print("Invalid data found, record insert failed")
			print("Copying file to Validate Failure Container")
			print(validate_failure_container_name, filename, filename)
			moveFileToAnotherContainer(container_name,validate_failure_container_name,filename)
	else:
		print(filename,":Fail")
		print("Copying file to Validate Failure Container")
		print(validate_failure_container_name, filename, filename)
		moveFileToAnotherContainer(container_name,validate_failure_container_name,filename)
connection.close()

