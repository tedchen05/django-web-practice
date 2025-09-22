# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 00:14:51 2025

@author: ted
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import pytesseract
from PIL import Image
import base64
import time

# 等待元素出現後返回元素
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# 等待元素可點擊後返回元素
def wait_for_clickable(driver, by, value, timeout=10):

    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def init_driver(headless):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if not headless:
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.einvoice.nat.gov.tw/accounts/login/mw?login_challenge=d2247755b24643dabf7204e0aa3c752b")

    return driver

def get_captcha_text(driver):
    captcha_text = ""
    # 啟動瀏覽器（自動下載驅動）
    pytesseract.pytesseract.tesseract_cmd = r'webapp\utils\Tesseract-OCR\tesseract.exe'
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

    while len(captcha_text) != 6:
        # 取得驗證碼圖片
        captcha_img = wait_for_element(driver, By.CSS_SELECTOR, "span.input-group-text img", timeout=15)
        img_src = captcha_img.get_attribute("src")
        data = img_src.split(",")[1]

        # 儲存圖片
        with open("captcha.png", "wb") as f:
            f.write(base64.b64decode(data))

        # OCR 辨識
        img = Image.open("captcha.png")
        captcha_text = pytesseract.image_to_string(img, config=custom_config)

        # 如果失敗就點擊刷新按鈕
        if len(captcha_text) != 6:
            refresh_button = driver.find_element(By.XPATH, '//button[@title="更新圖形驗證碼"]')
            refresh_button.click()
            time.sleep(0.3) # 等待新圖片載入
    return captcha_text


def fill_login_form(driver, account, password, captcha_text):
    # 帳號欄位
    account_xpath = "/html/body/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div/form/div[1]/div/input"
    account_input = wait_for_element(driver, By.XPATH, account_xpath)
    account_input.clear()
    account_input.send_keys(account)

    # 密碼欄位
    password_input = driver.find_element(By.XPATH, "//input[@id='password']")
    password_input.click()
    password_input.clear()
    password_input.send_keys(password)

    # 驗證碼欄位
    captcha_input = driver.find_element(By.XPATH, "//input[@id='captcha']")
    captcha_input.click()
    captcha_input.clear()
    captcha_input.send_keys(captcha_text)

    time.sleep(0.3)

    if "使用者帳號或密碼錯誤" in driver.page_source:
        error_element = driver.find_element(By.XPATH, "//span[contains(text(),'使用者帳號或密碼錯誤')]")
        error_text = error_element.text
        print("使用者帳號或密碼錯誤！")
        return f"系統訊息：{error_text}"

    if "圖形驗證碼驗證失敗" in driver.page_source:
        print("驗證碼錯誤！")
        captcha_text = get_captcha_text(driver)
        fill_login_form(driver, account, password, captcha_text)

    if "返回首頁" in driver.page_source:
        element = driver.find_element("xpath", '//a[@title="返回首頁"]')
        element.click()
        time.sleep(1)
        login_button = driver.find_element("xpath", '//a[@title="登入"]')
        login_button.click()
        time.sleep(1)
        captcha_text = get_captcha_text(driver)
        fill_login_form(driver, account, password, captcha_text)
    return True

def select_invoice_date(driver, start_day, end_day):

    date_input = wait_for_clickable(driver, By.XPATH, "//input[@id='dp-input-searchInvoiceDate']")
    date_input.click()

    month = start_day.split("-")[1]
    month = str(int(month))

    # 點擊月份設定按鈕
    month_toggle = driver.find_element(By.XPATH, '//button[@aria-label="月份設定"]')
    month_toggle.click()

    # 接下來會跳出月份選單，你可以再選擇具體的月份（例如「12月」）
    december_btn = driver.find_element(By.XPATH, f'//div[text()="{month}月"]')
    december_btn.click()

    element = driver.find_element(By.XPATH, f'//*[@id="{start_day}"]')
    element.click()  # 可選，讓欄位聚焦
    element = driver.find_element(By.XPATH, f'//*[@id="{end_day}"]')
    element.click()  # 可選，讓欄位聚焦
    button = driver.find_element(By.CLASS_NAME, "button_style.blue_btn")
    button.click()
    return True

def rangetr(table):
    datas = []
    j = [0, 5, 6, 7, 8]
    i = 0
    data = []
    for t in range(len(table)):
        if i in j:
            i += 1
            continue
        elif i == 2:
            data.append(table[t].text.replace("手機條碼", ""))
        else:
            data.append(table[t].text)
        i += 1
        if i == 10:
            i = 0
            datas.append(data)
            data = []
    return datas


def crawl_pages(driver, all_data=None):
    if all_data is None:
        all_data = []

    table_element = wait_for_element(driver, By.CSS_SELECTOR, "table.table_style.have_checkbox.merge")
    chrome = driver.page_source
    soup = BeautifulSoup(chrome, 'html.parser')
    table = soup.find("table", class_="table table_style have_checkbox merge").find_all("td")
    page_data = rangetr(table)
    all_data.extend(page_data)

    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(5):
        body.send_keys(Keys.END)

    try:
        next_page = driver.find_element(By.XPATH, '//a[@title="下一頁"]')
        if next_page.get_attribute("disabled") is None:
            next_page.click()
            driver.implicitly_wait(2)  # 等待頁面載入
            return crawl_pages(driver, all_data)
        else:
            logout_button = driver.find_element(By.XPATH, '//a[@title="登出"]')
            logout_button.click()
            driver.quit()
            return all_data
    except Exception as e:
        print(f"⚠️ 發生錯誤：{e}")
        return all_data


def invoices_to_dict(invoice_data):
    columns = ["載具自訂名稱", "發票號碼", "發票金額", "發票日期", "出處"]
    df = pd.DataFrame(invoice_data, columns=columns)
    df.sort_index(ascending=False, inplace=True)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    account = input("請輸入帳號:")
    password = input("請輸入密碼:")

    driver = init_driver(True)
    captcha_text = get_captcha_text(driver)
    fill_login_form(driver, account, password, captcha_text)

    start_day = "2025-08-01"
    end_day = "2025-08-31"
    month = start_day.split("-")[1]

    select_invoice_date(driver, start_day, end_day)
    invoice_data = crawl_pages(driver)

    print(invoice_data)
    print("成功下載")

