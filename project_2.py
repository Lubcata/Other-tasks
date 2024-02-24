import pandas as pd  # Импортиране на библиотеката pandas за работа с данни
import os  # Импортиране на модула os за взаимодействие с операционната система
import smtplib  # Импортиране на модула smtplib за изпращане на имейли
import ssl  # Импортиране на модула ssl за сигурни връзки

from email.message import EmailMessage  # Импортиране на класа EmailMessage за създаване на имейл съобщения
from selenium import webdriver  # Импортиране на селениум webdriver за уеб скрейпинг
from selenium.webdriver.common.by import By  # Импортиране на класа By за локализиране на елементи чрез различни стратегии
from selenium.webdriver.support.ui import WebDriverWait  # Импортиране на WebDriverWait за чакане на конкретни условия
from selenium.webdriver.support import expected_conditions as EC  # Импортиране на expected_conditions за дефиниране на очаквани условия
from selenium.common import NoSuchElementException  # Импортиране на класа NoSuchElementException за обработка на липсващи елементи
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# Дефиниране на функция за извличане на данни
def extract_data():
    offices_and_addresses = driver.find_elements(By.CLASS_NAME, "margin-16")  # Намиране на елементи със зададен клас
    for curr_office in offices_and_addresses:
        name = curr_office.find_element(By.XPATH, './p[1]').text  # Намиране и извличане на текст от първия параграф под текущия офис
        address = curr_office.find_element(By.XPATH, './p[2]').text  # Намиране и извличане на текст от втория параграф под текущия офис
        phone_number = curr_office.find_element(By.XPATH, './dl/dd/p').text  # Намиране и извличане на текст от определен параграф под текущия офис
        try:
            sat_hours = curr_office.find_element(By.XPATH, './div[1]/div/dl/dd/span/p[2]').text  # Опит за намиране и извличане на текст за работно време събота
        except NoSuchElementException:
            sat_hours = ""  # Ако NoSuchElementException се появи, задаване на работно време събота на празен стринг
        try:
            sun_hours = curr_office.find_element(By.XPATH, './div[1]/div/dl/dd/span/p[3]').text  # Опит за намиране и извличане на текст за работно време неделя
        except NoSuchElementException:
            sun_hours = ""  # Ако NoSuchElementException се появи, задаване на работно време неделя на празен стринг

        # Добавяне на извлечените данни към съответните списъци
        office_name.append(name)
        office_addresses.append(address)
        phone_numbers.append(phone_number)
        saturday.append(sat_hours)
        sunday.append(sun_hours)


# Дефиниране на функция за експорт на данни в Excel файл
def export():
    df = pd.DataFrame({
        "Име на офиса": office_name,
        "Адрес": office_addresses,
        "Телефон": phone_numbers,
        "Раб.време събота": saturday,
        "Раб.време неделя": sunday
    })
    df.to_excel('C:\\PythonApp\\fibank_branches.xlsx', index=False)  # Експорт на DataFrame в Excel файл


# Дефиниране на функция за изпращане на имейл с прикачените данни
def send_email():
    email_sender = "lflorov2@gmail.com"
    email_password = "fcuo esuy qbeq vaqe"
    email_receiver = "lflorov7@icloud.com"

    host = "smtp.gmail.com"
    port = 465

    subject = "Информация за офисите на Fibank"
    body = """
Здравейте,
Прикачен е файл с информация за офисите на Fibank.
Поздрави!
    """

    # Задаване на име и път за файла
    file_name = "fibank_branches.xlsx"
    file_path = os.path.join("C:", "PythonApp", file_name)

    em = EmailMessage()  # Създаване на обект от класа EmailMessage
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)  # Задаване на съдържанието на имейла

    # Прикачване на Excel файла към имейла
    with open(file_path, "rb") as attachment:
        em.add_attachment(attachment.read(), maintype='application', subtype='octet-stream', filename=file_name)

    context = ssl.create_default_context()

    # Свързване с SMTP сървъра, логин и изпращане на имейла
    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


# Задаване на URL адреса на уебсайта
website = "https://my.fibank.bg/EBank/public/offices"
driver = webdriver.Chrome() # Създаване на инстанция на Chrome WebDriver
driver.get(website)  # Отваряне на уебсайта в браузъра

# Инициализиране на празни списъци за съхранение на извлечените данни
office_name = []
office_addresses = []
phone_numbers = []
saturday = []
sunday = []

# Създаване на инстанция на WebDriverWait за чакане на конкретни условия
wait = WebDriverWait(driver, 10)

# Изчакване за кликване на бутона преди да бъде кликнат
button_xpath = '//*[@id="content-col"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/button'
wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()

# Изчакване за кликване на връзката преди да бъде кликната
link_xpath = ('//*[@id="content-col"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div/ul/li['
              '3]/a/span[1]')
wait.until(EC.element_to_be_clickable((By.XPATH, link_xpath))).click()

# Извличане на данни с помощта на оптимизираната функция
extract_data()

# Затваряне на браузъра
driver.quit()

# Експорт и изпращане на имейл
export()
send_email()
