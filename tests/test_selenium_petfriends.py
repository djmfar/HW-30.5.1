import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_show_all_pets(web_browser):
   # Проверяем, что мы оказались на главной странице пользователя
   assert web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets'


def test_show_my_pets(web_browser):
   # Переходим на страницу питомцев пользователя
   web_browser.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
   # Проверяем, что мы оказались на странице с питомцами пользователя
   assert web_browser.current_url == 'https://petfriends.skillfactory.ru/my_pets', "login error"

   # список всех объектов питомца, в котором есть атрибут ".text"
   WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody')))
   all_my_pets = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

   # проверяем, что список своих питомцев не пуст
   assert len(all_my_pets) > 0, "у пользователя нет своих питомцев"

   # Проверяем, что присутствуют все питомцы
   pets_in_statistic = int(
       web_browser.find_element(By.XPATH, '//div[contains(@class, ".col-sm-4 left")]').
       text.split("\n")[1].split()[1])
   assert len(all_my_pets) == pets_in_statistic, "отображаются не все питомцы"

   # список фото питомцев - пустых и реальных
   all_photo_my_pets = web_browser.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
   list_photo_my_pets = 0 # переменная для подсчета реальных фото
   for i in range(len(all_photo_my_pets)):
       if all_photo_my_pets[i].get_attribute('src') != '': # если ссылка в списке фото не пустая, то
           list_photo_my_pets += 1  # увеличиваем количество реальных фото на 1

   # проверяем, есть ли фото хотя бы у половины питомцев
   assert list_photo_my_pets >= len(all_my_pets) / 2, "фото есть меньше, чем у половины питомцев"

   list_data_my_pets = [] # список данных своих питомцев
   list_name_my_pets = [] # список имен своих питомцев
   list_breed_my_pets = [] # список пород своих питомцев
   list_age_my_pets = [] # список возрастов своих питомцев

   for i in range(len(all_my_pets)):
       list_data = all_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
       list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список питомцев
       list_data = list_data_my_pets[i].split()  # разделяем имя, породу и возраст питомца
       list_name_my_pets.append(list_data[0])  # выбираем элемент с именем питомца и добавляем его в список имен
       list_breed_my_pets.append(list_data[1])  # выбираем элемент с породой питомца и добавляем его в список пород
       list_age_my_pets.append(list_data[2])  # выбираем элемент с возрастом питомца и добавляем его в список возрастов

   for i in range(len(all_my_pets)): # проверяем, что для каждого питомца
       assert list_name_my_pets[i] != '', "имя питомца пустое" # его имя не пустое
       assert list_breed_my_pets[i] != '', "порода питомца пустая"  # его порода не пустая
       assert list_age_my_pets[i] != '', "возраст питомца пустой"  # его возраст не пустой

   set_data_my_pets = set(list_data_my_pets)  # преобразовываем список питомцев в множество питомцев
   # сравниваем длину списка и множества питомцев: без повторов должны совпасть
   assert len(list_data_my_pets) == len(set_data_my_pets), "есть повторяющиеся питомцы"

   set_name_my_pets = set(list_name_my_pets)  # преобразовываем список имен питомцев в множество имен питомцев
   # сравниваем длину списка и множества имен питомцев: без повторов должны совпасть
   assert len(list_name_my_pets) == len(set_name_my_pets), "есть повторяющиеся имена питомцев"
