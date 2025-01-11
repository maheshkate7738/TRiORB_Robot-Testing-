
import time
from triorb_core import robot as TriOrbRobot

class TriOrbController:
    def __init__(self, device_path, logger, robot_type="follower", distance_offset_correction=0.11, angle_offset_correction=0.43):
        """
        Initialize the TriOrb robot.

        :param device_path: Path to the robot device.
        :param robot_type: Type of the robot ("follower" or "guider").
        :param distance_offset_correction: Offset correction for distance (meters).
        :param angle_offset_correction: Offset correction for angle (radians).
        """
        self.device_path = device_path
        self.robot_type = robot_type.lower()
        self.offset_correction = distance_offset_correction
        self.turn_offset = angle_offset_correction
        self.logger = logger
        try:
            self.logger.info("Initializing the TriOrb Robot...")
            self.robot = TriOrbRobot(self.device_path)
            self.logger.info("Robot initialized successfully!")
        except Exception as e:
            self.logger.error(f"Failed to initialize the robot: {e}")
            exit(1)

    def reset_origin(self):
        """Reset the robot's origin."""
        try:
            self.logger.info("Resetting origin...")
            for _ in range(2):
                self.robot.reset_origin()
        except Exception as e:
            self.logger.error(f"Failed to reset origin: {e}")

    def wakeup(self):
        """Wake up the robot."""
        try:
            self.logger.info("Waking up the robot...")
            for _ in range(2):
                self.robot.wakeup()
            time.sleep(3)
        except Exception as e:
            self.logger.error(f"Failed to wake up the robot: {e}")

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
            correction_distance = desired_distance * self.offset_correction
            adjusted_distance = max(desired_distance - correction_distance, 0)
            initial_position = getattr(self.robot.get_pos()[0], axis)
            self.logger.info(f"Starting movement along {axis}-axis for {desired_distance} meters (adjusted to {adjusted_distance} meters)...")

            for _ in range(3):
                self.robot.set_vel_absolute(x_vel, y_vel, z_vel, acc=acc, dec=dec)

            while True:
                current_position = getattr(self.robot.get_pos()[0], axis)
                if abs(current_position - initial_position) >= abs(adjusted_distance):
                    break
                time.sleep(0.05)
                self.logger.info(f"Current {axis.upper()} Position: {current_position:.2f} m")

            for _ in range(2):
                self.robot.brake()

            time.sleep(3)
            current_position = getattr(self.robot.get_pos()[0], axis)
            self.logger.info(f"Completed movement along {axis}-axis. Final Position: {current_position:.2f} m")
        except Exception as e:
            self.logger.error(f"Error during movement: {e}")

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
            adjusted_angle = max(desired_angle - self.turn_offset, 0)
            initial_angle = self.robot.get_pos()[0].w
            self.logger.info(f"Starting turn {direction} for {desired_angle} radians (adjusted to {adjusted_angle} radians)...")

            if direction == 'ccw':
                z_vel = -abs(z_vel)
            elif direction == 'cw':
                z_vel = abs(z_vel)
            else:
                raise ValueError("Invalid direction. Use 'cw' for clockwise or 'ccw' for counterclockwise.")

            while True:
                current_angle = self.robot.get_pos()[0].w
                if abs(current_angle - initial_angle) >= abs(adjusted_angle):
                    break
                self.robot.set_vel_absolute(0, 0, z_vel, acc=acc, dec=dec)
                time.sleep(0.05)
                self.logger.info(f"Current Angle: {current_angle:.2f} rad")

            for _ in range(2):
                self.robot.brake()

            time.sleep(3)
            current_angle = self.robot.get_pos()[0].w
            self.logger.info(f"Completed turn {direction}. Final Angle: {current_angle:.2f} rad")
        except Exception as e:
            self.logger.error(f"Error during turn: {e}")

    def lift(self, position):
        """
        Control the lifter to move up, down, or stop.

        :param position: Lifter position: 1 for up, -1 for down, 0 for stop.
        """
        if self.robot_type != "follower":
            self.logger.warning("Lift operation is not available for this robot type.")
            return

        try:
            self.logger.info(f"Starting lift operation: {'Up' if position == 1 else 'Down' if position == -1 else 'Stop'}")
            for attempt in range(5):
                response = self.robot.set_lifter_move(position)[0]
                if response == 1:
                    self.logger.info("Lift command executed successfully. Lift operation in progress...")
                    time.sleep(10)
                    self.logger.info("Lift operation completed.")
                    break
                elif response == 2:
                    self.logger.warning("One or more lifter motors are not energized. Retrying...")
                elif response == 3:
                    self.logger.error("Lifter motor encountered an error. Please restart the robot.")
                    return
                elif response == 4:
                    self.logger.warning("Failed to acquire motor status. Retrying...")
                else:
                    self.logger.warning(f"Unknown response code: {response}. Retrying...")
                time.sleep(1)
            else:
                self.logger.error("Lift operation failed after multiple attempts.")
        except Exception as e:
            self.logger.error(f"Error during lift operation: {e}")

    def stop(self):
        """Stop the robot."""
        try:
            self.logger.info("Stopping the robot.")
            for _ in range(2):
                self.robot.brake()
                self.robot.sleep()
            time.sleep(3)
        except Exception as e:
            self.logger.error(f"Failed to stop the robot: {e}")

    def get_pose(self):
        """
        Fetch and log the current pose of the robot.

        Logs the x, y, and omega (orientation) values.
        """
        try:
            pose = self.robot.get_pos()[0]
            x, y, omega = pose.x, pose.y, pose.w
            self.logger.info(f"Current Pose - X: {x:.2f} m, Y: {y:.2f} m, Omega: {omega:.2f} rad")
            return x, y, omega
        except Exception as e:
            self.logger.error(f"Failed to fetch the robot pose: {e}")
            return None, None, None
