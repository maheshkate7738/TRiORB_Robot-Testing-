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

def move_robot_forward():
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
        robot.set_vel_absolute(0, 0.2, 0, acc=500, dec=500)
        # Move 1 meter forward
        logging.info(f"Robot Y position: {robot.get_pos()[0].y}")
        while robot.get_pos()[0].y < 1.38:
            time.sleep(0.05)
            logging.info(f"Current Position: {robot.get_pos()[0].y}")
        robot.brake()  # Stop the robot
        # robot.join()
        logging.info(f"Current position after movement: {robot.get_pos()}")
        
        #Lifting up

        # time.sleep(1)
        # logging.info(f"lifting Up")
        # res = robot.set_lifter_move(1)[0]
        # time.sleep(10)
        # if res == 1:
        #     logging.info("Lifting done.")

        # time.sleep(1)
        # robot.set_vel_absolute(0, -0.2, 0, acc=500, dec=500)
        # # Move 1 meter forward
        # logging.info(f"Robot Y position: {robot.get_pos()[0].y}")
        # while robot.get_pos()[0].y > 0.15:
        #     time.sleep(0.05)
        #     logging.info(f"Current Position: {robot.get_pos()[0].y}")
        # robot.brake()  # Stop the robot
        # # robot.join()
        # logging.info(f"Current position after movement: {robot.get_pos()}")
        
        #lifting down

        # time.sleep(1)
        # lifter_res = robot.set_lifter_move(-1)
        # logging.info(f"Unlifting response : {lifter_res}")
        # time.sleep(10)
        # if lifter_res[0] == 1:
        #     logging.info("Unlifting done.")

    except Exception as e:
        logging.error(f"Error during robot movement: {e}")

if __name__ == "__main__":
    logging.info("Starting robot movement test...")
    move_robot_forward()
    #logging.info("Robot movement test completed.")
