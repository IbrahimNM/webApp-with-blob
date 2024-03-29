from flask import Flask, request
import os
import uuid
import sys
from azure.storage.blob import BlockBlobService, PublicAccess
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

''' An endpoint to create a container inside a blob storage.
    You need to specifiy and provife the account name and the account key 
    of the blob storage. 
    @params
        name: the name of the new container.
    @return:
        success: The container has been created.
        falied: The container was not created. 
'''
@app.route("/blob")
def create_blob():
    # get a container name parameter <name>
    container_name = request.args.get('name') 
    # set a default container name if the user did not provide it. 
    if container_name is None:
        container_name = 'test'
    
    status = "failed"
    try:
        
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(
            account_name='ibrahim20', account_key='wMCFPXsA/klI6OGSrmdc1jgFIAJa3bRyD9mhtH31fS9OLCnlhGL8Er/TSc9uKrMMt1GYinFBkIuC5lP2krt/IA==')

        # Create a container called 'quickstartblobs'.
        #container_name = newname
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(
            container_name, public_access=PublicAccess.Container)

        # Create a file in Documents to test the upload and download.
        local_path = os.path.expanduser("~/Documents")
        local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".txt"
        full_path_to_file = os.path.join(local_path, local_file_name)

        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write("Hello, World!")
        file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(
            container_name, local_file_name, full_path_to_file)

        status = "succeess"
    except Exception as e:
        print(e)

    return status
