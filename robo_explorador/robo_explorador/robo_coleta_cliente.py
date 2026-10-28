#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaMaterial


class RoboColetaClienteNode(Node):
    def __init__(self):
        super().__init__("robo_coleta_cliente")
        self.client_ = self.create_client(ColetaMaterial, "coleta_material")

    def call_coleta_material(self):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Aguardando o serviço 'coleta_material'...")

        request = ColetaMaterial.Request()
        request.profundidade = random.uniform(0.1, 0.5)
        self.get_logger().info(
            f"Solicitando coleta de solo na profundidade: {request.profundidade:.3f} m"
        )

        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_coleta_material_response)

    def callback_coleta_material_response(self, future):
        response = future.result()
        if response.sucesso:
            self.get_logger().info("Resposta recebida: Coleta bem sucedida!")
        else:
            self.get_logger().info("Resposta recebida: A coleta NÃO foi bem sucedida.")


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaClienteNode()
    node.call_coleta_material()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
