import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from triorb_robot_lib import TriOrbController

def main():
    robot_name = "Guider"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  (%(filename)s:%(lineno)d) [%(levelname)s] [Robot: %(robot_name)s] %(message)s")
    
    # Step 1: Connect to the robot
    device_path = "/dev/ttyACM0"
    robot = TriOrbController(device_path, robot_name)

    robot.reset_origin()
    robot.wakeup()
    
    # You can also add custom operations:
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=2.0, axis='y')
    robot.turn(desired_angle=3.14, direction='cw')
    robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=2.0, axis='y')
    robot.turn(desired_angle=3.14, direction='cw')
    robot.get_pose()

    # Stop the robot at the end
    robot.stop()
    logging.info("Robot operations completed.")

if __name__ == "__main__":
    main()
