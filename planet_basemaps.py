import subprocess
import re
from download_planet import download
def run_command_and_extract_order_id(command):
    # Run the command and capture its output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Check if the command ran successfully
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print("Error:", result.stderr)
        return None

    # Print the command output (for debugging purposes)
    # print("Command output:")
    # print(result.stdout)

    # Extract the order ID using a regular expression
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