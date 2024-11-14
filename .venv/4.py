import time
from fileinput import close
from operator import index
from pydoc import classname
from types import NoneType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.maximize_window()
URL = "https://tr.investing.com/currencies/usd-try-historical-data"
data_list = []

def close_popup(second):
    try:
        close_button = WebDriverWait(driver, second).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[data-test='sign-up-dialog-close-button']"))
        )
        close_button.click()
    except TimeoutException:
        pass


driver.get(URL)
close_popup(5)
scroll_amount = 10
pause_time = 0.05

thisDay = datetime.now()
thisDate = thisDay.strftime("%d.%m.%Y")
thisDate2 = thisDay.strftime("%Y-%m-%d")
print(thisDate)
for _ in range(75):
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(pause_time)

close_popup(5)
try:
    dateBox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '- {thisDate}')]"))
    )
    dateBox.click()
    close_popup(1)
    time.sleep(1)
    firstDateBox = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f'(//input[@type="date" and @max="{thisDate2}"])[1]'))
    )
    firstDateBox.click()
    close_popup(1)
    for i in range(700):
        firstDateBox.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Uygula']")))
    close_popup(1)
    apply_button.click()
    print("TARİH AYARLANDI.")
except:
    print("TARİH AYARLANAMADI.")

close_popup(5)
time.sleep(20)
usdData = driver.find_elements(By.CSS_SELECTOR,".datatable_cell__LJp3C")
for i in range(26, len(usdData), 1):
    if "%" not in usdData[i].text and "%" not in usdData[i+1].text:
        counter = (i - 26) // 3 +1
        close_popup(0)
        try:
            if counter % 200 == 0:
              print("VERİ MİKTARI :",counter)
            tarih = usdData[i].text
            fiyat= usdData[i + 1].text
            data_list.append({"Tarih": tarih, "Fiyat": fiyat})
        except (ValueError, IndexError) as e:
            print(f"Veri işlenemedi: {e}")
            continue
close_popup(5)
print("VERİLER HAZIRLANIYOR")
df = pd.DataFrame(data_list)
df.to_csv('usd_verileri.csv', index=False)
time.sleep(10)