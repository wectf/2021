import json
import time
import utils
import net
from config import redis_instance

p = redis_instance.pubsub()
p.subscribe("ping_req")


def handler(data):
    try:
        data = json.loads(data)
        ip = data["ip"]
        proto = int(data["protocol"])
        utils.l2_send(net.INTERFACE, net.get_ping_payload(ip, _proto=proto))
    except Exception as e:
        print(e)


while 1:
    msg = p.get_message()
    if msg and msg["type"] == "message":
        handler(msg["data"])
    time.sleep(0.0001)
