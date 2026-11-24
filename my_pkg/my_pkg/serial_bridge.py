import rclpy
import serial
import math

from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory


class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')

        self.esp = serial.Serial(
            '/dev/ttyUSB0',
            115200,
            timeout=1
        )

        self.create_subscription(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            self.trajectory_callback,
            10
        )

        self.get_logger().info('Serial bridge started')

    #Angle conversion method
    def angle_to_servo(self, radians, offset=90):
        degrees = round(math.degrees(radians) + offset)
        return degrees

    #Callback for trajectory messages
    def trajectory_callback(self, msg):
        if not msg.points:
            return

        positions = msg.points[-1].positions

        required_joints = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'joint5'
        ]

        # Ensure all required joints exist
        if not all(joint in msg.joint_names for joint in required_joints):
            self.get_logger().warn('Missing joint in trajectory')
            return

        # Map joint names to positions
        joint_positions = {
            name: positions[msg.joint_names.index(name)]
            for name in required_joints
        }

        #Convert from radians to degrees and apply offsets
        # Base: -60 to +60 -> 30 to 150
        base = self.angle_to_servo(
            joint_positions['joint1']
        )

        # Shoulder: centered at 90
        shoulder = self.angle_to_servo(
            joint_positions['joint2']
        )

        # Elbow: centered at 90
        elbow = self.angle_to_servo(
            joint_positions['joint3']
        )

        # Wrist: centered at 90
        wrist = self.angle_to_servo(
            joint_positions['joint4']
        )

        # Gripper: absolute 0 to 90
        gripper = round(
            math.degrees(joint_positions['joint5'])
        )

        #Constrain angles to valid ranges
        base = max(30, min(150, base))
        shoulder = max(60, min(120, shoulder))
        elbow = max(45, min(135, elbow))
        wrist = max(45, min(135, wrist))
        gripper = max(0, min(90, gripper))

        #Serial command
        command = (
            f'{base},{shoulder},{elbow},{wrist},{gripper}\n'
        )

        self.esp.write(command.encode())

        self.get_logger().info(
            f'Sent: {base},{shoulder},{elbow},{wrist},{gripper}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = SerialBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.esp.is_open:
            node.esp.close()

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()