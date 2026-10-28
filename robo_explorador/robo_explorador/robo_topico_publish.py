#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento


class RoboTopicoPublishNode(Node):
    def __init__(self):
        super().__init__("robo_topico_publish")
        self.publisher_ = self.create_publisher(Monitoramento, "monitoramento", 10)
        self.timer_ = self.create_timer(1.0, self.publish_monitoramento)
        self.get_logger().info("Nó do robô (publisher) iniciado no tópico 'monitoramento'.")

    def publish_monitoramento(self):
        msg = Monitoramento()
        msg.nivel_oxigenio = random.uniform(1.0, 100.0)
        msg.temperatura = random.uniform(1.0, 100.0)
        self.publisher_.publish(msg)
        self.get_logger().info(
            f"Publicado -> Oxigênio: {msg.nivel_oxigenio:.2f}% | Temperatura: {msg.temperatura:.2f}°C"
        )


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoPublishNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
