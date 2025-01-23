import threading
import subprocess

# Robot details
robots = [
    {
        "username": "emage",
        "password": "Emage123",
        "ip": "192.168.0.102",
        "script_path": "/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"
    },
    {
        "username": "emage",
        "password": "Emage123",
        "ip": "192.168.0.103",
        "script_path": "/home/emage/codes/emage_adam_demo_python/demo1/demo1_follower1.py"
    },

    # {
    #     "username": "iot98",
    #     "password": "iot2023",
    #     "ip": "192.168.0.104",
    #     "script_path": "/home/iot98/codes/emage_adam_demo_python/demo1/demo1_follower2.py"
    # }
]

# Function to connect to a robot and run its script
def run_on_robot(username, password, ip, script_path):
    print(f"Connecting to {username}@{ip} and starting the script at {script_path}...")
    
    # SSH command to run the script on the robot using sshpass and ssh
    command = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {username}@{ip} 'python3 {script_path}'"
    
    # Execute the command
    subprocess.run(command, shell=True)

# List to store threads
threads = []

for _ in range(2):
    threads = []  # Clear threads list before each loop iteration
    # Create a thread for each robot and start it
    for robot in robots:
        thread = threading.Thread(target=run_on_robot, args=(robot["username"], robot["password"], robot["ip"], robot["script_path"]))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

print("All scripts have been executed on the robots.")
