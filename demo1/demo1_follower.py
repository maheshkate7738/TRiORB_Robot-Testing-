import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from triorb_robot_lib import TriOrbController


class ContextualAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[Robot: {self.extra['robot_name']}] {msg}", kwargs


def main():
    robot_name = "Follower"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s (%(filename)s:%(lineno)d) [%(levelname)s] [Robot: %(robot_name)s] %(message)s",
    )
    # Add the robot name as part of the logger's context
    logger = ContextualAdapter(logging.getLogger(__name__), {"robot_name": robot_name})

    # Step 1: Connect to the robot
    device_path = "/dev/ttyACM0"
    robot = TriOrbController(device_path)

    logger.info("Resetting origin...")
    robot.reset_origin()
    logger.info("Waking up the robot...")
    robot.wakeup()

    # Custom operations
    logger.info("Starting movements...")
    robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=0.9, axis="y")
    robot.lift(1)  # Lift up
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=2.5, axis="y")
    robot.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=2.5, axis="y")
    robot.lift(-1)  # Lift down
    robot.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=0.9, axis="y")

    # Stop the robot at the end
    robot.stop()
    logger.info("Robot operations completed.")


if __name__ == "__main__":
    main()
