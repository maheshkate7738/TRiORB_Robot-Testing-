import logging
from triorb_robot_lib import TriOrbController

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    # Step 1: Connect to the robot
    device_path = "/dev/ttyACM0"
    robot = TriOrbController(device_path)

    robot.reset_origin()
    robot.wakeup()
    
    # You can also add custom operations:
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=1.0, axis='y')
    robot.lift(1)  # Lift up

    # Stop the robot at the end
    robot.stop()
    logging.info("Robot operations completed.")

if __name__ == "__main__":
    main()
