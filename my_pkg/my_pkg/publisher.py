import math

import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

from my_pkg.gui import GUI

class ArmPublisher(Node):
    def __init__(self):
        super().__init__("arm_publisher")

        self.publisher = self.create_publisher(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            10
        )

        self.get_logger().info("Arm publisher started")

        # Start GUI and pass our publish function to it
        self.gui = GUI(self.send_trajectory)

        # Process ROS events while Tkinter is running
        self.gui.root.after(10, self.ros_spin)

    #PUBLISH
    def send_trajectory(self, angles):
        msg = JointTrajectory()

        msg.joint_names = [
            "joint1",
            "joint2",
            "joint3",
            "joint4",
            "joint5"
        ]

        point = JointTrajectoryPoint()

        point.positions = [
            math.radians(angles["joint1"]),
            math.radians(angles["joint2"]),
            math.radians(angles["joint3"]),
            math.radians(angles["joint4"]),
            math.radians(angles["joint5"])
        ]

        point.time_from_start.sec = 1

        msg.points.append(point)

        self.publisher.publish(msg)

        self.get_logger().info(
            "Trajectory published"
        )

    #ROS SPIN
    def ros_spin(self):
        rclpy.spin_once(self, timeout_sec=0)
        self.gui.root.after(10, self.ros_spin)

def main(args=None):
    rclpy.init(args=args)
    node = ArmPublisher()

    try:
        node.gui.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()