PASSWORD = "UtOF3tbWJaHSCImY"

def check(selenium_obj, host):
    current_host = f"http://gallery.{host}/"
    selenium_obj.get(current_host)
    selenium_obj.add_cookie({'name': 'token', 'value': PASSWORD, 'path': '/'})
