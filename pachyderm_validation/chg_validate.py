import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from dateutil.parser import parse

act_name = "pachydermstorage"
act_key = "92byCglypLFaJ5BG1c0lbS7QRuxdmMvGDCpg0MOFR9rE7nh0VGiiQSr1rvrFP9NIkkp6lIXASQlJlVJKUtREmA=="
block_blob_service = BlockBlobService(account_name=act_name, account_key=act_key)

container_name = "pachy-container"
processed_container_name = "processed-container"
validate_success_container_name="validate-success"
validate_failure_container_name="validate-failure"
generator = block_blob_service.list_blobs(container_name,prefix="2")
print("Running Crowe Industry Practicum Project")

def validateEndLines(File_Name):
	validateStatus = True
	Open_file = open(path+File_Name,'r').readlines()
	print("File is Opened")
	if(len(Open_file) > 0):
		no_of_header_cols = len(Open_file[0].split("|"))
		for column in Open_file[0].split("|"):
			if(isinstance(column,str)) == False:
				validateStatus = False
				print("Validation #5 failed")
				print(column,type(column))
				break
	for line in Open_file:
		if os.name == "nt":
			if('\r\n' not in line):
				validateStatus = False
				print("Validation #2 failed")
				break
			else:
				if('\n' not in line):
					validateStatus = False
					print("Validation #2 failed")
					break
		if(len(line.split("|")) != no_of_header_cols):
			validateStatus = False
			print("Validation #7 failed")
			break
		for field in line.split("|"):
			if(field != "" and "str" == type(field)):
				if(field.strip() == ""):
					validateStatus = False
					print("Validation #8 failed")
					break
				if(field.trim() != field):
					validateStatus = False
					print("Validation #9 failed")
					break
	return validateStatus

path = '/pfs/query/'
for filename in os.listdir(path):
	if validateEndLines(filename):
		print(filename,":Success")

		print("Copying file to Validate Success Container")
		print(validate_success_container_name, filename, filename)

		blob_url = block_blob_service.make_blob_url(container_name, filename)
		print(blob_url)

		block_blob_service.copy_blob(validate_success_container_name, filename, blob_url)

		print("Deleting file from pachyderm container")
		print(container_name, filename)
		block_blob_service.delete_blob(container_name, filename, snapshot = None)

	else:
		print(filename,":Fail")
		print("Copying file to Validate Failure Container")
		print(validate_failure_container_name, filename, filename)

		blob_url = block_blob_service.make_blob_url(container_name, filename)
		print(blob_url)

		block_blob_service.copy_blob(validate_failure_container_name, filename, blob_url)
		block_blob_service.delete_blob(container_name, filename)