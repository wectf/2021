from requests import *
import random


def check(host):
    s = session()
    # index
    result = s.get(f"http://{host}/")
    if b"Sign in to iCloud" not in result.content:
        return 0, "Failed to get"

    # get url
    result = s.post(f"http://{host}/add", data={
        "username": "shou",
        "password": "123"
    })
    if b"UNIQUE constr" not in result.content:
        return 0, "No Shou"

    result = s.post(f"http://{host}/add", data={
        "username": f"wrvuivhrevhy40hi34v2c{random.randint(0,10000000)}",
        "password": "123"
    })

    if b"UNIQUE constr" in result.content:
        return 0, "Bad unique"
    if b"imgur" not in result.content:
        return 0, "Bad resp"

    return 1, ""


FUNCTIONS = [check]


if __name__ == "__main__":
    print(check("127.0.0.1:5000"))
