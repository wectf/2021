import random

from requests import *

ADMIN_TOKEN = "CroRQgDwMmJdybKa"


def check(host):
    s = session()
    # index
    result = get(f"http://{host}/index")
    if b"/flag" not in result.content:
        return 0, "Dead"

    result = get(f"http://{host}/flag@3gh3ugh4m.css")

    if b"we{" in result.content:
        return 0, "Flag Leak 1 "

    result = get(f"http://{host}/flag")

    if b"we{" in result.content:
        return 0, "Flag Leak 2"

    result = get(f"http://{host}/flag@ufh48fk32.css", cookies={
        "token": ADMIN_TOKEN
    })

    if b"we{" not in result.content:
        return 0, "No Flag"

    result = get(f"http://{host}/flag@ufh48fk32.css")
    if b"we{" not in result.content:
        return 0, "Cant pwn"

    return 1, ""


FUNCTIONS = [check]

if __name__ == "__main__":
    print(check("172.17.0.2:1006"))
