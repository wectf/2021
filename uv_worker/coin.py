FLAG = "d6ccfd3a4cc18807825030209caa91a71bc074bd0bef2a516f7374a3576c0595"

def check(selenium_obj, host):
    current_host = f"http://coin.{host}:4001/"
    selenium_obj.get(current_host)
    selenium_obj.add_cookie({'name': 'token', 'value': FLAG, 'path': '/'})
