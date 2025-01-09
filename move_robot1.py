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

        # Move 1.5 meters forward
        logging.info("Moving forward 1.5 meters...")
        robot.set_vel_absolute(0, 0.2, 0, acc=500, dec=500)
        while robot.get_pos()[0].y < 1.5:
            time.sleep(0.05)
            logging.info(f"Current Y Position: {robot.get_pos()[0].y:.2f} m")
        robot.brake()
        logging.info("Reached 1.5 meters.")

        time.sleep(1)
        logging.info(f"lifting Up")
        res = robot.set_lifter_move(1)[0]
        time.sleep(10)
        if res == 1:
            logging.info("Lifting done.")

        # Turn 90 degrees to the right
        time.sleep(2)
        logging.info("Turning 90 degrees to the right...")
        robot.set_vel_absolute(0, 0, 0.6, acc=500, dec=500)  # Set angular velocity for the turn
        time.sleep(2)  # Allow time for the turn
        robot.brake()
        logging.info("Completed 90-degree turn.")

        #Move 1 meter forward
        time.sleep(2)
        logging.info("Moving forward 1 meter...")
        initial_position = robot.get_pos()[0].x  # Record the current position
        robot.set_vel_absolute(0.2, 0.0, 0, acc=500, dec=500)
        while robot.get_pos()[0].x - initial_position < 0.5:
            time.sleep(0.05)
            logging.info(f"Current X Position: {robot.get_pos()[0].x:.2f} m (relative to turn)")
        robot.brake()
        logging.info("Reached 1 meter after the turn.")

        time.sleep(1)
        lifter_res = robot.set_lifter_move(-1)
        logging.info(f"Unlifting response : {lifter_res}")
        time.sleep(10)
        if lifter_res[0] == 1:
            logging.info("Unlifting done.")

        #again 90 degrees to the right 
        time.sleep(2)
        logging.info("Turning another 90 degrees to the right...")
        robot.set_vel_absolute(0, 0, 0.6, acc=500, dec=500)  # Set angular velocity for the turn
        time.sleep(2)  # Allow time for the turn
        robot.brake()
        logging.info("Completed the second 90-degree turn.")

         # Move another 1 meter forward
        time.sleep(2)
        logging.info("Moving forward 1 meter...")
        initial_position = robot.get_pos()[0].y  # Record the current position
        robot.set_vel_absolute(0, -0.2, 0, acc=500, dec=500)
        logging.info(f"Current Y Position: {robot.get_pos()[0].y:.2f} m (relative to second turn)")

        while True:
            current_pose = robot.get_pos()[0].y 
            if not initial_position - current_pose < 1.5:
                break
            time.sleep(0.05)
            logging.info(f"Current Y Position: {robot.get_pos()[0].y:.2f} m (relative to second turn)")
        robot.brake()
        robot.brake()
        logging.info("Reached 1.5 meter after the second turn.")

        #again 90 degrees to the right 
        # time.sleep(2)
        # logging.info("Turning another 90 degrees to the right...")
        # robot.set_vel_absolute(0, 0, 0.6, acc=500, dec=500)  # Set angular velocity for the turn
        # time.sleep(2)  # Allow time for the turn
        # robot.brake()
        # logging.info("Completed the second 90-degree turn.")
        

        # Stop the robot
        logging.info("Stopping the robot.")
        robot.brake()

    except Exception as e:
        logging.error(f"Error during robot movement: {e}")

if __name__ == "__main__":
    logging.info("Starting robot movement sequence...")
    move_robot()
    logging.info("Robot movement sequence completed.")
