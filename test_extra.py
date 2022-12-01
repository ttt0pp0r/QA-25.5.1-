import pytest
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Users/skyew/PycharmProjects/pythonProject1/chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.maximize_window()
    pytest.driver.find_element(By.ID, 'email').send_keys('dainisvasiljev@gmail.com')
    pytest.driver.find_element(By.ID, 'pass').send_keys('Danissimo1990')
    pytest.driver.implicitly_wait(10)
    WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    WebDriverWait(pytest.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Мои питомцы')]"))).click()

    yield
    pytest.driver.quit()


def test_all_pets_present():
    pytest.driver.implicitly_wait(10)
    Nline = pytest.driver.find_elements(By.CSS_SELECTOR, 'tbody>tr')
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    assert NPets == len(Nline)


def test_half_pets_with_photo():
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(By.TAG_NAME, 'img')
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    No_images = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') == "":
            No_images += 1
    assert NPets / 2 >= No_images


def test_all_pets_have_name_ages_breed():
    pytest.driver.implicitly_wait(10)
    NPets = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')
    for i in range(len(names)):
        assert names[i].text != ""
        assert breed[i].text != ""
        assert ages[i].text != ""
    assert NPets == len(names) == len(breed) == len(ages)


def test_all_names_different():
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    list_of_names = []

    for i in range(len(names)):
        list_of_names.append(names[i].text)
    unigue_names = set(list_of_names)
    assert len(list_of_names) == len(unigue_names)


def test_no_repeating_pets():
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')
    list_names = []
    list_breed = []
    list_ages = []
    list_pets = []
    spisok = []

    for i in range(len(names)):
        list_names.append(names[i].text)
        list_breed.append(breed[i].text)
        list_ages.append(ages[i].text)
    for j in range(len(names)):
        list_pets.append(list_names[j])
        list_pets.append(list_breed[j])
        list_pets.append(list_ages[j])
        spisok.append(list_pets)
        list_pets = []

    for k in range(len(names)):
        n = k + 1
        while n < len(names):
            assert spisok[k] != spisok[n]
            n += 1