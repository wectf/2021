import struct
import utils
import random
import time
from getmac import get_mac_address
import netifaces


EMPTY = struct.pack("B", 0)
INTERFACE = netifaces.gateways()['default'][netifaces.AF_INET][1]
MAC_ADDR = get_mac_address(interface=INTERFACE)
IP = utils.get_ip_addr(INTERFACE)
ROUTER_IP = netifaces.gateways()['default'][netifaces.AF_INET][0]
ROUTER_MAC = get_mac_address(ip=ROUTER_IP)
print(INTERFACE, ROUTER_IP)


class Ether:
    SRC = b''
    DST = b''
    TYPE = b''

    def __init__(self):
        self.SRC = self.parse_mac(MAC_ADDR)
        self.DST = self.parse_mac(ROUTER_MAC)
        self.TYPE = struct.pack(">H", 0x800)

    @staticmethod
    def parse_mac(mac):
        result = b''
        try:
            for part in mac.split(':'):
                result += struct.pack('B', int("0x" + part, 16))
        except Exception as e:
            pass
        return result

    def payload(self):
        return self.DST + self.SRC + self.TYPE


# IPv4 headers
class IPv4:
    HEADER_PROTO_OPT = struct.pack("B", 0x45) + EMPTY  # IPv4 Magic
    TOTAL_LEN = EMPTY + EMPTY
    IDENTIFICATION = struct.pack("BB", 0xcc, 0x7d)  # Something Random
    FLAG = struct.pack("B", 0x40) + EMPTY  # Normal Flags
    TTL = struct.pack("B", 0x40)  # TTL = 64
    PROTOCOL = b''
    CHECKSUM = EMPTY + EMPTY  # Placeholder
    SOURCE = b''
    DESTINATION = b''

    def __init__(self, _ip, _proto=0x01):  # use ICMP by default, UDP is also fine even with ICMP payload
        self.DESTINATION = self.parse_ip(_ip)
        self.SOURCE = self.parse_ip(IP)
        self.PROTOCOL = struct.pack("B", _proto)

    @staticmethod
    def parse_ip(_ip):
        result = b''
        try:
            for part in _ip.split('.'):
                result += struct.pack('B', int(part))
        except Exception as e:
            pass
        return result

    def calc_checksum(self):
        _data = self.payload()
        _sum = 0
        for i in range(0, len(_data), 2):
            if i < len(_data) and (i + 1) < len(_data):
                _sum += (_data[i] + (_data[i + 1] << 8))
            elif i < len(_data) and (i + 1) == len(_data):
                _sum += _data[i]
        addon_carry = (_sum & 0xffff) + (_sum >> 16)
        result = (~addon_carry) & 0xffff
        result = result >> 8 | ((result & 0x00ff) << 8)
        self.CHECKSUM = struct.pack('>H', result)

    def set_len(self, n):
        self.TOTAL_LEN = struct.pack(">H", n + 20)

    def payload(self):
        return self.HEADER_PROTO_OPT + \
               self.TOTAL_LEN + \
               self.IDENTIFICATION + \
               self.FLAG + \
               self.TTL + \
               self.PROTOCOL + \
               self.CHECKSUM + \
               self.SOURCE + \
               self.DESTINATION


# ICMP headers
class ICMP:
    TYPE = struct.pack("B", 0x8)
    CODE = EMPTY
    CHECKSUM = EMPTY + EMPTY  # Placeholder
    identifier = random.randint(0, 0x7fff)
    IDENTIFIER = struct.pack("H", identifier)
    SEQ_NUM = struct.pack("H", 1337)
    TIMESTAMP = struct.pack("I", int(time.time())) + EMPTY + EMPTY + EMPTY + EMPTY

    # nothing wrong, no need to read it, it just gives a correct checksum
    def calc_checksum(self):
        source_string = self.payload()
        _sum = 0
        countTo = (len(source_string) / 2) * 2
        count = 0
        while count < countTo:
            thisVal = source_string[count + 1] * 256 + source_string[count]
            _sum = _sum + thisVal
            _sum = _sum & 0xffffffff
            count = count + 2
        if countTo < len(source_string):
            _sum = _sum + source_string[len(source_string) - 1]
            _sum = _sum & 0xffffffff
        _sum = (_sum >> 16) + (_sum & 0xffff)
        _sum = _sum + (_sum >> 16)
        answer = ~_sum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        self.CHECKSUM = struct.pack(">H", answer)

    def payload(self):
        return self.TYPE + \
               self.CODE + \
               self.CHECKSUM + \
               self.IDENTIFIER + \
               self.SEQ_NUM + \
               self.TIMESTAMP


def get_ping_payload(_ip, _proto=0x01):
    ether = Ether()
    ipv4 = IPv4(_ip, _proto=_proto)
    icmp = ICMP()
    icmp.calc_checksum()
    icmp_payload = icmp.payload()
    ipv4.set_len(len(icmp_payload))
    ipv4.calc_checksum()
    print(ether.payload())
    return ether.payload() + ipv4.payload() + icmp_payload

