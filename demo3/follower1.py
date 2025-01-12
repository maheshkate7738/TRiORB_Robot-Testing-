import logging
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from triorb_robot_lib import TriOrbController


class ContextualFilter(logging.Filter):
    def __init__(self, robot_name):
        super().__init__()
        self.robot_name = robot_name

    def filter(self, record):
        record.robot_name = self.robot_name
        return True


def configure_logger(robot_name):
    """Configure the logger with the contextual filter."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Set the log format
    formatter = logging.Formatter(
        "%(asctime)s (%(filename)s:%(lineno)d) [%(levelname)s] [Robot: %(robot_name)s] %(message)s"
    )

    # Create a stream handler and set the formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add contextual filter for robot_name
    logger.addFilter(ContextualFilter(robot_name))
    logger.addHandler(handler)

    return logger


def main():
    robot_name = "Follower 1"
    logger = configure_logger(robot_name)

    # Step 1: Connect to the robot
    device_path = "/dev/ttyACM0"
    robot = TriOrbController(device_path, logger, angle_offset_correction=0.28)

    logger.info("Resetting origin...")
    robot.reset_origin()
    logger.info("Waking up the robot...")
    robot.wakeup()

    # Custom operations
    logger.info("Starting movements...")
    robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=0.9, axis="y")
    robot.lift(1)  # Lift up
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=0.9, axis="y")
    time.sleep(7)
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=1.0, axis="y")
    robot.turn(desired_angle=1.57, direction='cw')
    robot.move(x_vel=0.2, y_vel=0, z_vel=0, desired_distance=2.0, axis="x")
    robot.turn(desired_angle=1.57, direction='cw')
    robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=0.5, axis="y")
    robot.lift(-1)  # Lift down
    # robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=0.9, axis="y")


    # robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=0.9, axis="y")
    # robot.lift(1)  # Lift up
    # robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=1.0, axis="y")
    # robot.turn(desired_angle=1.57, direction='cw')
    # robot.move(x_vel=0.2, y_vel=0, z_vel=0, desired_distance=1.0, axis="x")
    # robot.turn(desired_angle=1.57, direction='cw')
    # robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=0.5, axis="y")
    # robot.lift(-1)  # Lift down
    robot.get_pose()

    # Stop the robot at the end
    robot.stop()
    logger.info("Robot operations completed.")


if __name__ == "__main__":
    main()
