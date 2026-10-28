#!/usr/bin/env python3
import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from robo_interfaces.action import Deslocamento


class RoboDeslocamentoServidorNode(Node):
    def __init__(self):
        super().__init__("robo_deslocamento_servidor")
        self.latitude_atual_ = 0.0
        self.longitude_atual_ = 0.0
        self.action_server_ = ActionServer(
            self,
            Deslocamento,
            "deslocamento",
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
        )
        self.get_logger().info(
            f"Action Server 'deslocamento' iniciado. Posição inicial: "
            f"({self.latitude_atual_:.2f}, {self.longitude_atual_:.2f})"
        )

    def goal_callback(self, goal_request: Deslocamento.Goal):
        self.get_logger().info(
            f"Meta recebida -> Destino: ({goal_request.latitude_destino:.2f}, "
            f"{goal_request.longitude_destino:.2f}), "
            f"Velocidades: ({goal_request.velocidade_lat:.2f}, {goal_request.velocidade_lon:.2f})"
        )
        if (
            goal_request.latitude_destino == self.latitude_atual_
            and goal_request.longitude_destino == self.longitude_atual_
        ):
            self.get_logger().warn(
                "Rejeitando a meta: a localização de destino é igual à localização atual."
            )
            return GoalResponse.REJECT

        self.get_logger().info("Meta aceita! Iniciando deslocamento...")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Requisição de cancelamento recebida.")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        lat_dest = goal_handle.request.latitude_destino
        lon_dest = goal_handle.request.longitude_destino
        vel_lat = abs(goal_handle.request.velocidade_lat)
        vel_lon = abs(goal_handle.request.velocidade_lon)

        lat_atual = self.latitude_atual_
        lon_atual = self.longitude_atual_
        distancia_percorrida = 0.0

        feedback = Deslocamento.Feedback()
        result = Deslocamento.Result()

        while lat_atual != lat_dest or lon_atual != lon_dest:
            if goal_handle.is_cancel_requested:
                self.get_logger().info(
                    f"Meta cancelada! Distância percorrida: {distancia_percorrida:.2f}"
                )
                goal_handle.canceled()
                result.distancia_percorrida = distancia_percorrida
                return result

            time.sleep(1.0)

            diff_lat = lat_dest - lat_atual
            diff_lon = lon_dest - lon_atual

            passo_lat = math.copysign(min(vel_lat, abs(diff_lat)), diff_lat) if diff_lat != 0.0 else 0.0
            passo_lon = math.copysign(min(vel_lon, abs(diff_lon)), diff_lon) if diff_lon != 0.0 else 0.0

            lat_atual += passo_lat
            lon_atual += passo_lon
            distancia_percorrida += math.hypot(passo_lat, passo_lon)

            feedback.latitude_atual = lat_atual
            feedback.longitude_atual = lon_atual
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f"Feedback -> Localização atual: ({lat_atual:.2f}, {lon_atual:.2f}) | "
                f"Distância acumulada: {distancia_percorrida:.2f}"
            )

        goal_handle.succeed()
        result.distancia_percorrida = distancia_percorrida
        self.get_logger().info(
            f"Destino alcançado com sucesso! Distância total percorrida: {distancia_percorrida:.2f}"
        )
        return result


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoServidorNode()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
