import logging
import time
from triorb_core import robot as TriOrbRobot


class TriOrbController:
    def __init__(self, device_path, distance_offset_correction=0.1, angle_offset_correction=0.42):
        """
        Initialize the TriOrb robot.

        :param device_path: Path to the robot device.
        :param offset_correction: Offset correction for each motion (meters).
        """
        self.device_path = device_path
        self.offset_correction = distance_offset_correction
        self.turn_offset = angle_offset_correction
        try:
            logging.info("Initializing the TriOrb Robot...")
            self.robot = TriOrbRobot(self.device_path)
            logging.info("Robot initialized successfully!")
        except Exception as e:
            logging.error(f"Failed to initialize the robot: {e}")
            exit(1)

    def reset_origin(self):
        """Reset the robot's origin."""
        try:
            logging.info("Resetting origin...")
            for _ in range(2):
                self.robot.reset_origin()
        except Exception as e:
            logging.error(f"Failed to reset origin: {e}")

    def wakeup(self):
        """Wake up the robot."""
        try:
            logging.info("Waking up the robot...")
            for _ in range(2):
                self.robot.wakeup()
            time.sleep(3)
        except Exception as e:
            logging.error(f"Failed to wake up the robot: {e}")

    def move(self, x_vel, y_vel, z_vel, desired_distance, axis, acc=350, dec=350):
        """
        Move the robot in a specified direction, adjusting for hardware offset.

        :param x_vel: Velocity along the X-axis.
        :param y_vel: Velocity along the Y-axis.
        :param z_vel: Angular velocity.
        :param desired_distance: Desired distance to move in meters.
        :param axis: Axis of movement ('x' or 'y').
        :param acc: Acceleration.
        :param dec: Deceleration.
        """
        try:
            # Adjust distance based on the offset correction
            correction_distance = desired_distance * self.offset_correction
            adjusted_distance = max(desired_distance - correction_distance, 0)
            initial_position = getattr(self.robot.get_pos()[0], axis)
            logging.info(f"Starting movement along {axis}-axis for {desired_distance} meters (adjusted to {adjusted_distance} meters)...")
            
            for _ in range(3):  # Ensures multiple API calls for hardware consistency
                self.robot.set_vel_absolute(x_vel, y_vel, z_vel, acc=acc, dec=dec)

            while True:
                current_position = getattr(self.robot.get_pos()[0], axis)
                if abs(current_position - initial_position) >= abs(adjusted_distance):
                    break
                time.sleep(0.05)
                logging.info(f"Current {axis.upper()} Position: {current_position:.2f} m")

            for _ in range(2):  # Ensures multiple API calls to stop the robot
                self.robot.brake()

            time.sleep(3)  # Give time for the robot to fully stop
            current_position = getattr(self.robot.get_pos()[0], axis)
            logging.info(f"Completed movement along {axis}-axis. Final Position: {current_position:.2f} m")
        except Exception as e:
            logging.error(f"Error during movement: {e}")

    def turn(self, desired_angle, direction, z_vel=0.5, acc=350, dec=350):
        """
        Turn the robot in a specified direction, adjusting for angular offset.

        :param desired_angle: Desired angle to turn in radians.
        :param direction: Direction of rotation ('cw' for clockwise, 'ccw' for counterclockwise).
        :param z_vel: Angular velocity (rad/s).
        :param acc: Angular acceleration.
        :param dec: Angular deceleration.
        """
        try:
            # Adjust angle based on the angular offset
            adjusted_angle = max(desired_angle - self.turn_offset, 0)
            initial_angle = self.robot.get_pos()[0].w  # Assuming theta represents the robot's orientation
            logging.info(f"Starting turn {direction} for {desired_angle} radians (adjusted to {adjusted_angle} radians)...")

            # Determine angular velocity direction
            if direction == 'ccw':  # Clockwise
                z_vel = -abs(z_vel)
            elif direction == 'cw':  # Counterclockwise
                z_vel = abs(z_vel)
            else:
                raise ValueError("Invalid direction. Use 'cw' for clockwise or 'ccw' for counterclockwise.")

            for _ in range(3):  # Ensures multiple API calls for hardware consistency
                self.robot.set_vel_absolute(0, 0, z_vel, acc=acc, dec=dec)

            while True:
                current_angle = self.robot.get_pos()[0].w
                if abs(current_angle - initial_angle) >= abs(adjusted_angle):
                    break
                time.sleep(0.05)
                logging.info(f"Current Angle: {current_angle:.2f} rad")

            for _ in range(2):  # Ensures multiple API calls to stop the robot
                self.robot.brake()

            time.sleep(3)  # Give time for the robot to fully stop
            current_angle = self.robot.get_pos()[0].w
            logging.info(f"Completed turn {direction}. Final Angle: {current_angle:.2f} rad")
        except Exception as e:
            logging.error(f"Error during turn: {e}")

    def stop(self):
        """Stop the robot."""
        try:
            logging.info("Stopping the robot.")
            for _ in range(2):  # Ensures multiple API calls to stop the robot
                self.robot.brake()
                self.robot.sleep()
            time.sleep(3)
        except Exception as e:
            logging.error(f"Failed to stop the robot: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s")

    # Initialize the robot controller with an offset correction of 0.15 meters
    robot_controller = TriOrbController("/dev/ttyACM0")

    for _ in range(1):
        # Wake up the robot and reset origin
        robot_controller.reset_origin()
        robot_controller.wakeup()

        # Move forward 1.5 meters (adjusted for offset)
        robot_controller.move(x_vel=0, y_vel=0.2, z_vel=0, desired_distance=1.5, axis='y')

        # Turn 1.57 radian clockwise
        robot_controller.turn(desired_angle=1.57, direction='cw')

        # Move backward 1.5 meters to return to the origin (adjusted for offset)
        # robot_controller.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=1.0, axis='y')
        
        robot_controller.move(x_vel=0.0, y_vel=0.2, z_vel=0, desired_distance=1.0, axis='x')

        # Turn 1.57 radian clockwise
        robot_controller.turn(desired_angle=1.57, direction='cw')

        robot_controller.move(x_vel=0, y_vel=-0.2, z_vel=0, desired_distance=1.5, axis='y')

        # Turn 1.57 radian clockwise
        robot_controller.turn(desired_angle=1.57, direction='cw')

        robot_controller.move(x_vel=-0.2, y_vel=0.0, z_vel=0, desired_distance=1.0, axis='x')

        # Turn 1.57 radian clockwise
        robot_controller.turn(desired_angle=1.57, direction='cw')

        # Stop the robot
        robot_controller.stop()
        logging.info("Robot forward and backward movement sequence completed.")


if __name__ == "__main__":
    main()
