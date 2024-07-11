from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Edge()


driver.get('https://iftp.chinamoney.com.cn/english/bdInfo/')


sleep(5)


try:

    bond_type_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'Bond_Type_select'))
    )
    bond_type_select = Select(bond_type_select_element)
    bond_type_select.select_by_visible_text('Treasury Bond')
except Exception as e:
    print(f"无法找到 Bond Type 下拉框: {e}")
    driver.quit()

try:

    coupon_type_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'Coupon_Type_select'))
    )
    coupon_type_select = Select(coupon_type_select_element)
    coupon_type_select.select_by_visible_text('All')
except Exception as e:
    print(f"无法找到 Coupon Type 下拉框: {e}")
    driver.quit()


try:

    issue_year_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'Issue_Year_select'))
    )
    issue_year_select = Select(issue_year_select_element)
    issue_year_select.select_by_visible_text('2023')
except Exception as e:
    print(f"无法找到 Issue Year 下拉框: {e}")
    driver.quit()


try:

    rating_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'Rating_select'))
    )
    rating_select = Select(rating_select_element)
    rating_select.select_by_visible_text('All')
except Exception as e:
    print(f"无法找到 Rating 下拉框: {e}")
    driver.quit()

try:
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@onclick="searchData()"]'))
    )
    driver.execute_script("arguments[0].click();", search_button)
except Exception as e:
    print(f"无法找到搜索按钮: {e}")
    driver.quit()

sleep(5)


html = driver.page_source


driver.quit()


soup = BeautifulSoup(html, 'html.parser')


table = soup.find('table')

if table:

    headers = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']


    data = []
    table_rows = table.find_all('tr')

    for row in table_rows:
        columns = row.find_all('td')
        row_data = [col.get_text(strip=True) for col in columns]
        if row_data:
            data.append(row_data)


    df = pd.DataFrame(data, columns=headers)


    df.to_csv('bond_data.csv', index=False)
else:
    print("无法找到表格")
