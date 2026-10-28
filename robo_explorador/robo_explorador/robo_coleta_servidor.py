#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from robo_interfaces.srv import ColetaMaterial


class RoboColetaServidorNode(Node):
    def __init__(self):
        super().__init__("robo_coleta_servidor")
        self.service_ = self.create_service(
            ColetaMaterial, "coleta_material", self.callback_coleta_material
        )
        self.get_logger().info("Servidor de coleta 'coleta_material' iniciado e pronto.")

    def callback_coleta_material(
        self, request: ColetaMaterial.Request, response: ColetaMaterial.Response
    ):
        valor_aleatorio = random.uniform(0.0, 1.0)
        response.sucesso = valor_aleatorio <= 0.7
        self.get_logger().info(
            f"Requisição recebida (profundidade={request.profundidade:.3f} m) | "
            f"Sorteio={valor_aleatorio:.2f} -> Sucesso={response.sucesso}"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaServidorNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
