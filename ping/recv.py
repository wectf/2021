import base64
import json

from scapy.all import ICMP, IP, sniff

import net
from config import redis_instance


def pub_data(pkt):
    try:
        _ip = pkt[IP].src
        _ttl = pkt[IP].ttl
        _load = pkt[IP].load
        print(_ip, _ttl, _load)  # debug
        redis_instance.publish("ping_result", json.dumps({
            "ip": _ip,
            "ttl": _ttl,
            "load": base64.b64encode(_load).decode("utf-8")
        }))
    except Exception as e:
        print(e)


sniff(iface=net.INTERFACE, filter="ip", count=0, prn=pub_data)

