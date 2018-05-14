import urllib3
from lxml import etree
import crawl_config as cc
import socket_config as sc
import logging
from socket_client import SocketClient
import sys
from time import sleep

logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)
urllib3.disable_warnings()


def get_page_content(cur_url, depth, encoding="utf-8"):
    logging.info("Line 9: downloading %s at level %s " % (cur_url, depth))
    try:
        proxy_ip = cc.get_proxy_ip()
        if proxy_ip:
            http = urllib3.ProxyManager()
        else:
            http = urllib3.PoolManager()
        r = http.request('GET', cur_url, headers=cc.get_request_headers())
    except IOError as err:
        logging.error("Line 19: %s" % str(err))
        raise
    except Exception as err:
        logging.error("Line 23: %s" % str(err))
        raise
    html = etree.HTML(r.data.lower().decode(encoding))
    ret_from_page = cc.get_depth_result(html, depth)
    return ret_from_page


# 初始传入注册的id号
def init(clid):
    global client_socket
    global client_id
    client_socket = SocketClient(sc.ser_ip, sc.ser_port)
    # sign in
    recv_msg_1 = client_socket.send({"signal": "sign", "client_id": clid})
    if recv_msg_1.get("client_id"):
        client_id = recv_msg_1.get("client_id")
        logging.info("client_id: %s" % client_id)
    else:
        sys.exit(recv_msg_1.get("erro"))
    logging.info("Line 44: client_id = %s" % client_id)


init("test1")
recv_msg = client_socket.send({"client_id": client_id})
if recv_msg.get("signal") == "done":
    sys.exit(1)

while True:
    # recv_msg = client_socket.send({"client_id": client_id})
    result = get_page_content(recv_msg.get("url"), "depth_2")
    recv_msg = client_socket.send({"client_id": client_id, "signal": "crawl", "result": result})
    if recv_msg.get("signal") == "done":
        logging.info("Line 56: server kill me, signal is %s" % recv_msg.get("signal"))
        sys.exit(1)
    logging.info("Line 58: recv_msg is %s" % recv_msg)
    sleep(1)

    # if __name__ == "__main__":
    # print(cc.get_depth_xpath("depth_1"))
    # print(get_page_content("http://www.mafengwo.cn", "depth_2"))
