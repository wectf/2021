import socket
import fcntl
import struct
import os


def get_ip_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15].encode("latin-1"))
    )[20:24])


def l2_send(ifname, data):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))  # Layer 2 Socket
    s.bind((ifname, 0))  # Bind NIC
    s.sendall(data)  # Send Payload
    print(ifname, data)
    s.close()  # Wipe My Ass

