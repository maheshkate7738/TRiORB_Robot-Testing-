import logging
import time
from triorb_core import robot as TriOrbRobot

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")

# Initialize the robot
try:
    logging.info("Initializing the TriOrb Robot...")
    robot = TriOrbRobot("/dev/ttyACM0")
    logging.info("Robot initialized successfully!")
except Exception as e:
    logging.error(f"Failed to initialize the robot: {e}")
    exit(1)

def move_robot():
    try:
        # Reset the robot's origin
        logging.info("Resetting origin...")
        robot.reset_origin()

        # Wake up the robot
        logging.info("Waking up the robot...")
        robot.wakeup()
        time.sleep(3)

        # Log current position
        logging.info(f"Current position before movement: {robot.get_pos()}")

        # Move 1 meter forward
        logging.info("Moving 1.5 meter forward...")
        robot.set_pos_relative(0.0, 0.5, 0.0, vel_xy=0.2)  # Move forward 1 meter at 0.2 m/s
        time.sleep(1)
        robot.join()  # Wait for completion
        # robot.brake()  # Stop the robot
        logging.info(f"Current position after movement: {robot.get_pos()}")

        time.sleep(2)
        logging.info("Moving 1.5 meter backward...")
        robot.set_pos_relative(0.0, -0.5, 0.0, vel_xy=0.2)  # Move forward 1 meter at 0.2 m/s
        time.sleep(1)
        robot.join()  # Wait for completion
        robot.brake()  # Stop the robot
        logging.info(f"Current position after movement: {robot.get_pos()}")

    except Exception as e:
        logging.error(f"Error during robot movement: {e}")

if __name__ == "__main__":
    logging.info("Starting robot movement test...")
    move_robot()
    #logging.info("Robot movement test completed.")
