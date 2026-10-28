#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from robo_interfaces.action import Deslocamento


class RoboDeslocamentoClienteNode(Node):
    def __init__(self):
        super().__init__("robo_deslocamento_cliente")
        self.action_client_ = ActionClient(self, Deslocamento, "deslocamento")

    def send_goal(self, lat_dest, lon_dest, vel_lat, vel_lon):
        self.get_logger().info("Aguardando o servidor de action 'deslocamento'...")
        self.action_client_.wait_for_server()

        goal = Deslocamento.Goal()
        goal.latitude_destino = lat_dest
        goal.longitude_destino = lon_dest
        goal.velocidade_lat = vel_lat
        goal.velocidade_lon = vel_lon

        self.get_logger().info(
            f"Enviando meta -> Destino: ({lat_dest:.2f}, {lon_dest:.2f}) | "
            f"Velocidades: ({vel_lat:.2f}, {vel_lon:.2f}) unid/s"
        )
        self.action_client_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback
        ).add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()
        if self.goal_handle_.accepted:
            self.get_logger().info("Meta aceita pelo servidor! Aguardando conclusão...")
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback
            )
        else:
            self.get_logger().warn("Meta rejeitada pelo servidor.")

    def goal_feedback_callback(self, feedback_msg):
        lat = feedback_msg.feedback.latitude_atual
        lon = feedback_msg.feedback.longitude_atual
        self.get_logger().info(f"Feedback recebido -> Localização atual: ({lat:.2f}, {lon:.2f})")

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Sucesso! Deslocamento finalizado.")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Ação abortada.")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Ação cancelada.")
        self.get_logger().info(
            f"Distância percorrida final: {result.distancia_percorrida:.2f} unidades"
        )


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoClienteNode()
    node.send_goal(10.0, 10.0, 1.0, 1.0)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
