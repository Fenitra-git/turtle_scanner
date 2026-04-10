import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtleScannerNode(Node):
    def __init__(self):
        super().__init__('turtle_scanner_node')

        # Q2 : attribut pour stocker la pose du scanner
        self.pose_scanner = None

        # Q3 : attribut pour stocker la pose de la cible
        self.pose_target = None

        # Q2 : subscriber sur /turtle1/pose
        self.subscription_scanner = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_scanner_callback,
            10
        )

        # Q3 : subscriber sur /turtle_target/pose
        self.subscription_target = self.create_subscription(
            Pose,
            '/turtle_target/pose',
            self.pose_target_callback,
            10
        )

    def pose_scanner_callback(self, msg):
        # Q2 : mise a jour de la pose du scanner
        self.pose_scanner = msg
        self.get_logger().info(f"scanner : x={msg.x:.2f}, y={msg.y:.2f}")

    def pose_target_callback(self, msg):
        # Q3 : mise a jour de la pose de la cible
        self.pose_target = msg
        self.get_logger().info(f"target : x={msg.x:.2f}, y={msg.y:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleScannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
