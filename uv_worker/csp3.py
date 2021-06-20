FLAG = "we{d36c47dc-b578-4736-92e0-2368894e6fbb@r3p0rt_ur1_even_13aks_nonce}"


def check(selenium_obj, host):
    current_host = f"http://csp3.{host}/"
    selenium_obj.get(current_host)
    selenium_obj.add_cookie({'name': 'flag', 'value': FLAG, 'path': '/'})
