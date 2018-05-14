import socket
import sys
import _thread
import signal
import os
import threading
import logging
import json
import socket_config as sc
import mongo_redis_mgr as mrmg

logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)


class ServerSocket:
    def __init__(self, callback, mongo_redis, host='localhost', port=3028):
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback
        self.mongo_redis = mongo_redis
        try:
            print("bind ", port)
            self.ser_socket.bind((host, port))
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.ser_socket.listen(10)
        self.kill_conn = "local"

    def receive_signal(self, signum, stack):
        self.kill_conn = self.mongo_redis.logout_client(flag=False)  # 会由数据库控制
        print(self.kill_conn)

    def startlistening(self):
        while True:
            print('Waiting for new connection ... ')
            conn, addr = self.ser_socket.accept()
            # _thread.start_new_thread(self.clientthread, (conn,))
            t = threading.Thread(target=self.clientthread, name='clientthread', args=(conn, addr))
            t.start()

    def deal_recv_data(self, conn):
        return json.loads(conn.recv(1024).decode('utf8'))

    def clientthread(self, conn, addr):
        data = self.deal_recv_data(conn)
        # sleep(10)
        client_id = data.get("client_id")
        logging.info("Line 45: %s: %s" % (addr[0], addr[1]))
        logging.info("Line 45: recv_data: %s" % data)
        if self.kill_conn == data.get("client_id"):
            conn.sendall(json.dumps({"signal": "done"}).encode("utf-8"))
            self.kill_conn = "local"
        else:
            if data.get("signal") == "sign":
                if self.mongo_redis.sign_check_client(client_id):
                    conn.sendall(json.dumps({"client_id": client_id}).encode('utf8'))
                else:
                    conn.sendall(json.dumps({"erro": "1"}).encode('utf8'))
            elif data.get("signal") == "heart":
                pass
            elif data.get("signal") == "logout":
                pass
            else:
                if self.mongo_redis.sign_check_client(client_id, True):
                    conn.sendall(self.send_msg())
                else:
                    conn.sendall(json.dumps({"erro": "2"}).encode('utf8'))

        conn.close()

    # 需要改
    def send_msg(self):
        msg = json.dumps({"url": "http://www.mafengwo.cn",
                          "signal": "crawl",
                          "depth": "depth_2"}).encode('utf8')

        return msg

    def start(self):
        t = threading.Thread(target=self.startlistening, name='startlistening', args=())
        t.start()
        # _thread.start_new_thread(self.startlistening, ())

    def close(self):
        # self.s.shutdown(socket.SHUT_WR)
        self.s.close()


def msg_received(data):
    ret = data.decode('utf8')
    return ret


if __name__ == "__main__":
    # 注册信号处理程序
    logging.info("Line 86: PID = %s" % os.getpid())
    server = ServerSocket(msg_received, mrmg.MongoRedisManager(), host=sc.ser_ip, port=sc.ser_port)
    signal.signal(signal.SIGUSR1, server.receive_signal)
    server.start()
    # time.sleep(10)
    # 等待直到接收一个信号
    # signal.pause()
