mport boto3
import requests
import zipfile
import os

# Initialize a Boto3 client for Lambda
lambda_client = boto3.client('lambda')

def download_lambda_function_zip(function_name, download_path):
    try:
        # Get the Lambda function details
        response = lambda_client.get_function(FunctionName=function_name)
        
        # Extract the pre-signed URL to the deployment package
        zip_file_url = response['Code']['Location']
        print(f"ZIP file URL: {zip_file_url}")
        
        # Download the ZIP file using the pre-signed URL
        response = requests.get(zip_file_url)
        response.raise_for_status()  # Check if the request was successful

        # Save the downloaded ZIP file to the specified path
        with open(download_path, 'wb') as f:
            f.write(response.content)

        print(f"Lambda function ZIP file downloaded successfully: {download_path}")
    
    except Exception as e:
        print(f"Error occurred: {e}")

def unzip_file(zip_file_path, extract_to):
    try:
        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"ZIP file extracted successfully to: {extract_to}")
    except Exception as e:
        print(f"Error while unzipping the file: {e}")

if _name_ == "__main__":
    function_name = 'mylambda'  # Replace with your Lambda function name
    download_path = 'lambda_function.zip'  # Local path where the ZIP file will be saved
    extract_to = './'  # Directory where the ZIP file will be extracted
    
    # Step 1: Download the ZIP file
    download_lambda_function_zip(function_name, download_path)
    
    # Step 2: Unzip the downloaded file
    if os.path.exists(download_path):
        unzip_file(download_path, extract_to)
