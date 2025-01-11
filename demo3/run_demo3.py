import threading
import subprocess

# Robot details
robots = [
    {
        "username": "emage",
        "password": "Emage123",
        "ip": "192.168.0.205",
        "script_path": "/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"
    },
    # {
    #     "username": "emage",
    #     "password": "Emage123",
    #     "ip": "192.168.0.253",
    #     "script_path": "/home/emage/codes/emage_adam_demo_python/demo3/follower1.py"
    # },
    # {
    #     "username": "iot98",
    #     "password": "iot2023",
    #     "ip": "192.168.0.72",
    #     "script_path": "/home/iot98/codes/emage_adam_demo_python/demo1/demo1_follower2.py"
    # }
]

# Function to connect to a robot and run its script
# Function to connect to a robot and run its script
def run_on_robot(username, password, ip, script_path):
    logging.info(f"Connecting to {username}@{ip}...")

    # SSH command to stop any running Python processes
    pkill_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{ip} 'sudo pkill python3'"
    
    # SSH command to run the Python script
    script_command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{ip} 'python3 {script_path}'"
    
    try:
        # Step 1: Stop any previously running Python processes
        logging.info(f"Stopping any running Python processes on {ip}...")
        subprocess.run(pkill_command, shell=True, check=True, timeout=60)
        logging.info(f"Stopped running Python processes on {ip}")

        # Step 2: Start the new Python script
        logging.info(f"Starting the script {script_path} on {ip}...")
        subprocess.run(script_command, shell=True, check=True, timeout=300)
        logging.info(f"Script executed successfully on {ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command on {ip}: {e}")
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout expired while executing command on {ip}")

# List to store threads
threads = []

# Create a thread for each robot and start it
for robot in robots:
    thread = threading.Thread(target=run_on_robot, args=(robot["username"], robot["password"], robot["ip"], robot["script_path"]))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All scripts have been executed on the robots.")
