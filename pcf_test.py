import subprocess
import re

def run_command_and_extract_order_id(command):
    # Run the command and capture its output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Check if the command ran successfully
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print("Error:", result.stderr)
        return None

    # Print the command output (for debugging purposes)
    print("Command output:")
    print(result.stdout)

    # Extract the order ID using a regular expression
    match = re.search(r'Order ID ([\w-]+)', result.stdout)
    if match:
        order_id = match.group(1)
        return order_id
    else:
        print("Order ID not found in the output")
        return None

