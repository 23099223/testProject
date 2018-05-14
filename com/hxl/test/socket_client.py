import socket
import time
import sys
# import crawl
import json
import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)


# cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 连接服务端
# cli_socket.connect(('127.0.0.1', 9999))
# # 发送消息
# cli_socket.sendall('BYE'.encode('UTF-8'))
# # 接收服务端返回信息
# ser_msg = str(cli_socket.recv(1024), encoding="UTF-8")
# print("ser msg: %s" % ser_msg)
# cli_socket.close()

class SocketClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None
        self.families = self.get_constants('AF_')
        self.types = self.get_constants('SOCK_')
        self.protocols = self.get_constants('IPPROTO_')

    def get_constants(self, prefix):
        """Create a dictionary mapping socket module constants to their names."""
        return dict((getattr(socket, n), n)
                    for n in dir(socket)
                    if n.startswith(prefix)
                    )

    def send(self, message):
        try:
            # Create a TCP/IP socket
            logging.info("Line 40: connecting to %s" % self.server_port)
            self.sock = socket.create_connection((self.server_ip, self.server_port))
            # Send data
            logging.info('Line 43: connected! client sends %s' % message)
            self.sock.sendall(json.dumps(message).encode('utf8'))

            data = self.deal_recv_data()

            return data
        except Exception as err:
            # Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            logging.error('Line 50: Get Error Message: %s' % err)
            return None
        finally:
            if hasattr(self, 'sock'):
                self.sock.close()

    def deal_recv_data(self):
        return json.loads(self.sock.recv(1024).decode('utf8'))

# if __name__ == '__main__':
#     client = SocketClient('localhost', 3028)
#     recv_msg = client.send("hah")
#     logging.info(recv_msg)
#     if recv_msg.get("signal") == "done":
#         sys.exit(1)
#     while True:
#         # result = crawl.get_page_content(recv_msg, "depth_2")
#         # recv_msg = client.send(result[0])
#         if recv_msg.get("signal") == "done":
#             sys.exit(1)
#         print(recv_msg)
#         time.sleep(1)
