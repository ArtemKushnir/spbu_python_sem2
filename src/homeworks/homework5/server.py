import socket
from threading import Thread
from typing import Optional

from loguru import logger


class Server:
    def __init__(self) -> None:
        self.current_port: Optional[int] = None
        self.first_port: Optional[int] = None
        self.second_port: Optional[int] = None

    def give_response(self, clients: tuple[tuple[socket.socket, int], tuple[socket.socket, int]], data: bytes) -> None:
        message, sender_port = data.decode().split()
        logger.info(f"Received data from port: {sender_port}")
        if int(sender_port) == self.current_port:
            for client in clients:
                client[0].sendall(bytes(message, encoding="UTF-8"))
                logger.info(f"Send message: {message} to client: {client}")
            if self.current_port == self.first_port:
                self.current_port = self.second_port
            else:
                self.current_port = self.first_port

    def receive_data(self, current_client: tuple[socket.socket, int], other_client: tuple[socket.socket, int]) -> None:
        sock, addr = current_client
        while True:
            received_data = sock.recv(1024)
            if not received_data:
                break
            self.give_response((current_client, other_client), received_data)
        logger.info("Client disconnected:", sock.getpeername())


def main(ip: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(2)
    server = Server()
    logger.info(f"Server is running with ip: {ip}, port: {port}")
    while True:
        first_client_sock, first_addr = sock.accept()
        logger.info(f"Connected: {first_addr}")
        second_client_sock, second_addr = sock.accept()
        logger.info(f"Connected: {second_addr}")
        server.first_port = first_addr[1]
        server.second_port = second_addr[1]
        server.current_port = server.first_port

        first_client_thread = Thread(
            target=server.receive_data, args=((first_client_sock, first_addr), (second_client_sock, second_addr))
        )
        second_client_thread = Thread(
            target=server.receive_data, args=((second_client_sock, second_addr), (first_client_sock, first_addr))
        )
        first_client_thread.start()
        second_client_thread.start()


if __name__ == "__main__":
    main("127.0.0.1", 8888)
