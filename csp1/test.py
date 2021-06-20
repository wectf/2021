from requests import *


def check(host):
    s = session()
    # index
    result = s.get(f"http://{host}/")
    if b"Give HTML:" not in result.content:
        return 0, "Failed to get"

    # get url
    result = s.post(f"http://{host}/write", data={
        "content": "123"
    })
    if "display" not in result.url:
        return 0, "Bad url"

    if b"123" not in result.content:
        return 0, "Bad result"

    if "connect-src 'self';" not in result.headers.get("Content-Security-Policy"):
        return 0, "Bad CSP"

    result = s.post(f"http://{host}/write", data={
        "content": "123<img src=\"https://google.c;script-src 'unsafe-inline'\" /><script>alert(1)</script>"
    })
    if "script-src 'unsafe-inline';" not in result.headers.get("Content-Security-Policy"):
        return 0, "Cannot pwn"

    return 1, ""


FUNCTIONS = [check]


if __name__ == "__main__":
    print(check("172.17.0.4:1003"))
