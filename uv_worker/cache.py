  
PASSWORD = "CroRQgDwMmJdybKa"


def check(selenium_obj, host):
    current_host = f"http://cache.{host}/"
    selenium_obj.get(current_host)
    selenium_obj.add_cookie({'name': 'token', 'value': PASSWORD, 'path': '/'})
