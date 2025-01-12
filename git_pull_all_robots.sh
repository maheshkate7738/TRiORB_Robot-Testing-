#!/bin/bash

# Robot 1 details
GUIDER_USER="emage"
GUIDER_PASSWORD="Emage123"
ROBOT1_IP="192.168.0.205"
PROJECT_PATH="/home/emage/codes/emage_adam_demo_python"

# Robot 2 details
FOLLER1_USER="emage"
FOLLER1_PASSWORD="Emage123"
ROBOT2_IP="192.168.0.253"
PROJECT_PATH2="/home/emage/codes/emage_adam_demo_python"

# Robot 3 details
ROBOT3_USERNAME="iot98"
ROBOT3_PASSWORD="iot2023"
ROBOT3_IP="192.168.0.72"
PROJECT_PATH3="/home/iot98/codes/emage_adam_demo_python"

# Function to connect to a robot, kill python processes, and then run git pull
kill_python_processes_and_git_pull() {
    local USERNAME=$1
    local PASSWORD=$2
    local IP=$3
    local PROJECT_PATH=$4

    echo "Connecting to $USERNAME@$IP and killing all Python processes..."

    # Kill all running Python processes using pkill
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$IP "echo '$PASSWORD' | sudo -S pkill -9 python3"

    # Run git pull after killing Python processes
    echo "Performing 'git pull' at $PROJECT_PATH on $IP..."
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no $USERNAME@$IP "cd $PROJECT_PATH && git pull" &
}

# Kill Python processes and pull latest changes from Git on all robots
kill_python_processes_and_git_pull $GUIDER_USER $GUIDER_PASSWORD $ROBOT1_IP $PROJECT_PATH
kill_python_processes_and_git_pull $FOLLER1_USER $FOLLER1_PASSWORD $ROBOT2_IP $PROJECT_PATH2
kill_python_processes_and_git_pull $ROBOT3_USERNAME $ROBOT3_PASSWORD $ROBOT3_IP $PROJECT_PATH3

# Wait for all processes to finish
wait
echo "Git pull operation has been completed on all robots after killing Python processes."
