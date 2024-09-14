import subprocess
import zipfile
import os
import shutil
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logger.info(f"Command failed with return code {result.returncode}")
        logger.info(f"Error: {result.stderr}")
        return None
    logger.info(f"now here {result.stdout}")
    return result.stdout

def unzip_files(zip_directory, extract_to):
    for item in os.listdir(zip_directory):
        item_path = os.path.join(zip_directory, item)
        if os.path.isdir(item_path):
            # Recursively process subdirectories
            unzip_files(item_path, extract_to)
        elif item.endswith('.zip'):
            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

def find_and_move_tif_files(base_directory, target_directory):
    # Traverse the directory tree to find composite.tif files
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file == 'composite.tif':
                source_file = os.path.join(root, file)
                # Generate a unique filename using the order ID and timestamp
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                unique_name = f"composite_{timestamp}.tif"
                destination_file = os.path.join(target_directory, unique_name)
                # Move the file to the target directory with the unique name
                shutil.move(source_file, destination_file)
                print(f"Moved {source_file} to {destination_file}")

def download(order_id,ps_path):
    # Run the command to download the order
    logger.info("reached inside download")
    os.makedirs('svr_data', exist_ok=True)
    download_command = f"planet orders wait --max-attempts 0 {order_id}  && planet orders download {order_id} --directory svr_data"
    run_command(download_command)
    logger.info("reached after planet orders wait command")
    # Create directories
    extract_to = 'svr_data_extracted'
    os.makedirs(extract_to, exist_ok=True)
    os.makedirs(ps_path, exist_ok=True)

    # Unzip the files
    unzip_files('svr_data', extract_to)

    # Find and copy the composite.tif files
    find_and_move_tif_files(extract_to, ps_path)

    print("Processing complete.")
    shutil.rmtree('svr_data')
    shutil.rmtree(extract_to)
    # os.remove('svr_data')
    # os.remove(extract_to)