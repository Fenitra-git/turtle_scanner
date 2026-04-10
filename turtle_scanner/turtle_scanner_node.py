import math
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class TurtleScannerNode(Node):
    def __init__(self):
        super().__init__('turtle_scanner_node')

        # P2 : attribut pour stocker la pose du scanner
        self.pose_scanner = None

        # P2 : attribut pour stocker la pose de la cible
        self.pose_target = None

        # P3 : etat du balayage
        self.scan_finished = False

        # P4 : etat de la detection
        self.target_detected = False
        self.detection_radius = 1.5

        # P2 : subscriber sur /turtle1/pose
        self.subscription_scanner = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_scanner_callback,
            10
        )

        # P2 : subscriber sur /turtle_target/pose
        self.subscription_target = self.create_subscription(
            Pose,
            '/turtle_target/pose',
            self.pose_target_callback,
            10
        )

        # P3 : publisher sur /turtle1/cmd_vel
        self.publisher_cmd = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        # P4 : publisher sur /target_detected
        self.publisher_detected = self.create_publisher(
            Bool,
            '/target_detected',
            10
        )

        # P3 : parametres du serpentin
        self.nb_lignes = 5
        self.y_start = 1.0
        self.y_step = 2.0
        self.x_min = 1.0
        self.x_max = 10.0

        # P3 : parametres de commande
        self.Kp_ang = 4.0
        self.Kp_lin = 1.5
        self.linear_speed_max = 2.0
        self.waypoint_tolerance = 0.3

        # P3 : generation de la liste des waypoints
        self.waypoints = []
        self.current_waypoint_index = 0

        for i in range(self.nb_lignes):
            y = self.y_start + i * self.y_step

            if i % 2 == 0:
                self.waypoints.append((self.x_max, y))
            else:
                self.waypoints.append((self.x_min, y))

        # P3 : timer pour executer scan_step regulierement
        self.timer = self.create_timer(0.05, self.scan_step)

    def pose_scanner_callback(self, msg):
        # P2 : mise a jour de la pose du scanner
        self.pose_scanner = msg

    def pose_target_callback(self, msg):
        # P2 : mise a jour de la pose de la cible
        self.pose_target = msg

    def compute_angle(self, A, B):
        # P3 : calcul de l'angle entre deux points
        xA, yA = A
        xB, yB = B
        return math.atan2(yB - yA, xB - xA)

    def compute_distance(self, A, B):
        # P3 : calcul de la distance entre deux points
        xA, yA = A
        xB, yB = B
        return math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)

    def publish_detection_state(self):
        # P4 : publication de l'etat de detection
        detected_msg = Bool()
        detected_msg.data = self.target_detected
        self.publisher_detected.publish(detected_msg)

    def stop_turtle(self):
        # P4 : arret de la tortue
        cmd = Twist()
        self.publisher_cmd.publish(cmd)

    def scan_step(self):
        # P3 : attendre les poses avant de commencer
        if self.pose_scanner is None or self.pose_target is None:
            return

        # P4 : calcul de la distance entre le scanner et la cible
        scanner_position = (self.pose_scanner.x, self.pose_scanner.y)
        target_position = (self.pose_target.x, self.pose_target.y)
        target_distance = self.compute_distance(scanner_position, target_position)

        # P4 : detection de la cible
        if target_distance < self.detection_radius:
            if not self.target_detected:
                self.target_detected = True
                self.stop_turtle()
                self.get_logger().info(
                    f'Cible detectee a ({self.pose_target.x:.2f}, {self.pose_target.y:.2f}) !'
                )

            self.publish_detection_state()
            return

        # P4 : publication de False tant que la cible n'est pas detectee
        self.publish_detection_state()

        # P3 : arret si tous les waypoints sont termines
        if self.current_waypoint_index >= len(self.waypoints):
            if not self.scan_finished:
                self.stop_turtle()
                self.get_logger().info('Balayage termine')
                self.scan_finished = True
            return

        # P3 : position actuelle et waypoint courant
        current_position = (self.pose_scanner.x, self.pose_scanner.y)
        waypoint = self.waypoints[self.current_waypoint_index]

        # P3 : calcul de la distance au waypoint
        distance = self.compute_distance(current_position, waypoint)

        # P3 : passage au waypoint suivant si on est assez proche
        if distance < self.waypoint_tolerance:
            self.current_waypoint_index += 1
            return

        # P3 : calcul de l'angle desire
        theta_desired = self.compute_angle(current_position, waypoint)
        theta = self.pose_scanner.theta

        # P3 : calcul de l'erreur angulaire
        e = math.atan(math.tan((theta_desired - theta) / 2.0))

        # P3 : commande proportionnelle
        u = self.Kp_ang * e
        v = self.Kp_lin * distance

        # P3 : limitation de la vitesse lineaire
        if v > self.linear_speed_max:
            v = self.linear_speed_max

        # P3 : publication de la commande
        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = u
        self.publisher_cmd.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleScannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
