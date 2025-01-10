#!/bin/bash

# Robot 1 details
GUIDER_USER="emage"
GUIDER_PASSWORD="Emage123"
ROBOT1_IP="192.168.0.205"
ROBOT1_SCRIPT_PATH="/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"

# Robot 2 details
FOLLER1_USER="robot2_user"
FOLLER1_PASSWORD="robot2_pass"
ROBOT2_IP="192.168.0.253"
ROBOT2_SCRIPT_PATH="/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"

# Robot 3 details
ROBOT3_USERNAME="emage"
ROBOT3_PASSWORD="Emage123"
ROBOT3_IP="192.168.0.72"
ROBOT3_SCRIPT_PATH="/home/emage/codes/emage_adam_demo_python/demo1/demo1_guider.py"

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
# run_on_robot $FOLLER1_USER $ROBOT2_PASSWORD $ROBOT2_IP $ROBOT2_SCRIPT_PATH
# run_on_robot $ROBOT3_USERNAME $ROBOT3_PASSWORD $ROBOT3_IP $ROBOT3_SCRIPT_PATH

# Wait for all processes to finish
wait
echo "All scripts have been executed on the robots."
