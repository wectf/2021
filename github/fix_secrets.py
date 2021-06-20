import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://github.com/login")
elem = driver.find_element_by_id("login_field")
elem.clear()
elem.send_keys("wectf-challs")


elem = driver.find_element_by_id("password")
elem.clear()
elem.send_keys("rATLkWSFUX8I")

elem.send_keys(Keys.RETURN)

for i in open("repos3").readlines():
    i = i.replace("\n", "")
    driver.get(f"https://github.com/wectf-challs/{i}/settings/actions")
    time.sleep(.5)
    elem = driver.find_element_by_name("fork_pr_workflows_policy[run_workflows]")
    if not elem.is_selected():
        elem.click()
    time.sleep(.1)

    elem = driver.find_element_by_name("fork_pr_workflows_policy[write_tokens]")
    if not elem.is_selected():
        elem.click()

    elem = driver.find_element_by_name("fork_pr_workflows_policy[send_secrets]")
    if not elem.is_selected():
        elem.click()

    driver.find_elements_by_class_name("btn")[8].click()

    time.sleep(1)

driver.close()

