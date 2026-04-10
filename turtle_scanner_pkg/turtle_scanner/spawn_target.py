import random
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn

class SpawnTargetNode(Node):
    def __init__(self):
        super().__init__('spawn_target')

        # Q2 : creation du client du service /spawn
        self.spawn_client = self.create_client(Spawn, '/spawn')

        # Q2 : attente du service /spawn
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('En attente du service /spawn...')

        # Q2 : envoi de la requete de spawn
        self.spawn_target()

    def spawn_target(self):
        # Q2 : creation de la requete
        request = Spawn.Request()

        # Q2 : generation aleatoire des coordonnees dans [1, 10]
        request.x = random.uniform(1.0, 10.0)
        request.y = random.uniform(1.0, 10.0)

        # Q2 : orientation initiale et nom de la tortue cible
        request.theta = 0.0
        request.name = 'turtle_target'

        # Q3 : sauvegarde des coordonnees pour l'affichage
        self.target_x = request.x
        self.target_y = request.y

        # Q2 : appel asynchrone du service
        self.future = self.spawn_client.call_async(request)

def main(args=None):
    rclpy.init(args=args)
    node = SpawnTargetNode()
    rclpy.spin_until_future_complete(node, node.future)

    # Q3 : affichage des coordonnees si le spawn a reussi
    if node.future.result() is not None:
        node.get_logger().info(
            f'Cible creee en x={node.target_x:.2f}, y={node.target_y:.2f}'
        )
    else:
        node.get_logger().info('Le spawn a echoue')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
