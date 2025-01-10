#!/bin/bash

# Robot 1 details
GUIDER_USER="emage"
GUIDER_PASSWORD="Emage123"
ROBOT1_IP="192.168.0.205"
ROBOT1_SCRIPT_PATH="/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"

# Robot 2 details
FOLLOWER1_USER="emage"
FOLLOWER1_PASSWORD="Emage123"
FOLLOWER1_IP="192.168.0.253"
FOLLOWER1_SCRIPT_PATH="/home/emage/codes/emage_adam_demo_python/demo1/demo1_follower.py"

# Robot 3 details
FOLLOWER2_USERNAME="iot98"
FOLLOWER2_PASSWORD="iot2023"
FOLLOWER2_IP="192.168.0.72"
FOLLOWER2_SCRIPT_PATH="/home/iot98/codes/emage_adam_demo_python/demo1/demo1_follower.py"

# Function to connect to a robot and run its script
run_on_robot() {
    local USERNAME=$1
    local PASSWORD=$2
    local IP=$3
    local SCRIPT_PATH=$4

    echo "Connecting to $USERNAME@$IP and starting the script at $SCRIPT_PATH..."

    # Use sshpass to pass the password for SSH
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$IP "python3 $SCRIPT_PATH" &
}

# Start running the scripts on all robots
run_on_robot $GUIDER_USER $GUIDER_PASSWORD $ROBOT1_IP $ROBOT1_SCRIPT_PATH
run_on_robot $FOLLOWER1_USER $FOLLOWER1_PASSWORD $FOLLOWER1_IP $FOLLOWER1_SCRIPT_PATH
run_on_robot $FOLLOWER2_USERNAME $FOLLOWER2_PASSWORD $FOLLOWER2_IP $FOLLOWER2_SCRIPT_PATH

# Wait for all processes to finish
wait
echo "All scripts have been executed on the robots."
