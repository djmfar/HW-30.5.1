# content of file conftest.py
import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request):
    browser = webdriver.Chrome()
    browser.maximize_window()

    browser.implicitly_wait(3)
    # Переходим на страницу авторизации
    browser.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    browser.find_element(By.ID, 'email').send_keys('abcd@mail.ru')
    # Вводим пароль
    browser.find_element(By.ID, 'pass').send_keys('qwerty123')
    # Нажимаем на кнопку входа в аккаунт
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что загрузилась таблица со всеми питомцами
    browser.find_element(By.CLASS_NAME, 'card-deck')

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):
    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")
            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')
            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)
        except:
            pass # just ignore any errors here

    browser.quit()