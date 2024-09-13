import subprocess
import re
from download_planet import download
import logging
from google.cloud import secretmanager
import os

# secret_id = 'planet-api-key'
# client = secretmanager.SecretManagerServiceClient()
# name = f"projects/projectps/secrets/{secret_id}/versions/latest"
# response = client.access_secret_version(name=name)
# PL_API_KEY = response.payload.data.decode("UTF-8")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_command_and_extract_order_id(command):
    # Run the command and capture its output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Check if the command ran successfully
    if result.returncode != 0:
        logger.info(f"Command failed with return code {result.returncode}")
        logger.info(f"Error:{result.stderr}")
        return None

    # Print the command output (for debugging purposes)
    # print("Command output:")
    # print(result.stdout)

    # Extract the order ID using a regular expression
    logger.info(f"{result.stdout}")
    order_ids = re.findall(r'Order ID ([\w-]+)', result.stdout)
    return list(set(order_ids))


def find_base_maps(date,confidence,temp_path):
    date = '2024-01-09'
    # Replace with your actual command
    command = "pcf "+temp_path+" "+date+" "+ "-t 75 --order"
    print(command)

    # Run the command and extract the order ID
    order_id = run_command_and_extract_order_id(command)
    # Print or use the extracted order ID
    print(order_id)
    return order_id

def download_and_extract_base_maps(order_ids,download_path):
    for x in order_ids:
        download(x,download_path)
    return