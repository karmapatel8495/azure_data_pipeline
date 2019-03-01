import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from dateutil.parser import parse

act_name = "pachydermstorage"
act_key = "92byCglypLFaJ5BG1c0lbS7QRuxdmMvGDCpg0MOFR9rE7nh0VGiiQSr1rvrFP9NIkkp6lIXASQlJlVJKUtREmA=="
block_blob_service = BlockBlobService(account_name=act_name, account_key=act_key)

def validateFileNamingConvention(filename):
    try:
        parse(filename[0:10])
        return True
    except:
        return False

# Check the list of blob
container_name = "pachy-container"
processed_container_name = "processed-container"
invalid_container_name = "invalid-container"
generator = block_blob_service.list_blobs(container_name,prefix="2")
print("Running Crowe Industry Practicum Project")
#valid_file_path = "processed/valid/"
#invalid_file_path = "processed/invalid/"

for blob in generator:
	if blob.name.endswith('.csv'):
		if validateFileNamingConvention(blob.name):
			print(blob.name, "is a valid file")
			newname = blob.name.split('_')[1]
			file_path_name = "/pfs/out/" + blob.name
			print(file_path_name)
			block_blob_service.get_blob_to_path(container_name, blob.name,file_path_name)
			print("Pushing to Pachctl Input Repo")
			print("Copying file to Processed Container")
			block_blob_service.create_blob_from_path(processed_container_name, blob.name, file_path_name)
		else:
			print(blob.name, "is an invalid file")
			print("Copying file to Invalid Files Container")

			blob_url = block_blob_service.make_blob_url(container_name, blob.name)

			print(blob_url)
			block_blob_service.copy_blob(invalid_container_name, blob.name, blob_url)
			#for move the file use this line
			block_blob_service.delete_blob(container_name, blob.name)			