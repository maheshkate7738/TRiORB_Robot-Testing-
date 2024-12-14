import logging

import time

from triorb_core import robot as TriOrbRobot
 
# Created by DEEPAK YADAV

# Date: 2021-09-30
 
# Configure logging to capture test output

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")

# Initialize the robot

try:

    logging.info("Initializing the TriOrb Robot...")

    robot = TriOrbRobot("/dev/ttyACM0")

    logging.info("Robot initialized successfully!")

except Exception as e:

    logging.error(f"Failed to initialize the robot: {e}")

    exit(1)
 
# Function to test robot's response

def test_function(func, *args, **kwargs):

    try:

        logging.info(f"Testing {func.__name__} with args={args}, kwargs={kwargs}...")

        response = func(*args, **kwargs)

        logging.info(f"Response from {func.__name__}: {response}")

        return response

    except Exception as e:

        logging.error(f"Error during {func.__name__}: {e}")

        return None
 
def run_tests():

    results = {}
 
    # Test movement functions

    logging.info("Getting robot info...")

    logging.info(f"Robot Info: {robot.get_info()}")
 
    logging.info("Finding port")

    logging.info(robot.find_port())

    logging.info(f"Resetting Origin to 0")
    robot.reset_origin()

    logging.info("Waking up the robot...")
    robot.wakeup()

    time.sleep(2)

    logging.info(f"Current Position: {robot.get_pos()}")
 
    logging.info("Reset Origin...")

    robot.reset_origin()

    logging.info(f"Current position: {robot.get_pos()}")
 
    logging.info(f"Robot Config : {robot.read_config()}")  # Read current configuration

    robot.write_config({  # Write new configuration

        "acc" : 1500,  # Set standard acceleration/deceleration time to 1.5[s]

        "std-vel" : 0.25,  # Set standard translation speed to 0.25[m/s]

        "std-rot" : 0.5,  # Set standard rotation speed to 0.5[rad/s]

        "torque" : 500,   # Set torque limit to 50[%]

    }) 

    while True:
        robot_pos = robot.get_pos()
        logging.info(f"Robot Pose: {robot_pos}")
        time.sleep(0.1)
 
    logging.info("Closing Robot Port")

    # robot.close_serial()

    # robot.set_pos_absolute(-0.50, 0.25, 0.0, vel_xy=0.2)  # Moves sideways -1m, forward 0.5m, at a speed of 0.2m/s.

    # robot.join()  # Wait for completion
 
    
 
 
if __name__ == "__main__":

    logging.info("Starting Joystick tests for the TriOrb Robot...")

    run_tests()

    logging.info("API tests completed.")

 