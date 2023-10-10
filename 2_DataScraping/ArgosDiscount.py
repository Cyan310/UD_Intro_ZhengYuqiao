import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

url="https://www.argos.co.uk/"

def extract_item_data(driver):
    
    items=driver.find_elements("xpath", "//div[div/@data-test='component-product-card']")

    for b in range(len(items)):
        try:          
            itemName = items[b].find_element(By.CSS_SELECTOR, 'div[data-test="component-product-card-title"]').text       
            price = items[b].find_element(By.CSS_SELECTOR, 'div[data-test="component-product-card-price"]').text
            link = items[b].find_element(By.CSS_SELECTOR, 'div[data-test="component-product-card"]').find_element(By.TAG_NAME, 'a').get_attribute('href')
                  
            items_list.append(itemName)
            price_list.append(price)
            link_list.append(link)

            sleep(0.5)  
        
        except:
            pass
                       
            
        try:

            discount= items[b].find_element(By.CSS_SELECTOR, 'div[data-test="special-offer"]').text
            
            discount_list.append(discount)

        except:
            discount_list.append("NONE")
            continue

driver = webdriver.Chrome()
driver.get(url)

items_list = []
price_list=[]
discount_list=[]
link_list=[]

search_query = driver.find_element("name","searchTerm")
sleep(1)

search_query.send_keys('Marshall')
search_query.send_keys(Keys.RETURN)

sleep(1)

for page_num in range(0,3):
    try:

        extract_item_data(driver)
        
        next_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-test="component-pagination-arrow-right"]')))
        next_button.click()
    
    except Exception as e:
        print(f"An error occurred on page {page_num + 1}: {str(e)}")
        pass


driver.quit()
print("Data acquisition completed")

import csv 

data=zip(items_list,price_list,discount_list,link_list)

with open('ArgosDiscount.csv', 'w', encoding='gbk', errors='ignore', newline='') as csvfile: 
    writer = csv.writer(csvfile) 
    for row in data:
        writer.writerow(row)


