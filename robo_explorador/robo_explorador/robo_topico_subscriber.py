#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from robo_interfaces.msg import Monitoramento


class RoboTopicoSubscriberNode(Node):
    def __init__(self):
        super().__init__("robo_topico_subscriber")
        self.subscriber_ = self.create_subscription(
            Monitoramento, "monitoramento", self.callback_monitoramento, 10
        )
        self.get_logger().info("Estação base (subscriber) iniciada. Aguardando dados de 'monitoramento'...")

    def callback_monitoramento(self, msg: Monitoramento):
        if 10.0 <= msg.temperatura <= 40.0 and msg.nivel_oxigenio > 80.0:
            situacao = "Safe"
        else:
            situacao = "Not Safe"

        self.get_logger().info(
            f"Oxigênio: {msg.nivel_oxigenio:.2f}% | Temperatura: {msg.temperatura:.2f}°C -> {situacao}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
