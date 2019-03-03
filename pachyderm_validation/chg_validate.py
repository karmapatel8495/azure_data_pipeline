import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from dateutil.parser import parse

# Mentioning the storage account name and key
act_name = "crowedemostorage"
act_key = "WWxjJW+GkKIkklkXEuR6nDalogfrriKUG3Ra03Z3/xiwg5EA3lOVutjqqJbxCBCxd9C8HrtAuV6OC0Nzwz1rbQ=="
block_blob_service = BlockBlobService(account_name=act_name, account_key=act_key)

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

# Iterate through the blobs in the container

generator = block_blob_service.list_blobs(container_name,prefix="2")
print("Running Crowe Industry Practicum Project")

# Function to validate column headers

def validate_title_row(titlerow):
	columns_names = ["LEVEL_1_CODE", "ACCOUNT NUMBER", "DATE_OF_SERVICE", "POST_DATE", "HCPCS_CPT", "MODIFIER_1", "MODIFIER_2", "MODIFIER_3", "MODIFIER_4", "PROVIDER_RVU", "PLACE_OF_SERVICE", "CARRIER_NUMBER", "LOCALITY_NUMBER", "REVEN"]
	validate_status = True
	title_list = titlerow.split("|")
	for column in title_list:
		if(isinstance(column,str)) == False:
			validate_status = False
			print("Validation #5 failed")
			print(column,type(column))
			return validate_status
	for column_index in range(len(title_list)):
		if(title_list[column_index] != columns_names[column_index]):
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

		validate_status = data_validation(open_file, no_of_header_cols)
		if(not validate_status):
			return validate_status

	else:
		validate_status = False
	return validate_status

path = '/pfs/query/'
for filename in os.listdir(path):
	if validate_file(filename):
		print(filename,":Success")
		print("Copying file to Validate Success Container")
		print(validate_success_container_name, filename, filename)
		moveFileToAnotherContainer(container_name,validate_success_container_name,filename)

	else:
		print(filename,":Fail")
		print("Copying file to Validate Failure Container")
		print(validate_failure_container_name, filename, filename)
		moveFileToAnotherContainer(container_name,validate_failure_container_name,filename)