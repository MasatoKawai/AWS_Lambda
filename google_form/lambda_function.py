import json
from selenium import webdriver
import time
import random
from datetime import datetime, timedelta, timezone

def lambda_handler(event, context):
    # タイムゾーンの生成
    JST = timezone(timedelta(hours=+9), 'JST')
    print(datetime.now(JST))
    url = 'https://docs.google.com/forms/d/e/************************************/viewform'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=880x996")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")
    options.binary_location = "/opt/headless/python/bin/headless-chromium"

    #ブラウザの定義
    driver = webdriver.Chrome(
        executable_path = "/opt/headless/python/bin/chromedriver",
        options=options
    )
    driver.implicitly_wait(1)
    driver.get(url)
    driver.implicitly_wait(1)

    
    def click(xpath):
        driver.find_element_by_xpath(xpath).click()
    
    def send_text_throw_xpath(num, xpath):
        driver.find_element_by_xpath(xpath).send_keys(num)
        

    date_xpath_1 = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div[1]/input'
    date_xpath_2 = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[1]/input'
    morning_button = '//*[@id="i9"]/div[3]/div'
    night_button = '//*[@id="i12"]/div[3]/div'
    temperture_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    weight_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input'
    feeling_xpath = '//*[@id="i27"]/div[3]/div'  
    submit_button = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span'

    
    # 日付入力
    month = datetime.now(JST).month
    send_text_throw_xpath(month, date_xpath_1)
    day = datetime.now(JST).day
    send_text_throw_xpath(day, date_xpath_2)
    
    # 朝か夜のボタン押下
    if datetime.now(JST).hour < 12:
        click(morning_button)
    else:
        click(night_button)
    
    # 体温入力
    body_temp = 36.0 + random.randint(1,7)/10
    send_text_throw_xpath(str(body_temp), temperture_xpath)

    # 体重入力
    weight = 96.0 + random.randint(-5,5)/10
    send_text_throw_xpath(str(weight), weight_xpath)
    
    # 体調入力
    click(feeling_xpath)
    
    click(submit_button)
    driver.close
    driver.quit
    return {
        'statusCode': 200,
        'body': json.dumps('Form submission success!!')
    }

