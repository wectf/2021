import random

from requests import *


def check(host):
    s = session()
    # index
    result = s.get(f"http://{host}/")
    if b"Login / Register" not in result.content:
        return 0, "Dead"

    # login
    result = s.post(f"http://{host}/register", data={
        "username": f"shoushoushou@2ugf4f8x{random.randint(0, 1000000)}",
        "password": "shoushoushou@2ugf4f8"
    })

    if b"Add links here!" not in result.content:
        return 0, "Cant login"

    # create
    result = s.post(f"http://{host}/add", data={
        "link": "1231221",
        "description": "123123"
    })

    if b"1231221" not in result.content:
        return 0, "Cant add link"


    # search
    result = s.get(f"http://{host}/?keyword=jjj")

    if b"1231221" in result.content:
        return 0, "Cant search link 1"

    result = s.get(f"http://{host}/?keyword=123")

    if b"1231221" not in result.content:
        return 0, "Cant search link 2"

    # pin
    result = s.post(f"http://{host}/pin", data={
        "link": "1231221",
    })
    if b'Unpin' not in result.content:
        return 0, "Cant pin link"

    result = s.post(f"http://{host}/unpin", data={
        "link": "1231221",
    })
    if b'Unpin' in result.content:
        return 0, "Cant unpin link"

    return 1, ""


FUNCTIONS = [check]


if __name__ == "__main__":
    print(check("172.17.0.5:1004"))
