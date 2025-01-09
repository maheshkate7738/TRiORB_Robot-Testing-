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

def move_forward_and_backward():
    try:
        # Reset the robot's origin
        logging.info("Resetting origin...")
        robot.reset_origin()

        # Wake up the robot
        logging.info("Waking up the robot...")
        robot.wakeup()
        time.sleep(3)

        # Move 1.5 meters forward
        logging.info("Moving forward 1.5 meters...")
        robot.set_vel_absolute(0, 0.2, 0, acc=500, dec=500)
        initial_position_y = robot.get_pos()[0].y  # Record the initial position

        while True:
            current_position_y = robot.get_pos()[0].y
            if current_position_y - initial_position_y >= 1.5:
                break
            time.sleep(0.05)
            logging.info(f"Current Y Position: {current_position_y:.2f} m")

        robot.brake()
        logging.info("Reached 1.5 meters forward.")

        time.sleep(1)

        # Move back to the original position (-1.5 meters)
        logging.info("Moving back to the original position (-1.5 meters)...")
        robot.set_vel_absolute(0, -0.2, 0, acc=500, dec=500)

        while True:
            current_position_y = robot.get_pos()[0].y
            if current_position_y - initial_position_y <= 0:
                break
            time.sleep(0.05)
            logging.info(f"Current Y Position: {current_position_y:.2f} m")

        robot.brake()
        logging.info("Returned to the original position.")

        # Stop the robot
        logging.info("Stopping the robot.")
        robot.brake()

    except Exception as e:
        logging.error(f"Error during robot movement: {e}")

if __name__ == "__main__":
    logging.info("Starting robot forward and backward movement sequence...")
    move_forward_and_backward()
    logging.info("Robot forward and backward movement sequence completed.")
