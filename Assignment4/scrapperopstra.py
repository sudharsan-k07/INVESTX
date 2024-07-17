import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def setup_driver(download_dir):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = webdriver.Chrome(options=options)
    return driver

def login_to_opstra(driver, username, password):
    driver.get('https://opstra.definedge.com')
    time.sleep(5)
    searchelement = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/nav/div/div[4]/button/div')
    searchelement.click()
    searchelement1 = driver.find_element(By.XPATH, '//*[@id="username"]')
    searchelement1.send_keys(username)
    searchelement2 = driver.find_element(By.XPATH, '//*[@id="password"]')
    searchelement2.send_keys(password)
    searchelement3 = driver.find_element(By.XPATH, '//*[@id="kc-login"]')
    searchelement3.click()

def scrape_option_data(driver, output_file):
    driver.get('https://opstra.definedge.com/strategy-builder')
    time.sleep(5)
    searchelement4 = driver.find_element(By.XPATH, '//*[@id="app"]/div[62]/main/div/div/div/div/div[3]/div[2]/div[3]/ul/li/div[1]/div[1]')
    time.sleep(5)
    searchelement4.click()

    optiondata = []
    for j in range(1, 11):
        add = '//*[@id="app"]/div[62]/main/div/div/div/div/div[3]/div[2]/div[3]/ul/li/div[2]/div[1]/div[' + str(j) + ']/button/div'
        searchelement5 = driver.find_element(By.XPATH, add)
        searchelement5.click()

        CallLTP = driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        itmprob = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        CallIv = driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
        CallDelta = driver.find_elements(By.XPATH, '//tbody/tr/td[4]')
        StrikePrice = driver.find_elements(By.XPATH, '//tbody/tr/td[5]')
        PutDelta = driver.find_elements(By.XPATH, '//tbody/tr/td[6]')
        PutIV = driver.find_elements(By.XPATH, '//tbody/tr/td[7]')
        ITMProb = driver.find_elements(By.XPATH, '//tbody/tr/td[8]')
        PutLTP = driver.find_elements(By.XPATH, '//tbody/tr/td[9]')

        for i in range(len(CallLTP)):
            tempdata = {
                'CallLTP': CallLTP[i].text,
                'itmprob': itmprob[i].text,
                'CallIv': CallIv[i].text,
                'CallDelta': CallDelta[i].text,
                'StrikePrice': StrikePrice[i].text,
                'PutDelta': PutDelta[i].text,
                'PutIV': PutIV[i].text,
                'ITMProb': ITMProb[i].text,
                'PutLTP': PutLTP[i].text
            }
            optiondata.append(tempdata)

        df = pd.DataFrame(optiondata)
        df.to_csv(output_file, index=False)

if __name__ == "__main__":
    output_dir = r"C:\Users\RohanRam\Desktop\opstrascrapping"
    username = "#email goes here"
    password = "#password goes here"

    driver = setup_driver(output_dir)
    login_to_opstra(driver, username, password)
    scrape_option_data(driver, output_file)
    driver.quit()
