from requests import *


def check(host):
    s = session()
    # index
    result = s.get(f"http://{host}/")
    if b"Modify Backgroud" not in result.content:
        return 0, "Failed to get"

    if b"src=\"/static/default.gif\"" not in result.content:
        return 0, "No img"

    if not result.headers.get("Set-Cookie"):
        return 0, "No cookie set"

    files = {'file': b"123123"}

    # get url
    result = s.post(f"http://{host}/upload", files=files)
    r = result.content.split(b"      window.location.href = \"")[1].split(b'";\n        }\n    }\n    redirect();\n    window.onhashchange')[0]
    if s.get(r).content != b'123123':
        return 0, "Wrong content"
    result = s.get(f"http://{host}/")
    if r not in result.content:
        return 0, "Token not persist"

    # csp
    if "frame-ancestors 'none'" not in result.headers.get("Content-Security-Policy"):
        return 0, "CSP issue"
    return 1, ""




FUNCTIONS = [check]


if __name__ == "__main__":
    print(check("172.17.0.3:1000"))
