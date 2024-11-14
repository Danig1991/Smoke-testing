import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# базовый url
base_url = "https://www.saucedemo.com/"

# добавить опции/оставить браузер открытым
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# автоматическая загрузка драйвера
service = ChromeService(ChromeDriverManager().install())

# открытие браузера с параметрами
driver_chrome = webdriver.Chrome(
    options=options,
    service=service
)

# переход по url в браузере/развернуть на весь экран
driver_chrome.get(base_url)
driver_chrome.maximize_window()

# ввод логина/пароля, нажатие на кнопку Login
driver_chrome.find_element(
    By.ID, "user-name"
).send_keys("standard_user")

driver_chrome.find_element(
    By.ID, "password"
).send_keys("secret_sauce")

# пауза 1 секунда
time.sleep(1)

driver_chrome.find_element(
    By.ID, "login-button"
).click()
print("Успешная авторизация.")

# получить 1 продукт, его название, цену и добавить в корзину
product_1 = driver_chrome.find_element(
    By.XPATH, "//a[@id='item_4_title_link']"
)
value_product_1 = product_1.text

price_product_1 = driver_chrome.find_element(
    By.XPATH, "//*[@id='inventory_container']/div/div[1]/div[2]/div[2]/div"
)
value_price_product_1 = price_product_1.text

driver_chrome.find_element(
    By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']"
).click()
print(f"1 продукт добавлен в корзину\n"
      f"Название - \"{value_product_1}\"\n"
      f"Цена: {value_price_product_1}")

# пауза 1 секунда
time.sleep(1)

# получить 2 продукт, его название, цену и добавить в корзину
product_2 = driver_chrome.find_element(
    By.XPATH, "//a[@id='item_0_title_link']"
)
value_product_2 = product_2.text

price_product_2 = driver_chrome.find_element(
    By.XPATH, "//*[@id='inventory_container']/div/div[2]/div[2]/div[2]/div"
)
value_price_product_2 = price_product_2.text

driver_chrome.find_element(
    By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']"
).click()
print(f"2 продукт добавлен в корзину\n"
      f"Название - \"{value_product_2}\"\n"
      f"Цена: {value_price_product_2}")

# пауза 1 секунда
time.sleep(1)

# перейти в корзину
driver_chrome.find_element(
    By.ID, "shopping_cart_container"
).click()
print("Переход в корзину.")

# пауза 1 секунда
time.sleep(1)

# нажать на кнопку Checkout
driver_chrome.find_element(
    By.ID, "checkout"
).click()
print("Нажатие на кнопку Checkout.")

# заполнить личную информацию и нажать кнопку Continue
driver_chrome.find_element(
    By.ID, "first-name"
).send_keys("Ivan")

driver_chrome.find_element(
    By.ID, "last-name"
).send_keys("Ivanov")

driver_chrome.find_element(
    By.ID, "postal-code"
).send_keys("333-333")

# пауза 1 секунда
time.sleep(1)

driver_chrome.find_element(
    By.ID, "continue"
).click()
print("Личная информация добавлена.\nНажата кнопка Continue.")

# проверка соответствия начального и финального названия/цены 1 продукта
finish_product_1 = driver_chrome.find_element(
    By.ID, "item_4_title_link"
)
value_finish_product_1 = finish_product_1.text
assert value_product_1 == value_finish_product_1, \
    ("Ошибка: Начальное название 1 продукта должно"
     " совпадать с финальным его названием.")
print(f"Название продукта 1 - {value_finish_product_1} - совпадает.")

finish_price_product_1 = driver_chrome.find_element(
    By.XPATH,
    "//*[@id='checkout_summary_container']/div/div[1]/div[3]/div[2]/div[2]/div"
)
value_finish_price_product_1 = finish_price_product_1.text
assert value_price_product_1 == value_finish_price_product_1, \
    ("Ошибка: Начальная цена 1 продукта должна"
     " совпадать с финальной её ценой.")
print(f"Цена продукта 1 - {value_finish_price_product_1} - совпадает.")

# проверка соответствия начального и финального названия/цены 2 продукта
finish_product_2 = driver_chrome.find_element(
    By.ID, "item_0_title_link"
)
value_finish_product_2 = finish_product_2.text
assert value_product_2 == value_finish_product_2, \
    ("Ошибка: Начальное название 2 продукта должно"
     " совпадать с финальным его названием.")
print(f"Название продукта 2 - {value_finish_product_2} - совпадает.")

finish_price_product_2 = driver_chrome.find_element(
    By.XPATH,
    "//*[@id='checkout_summary_container']/div/div[1]/div[4]/div[2]/div[2]/div"
)
value_finish_price_product_2 = finish_price_product_2.text
assert value_price_product_2 == value_finish_price_product_2, \
    ("Ошибка: Начальная цена 2 продукта должна"
     " совпадать с финальной её ценой.")
print(f"Цена продукта 2 - {value_finish_price_product_2} - совпадает.")

# проверка правильности подсчета конечной суммы
finish_price_all_product = driver_chrome.find_element(
    By.XPATH, "//*[@id='checkout_summary_container']/div/div[2]/div[6]"
)
value_finish_price_all_product = float(finish_price_all_product.text[13:])

sum_price_all_product = (
        float(value_price_product_1[1:]) +
        float(value_price_product_2[1:])
)

assert sum_price_all_product == value_finish_price_all_product, \
    "Ошибка: Конечная сумма должна совпадать с суммой выбранных продуктов."
print(f"Конечная сумма - {value_finish_price_all_product} - совпадает.")

# пауза 1 секунда
time.sleep(1)

# нажатие на кнопку Finish
driver_chrome.find_element(
    By.ID, "finish"
).click()
print("Нажатие на кнопку Finish.")

# пауза 1 секунда
time.sleep(1)

# проверка успешности оформления
checkout_complete = driver_chrome.find_element(
    By.XPATH, "//*[contains(text(), 'Thank you for your order!')]"
)
value_checkout_complete = checkout_complete.text
assert value_checkout_complete == "Thank you for your order!", \
    "Ошибка: Должен присутствовать текст - 'Thank you for your order!'"
print("Успешное оформление.")

# пауза 1 секунда
time.sleep(1)

# нажать кнопку Back Home
driver_chrome.find_element(
    By.ID, "back-to-products"
).click()
print("Нажатие кнопки Back Home.")

# пауза 2,5 секунды
time.sleep(2.5)

# закрыть окно браузера
driver_chrome.close()
print("Закрытие окна.")
