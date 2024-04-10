import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# python -m pytest -v --driver Chrome --driver-path указать_свой_путь_до_драйвера\chromedriver.exe tests.py
# Авторизация

driver = webdriver.Chrome()
def test_petfriends(selenium):
    # Open PetFriends base page:
    selenium.get('https://petfriends.skillfactory.ru/')

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # click on the new user button
    btn_newuser = selenium.find_element(By.XPATH, '//body/div[1]/div[1]/div[2]/button[1]')

    btn_newuser.click()

    # click existing user button
    btn_exist_acc = selenium.find_element(By.LINK_TEXT, 'У меня уже есть аккаунт')
    btn_exist_acc.click()

        # add email
    field_email = selenium.find_element(By.ID, 'email')
    field_email.clear()
    field_email.send_keys("yuras_91@bk.ru")
        # add password
    field_pass = selenium.find_element(By.ID, 'pass')
    field_pass.clear()
    field_pass.send_keys("qwerty")

    # click submit button
    btn_submit = selenium.find_element(By.XPATH, '//button[@type="submit"]')
    btn_submit.click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


driver.get('https://petfriends.skillfactory.ru/my_pets')
def test_pets_list():
    # Получаем список всех питомцев
    pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    # Убеждаемся, что присутствуют все питомцы
    assert len(pets) == int(driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split('\n')[1].split('Питомцев:')[1])

    images_count = 0
    list_names = []
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    for i in range(len(pets_count)):
        list_names.append(names[i].text)
        if images[i].get_attribute('src') != '':
            images_count += 1
        else:
            images_count += 0
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
        print(images_count)
    if len(pets_count) == 0:
        print("No pets")
    else:
        assert images_count / len(pets_count) >= 0.5

    # Проверяем, что у питомцев разные имена
    set_name = set(list_names)
    assert len(set_name) == len(list_names)



# def test_show_my_pets(selenium_driver):
#     '''Этот тест проверяет, что на сайте присутствуют все питомцы пользователя'''
#     driver = selenium_driver
#     # Проверяем, что мы оказались на главной странице пользователя
#     # ЯВНЫЕ ОЖИДАНИЯ
#     WDW(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a')))
#     driver.find_element(By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a').click()
#
#     # Находим количество (цифру) питомцев, отображенную на сайте
#     pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
#
#     # Находим таблицу со всеми моими питомцами
#     # НЕЯВНЫЕ ОЖИДАНИЯ
#     driver.implicitly_wait(10)
#     pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
#
#     assert int(pets_number) == len(pets_count)
#
#
# def test_photo_pets(selenium_driver):
#     '''Этот тест проверяет, что у более половины питомцев есть фотографии'''
#     driver = selenium_driver
#     # Проверяем, что мы оказались на главной странице пользователя
#     # ЯВНЫЕ ОЖИДАНИЯ
#     WDW(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a')))
#     driver.find_element(By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a').click()
#
#     # НЕЯВНЫЕ ОЖИДАНИЯ
#     driver.implicitly_wait(10)
#     pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
#     # Находим питомцев у которых есть фото
#     image_count = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image/")]')
#     # Проверяем что фотографии имеются более чем у половины питомцев
#     assert len(image_count) > len(pets_count) / 2


def test_allpet_have_name_breed_age(selenium_driver):
    '''Этот тест проверяет, что все питомцы содержат данные имя, возраст, породу,
    что нет дублирующих имен, а также, что нет питомцев с одинаковым именем, возрастом и породой'''
    driver = selenium_driver
    # Проверяем, что мы оказались на главной странице пользователя
    # ЯВНЫЕ ОЖИДАНИЯ
    WDW(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a')))
    driver.find_element(By.XPATH, '//[@id="navbarNav"]/ul/li[1]/a').click()

    # Находим таблицу со всеми питомцами
    allpet_count = driver.find_elements(By.XPATH,
                                        '//[@id="all_my_pets"]/table/tbody/tr/td[1] | //[@id="all_my_pets"]/table/tbody/tr/td[2] | //[@id="all_my_pets"]/table/tbody/tr/td[3]')

    pet_data = set()

    for i in range(1, len(allpet_count) // 3 + 1):

        name = driver.find_element(By.XPATH, f'//[@id="all_my_pets"]/table/tbody/tr[{i}]/td[1]').text

        breed = driver.find_element(By.XPATH, f'//[@id="all_my_pets"]/table/tbody/tr[{i}]/td[2]').text

        age = driver.find_element(By.XPATH, f'//[@id="all_my_pets"]/table/tbody/tr[{i}]/td[3]').text

        if name and breed and age:

            print(f'Pet {i}: Name: {name}, Breed: {breed}, Age: {age}')

        else:

            print(f'Pet {i} is missing information')

            # Проверяем, что нет пустых значений

        if name and breed and age:

            # Проверяем уникальность имени

            if name not in pet_data:

                pet_data.add(name)

            else:

                print(f"Ошибка: Повторяющееся имя - {name}")

            # Проверяем уникальность комбинации имени, породы и возраста

            pet_info = (name, breed, age)

            if pet_info not in pet_data:

                pet_data.add(pet_info)

            else:

                print(f"Ошибка: Не уникальная комбинация - {pet_info}")

        else:

            print("Ошибка: Не все данные заполнены")
