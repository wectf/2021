FLAG = "we{2bf90f00-f560-4aee-a402-d46490b53541@just_L1k3_<sq1_injEcti0n>}"


def check(selenium_obj, host):
    current_host = f"http://csp1.{host}/"
    selenium_obj.get(current_host)
    selenium_obj.add_cookie({'name': 'flag', 'value': FLAG, 'path': '/'})
