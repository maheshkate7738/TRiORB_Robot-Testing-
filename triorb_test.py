import logging
import time
from triorb_core import robot as TriOrbRobot
from time import sleep


# Created by DEEPAK YADAV
# Date: 2021-09-30

# Configure logging to capture test output
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialize the robot
try:
    logging.info("Initializing the TriOrb Robot...")
    robot = TriOrbRobot()
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
    robot.wakeup()
    print("Waking up the robot...")
    print(robot.get_status())
    print(robot.get_pos())
    print("Moving forward at a speed of 0.1 m/s for 1 second...")
    robot.set_vel_relative(0.0, 0.1, 0.0, acc=1000)
    time.sleep(1.0)
    robot.brake() # Stops after moving forward for 1 second at a speed of 0.1 m/s.
    robot.sleep()
    results["move_backward"] = test_function(robot.move_backward, distance=1.0, speed=0.5)
    results["turn_left"] = test_function(robot.turn_left, angle=90)
    results["turn_right"] = test_function(robot.turn_right, angle=90)

    # Test sensor reading
    results["get_sensor_data"] = test_function(robot.get_sensor_data)

    # Test grabbing mechanism
    results["grab_object"] = test_function(robot.grab_object)
    results["release_object"] = test_function(robot.release_object)

    # Test system status APIs
    results["get_battery_status"] = test_function(robot.get_battery_status)
    results["get_status"] = test_function(robot.get_status)

    # Run diagnostics
    results["run_diagnostics"] = test_function(robot.run_diagnostics)

    # Log results summary
    logging.info("Test Results Summary:")
    for api, result in results.items():
        logging.info(f"{api}: {'Passed' if result is not None else 'Failed'}")

if __name__ == "__main__":
    logging.info("Starting API tests for the TriOrb Robot...")
    run_tests()
    logging.info("API tests completed.")
