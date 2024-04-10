import os
import time
from datetime import datetime
from selenium import webdriver as selenium_wd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://petfriends.skillfactory.ru"
USER = "kozdrin2013@yandex.ru"
PASSWORD = "qwerty"


@pytest.fixture(scope="session")
def selenium_driver(request):
    s = Service(executable_path=ChromeDriverManager().install())
    chrome_options = Options()
    driver = selenium_wd.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(BASE_URL+"/login")
    WDW(driver, 2).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, "email").send_keys(USER)
    driver.find_element(By.ID, "pass").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
     yield
     if request.node.rep_setup.outcome == 'failed':
         print("Test installation failed:", request.node.nodeid)
     elif request.node.rep_setup.outcome == 'passed':
         if request.node.rep_call.failed:
             driver = request.node.funcargs["selenium_driver"]
             take_screenshot(driver, request.node.nodeid)
             print("Test execution failed:", request.node.nodeid)


def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.png'.replace('/', '_' ).replace("::", "")
    print("Save screenshot as:", file_name)
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, file_name)
    driver.save_screenshot(file_path)