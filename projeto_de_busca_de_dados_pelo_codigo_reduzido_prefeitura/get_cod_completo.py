from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Disable loading of images
chrome_options.add_argument("--disable-images")

# Disable loading of CSS
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
def get_property_number_and_adress(numbers):
    alldata = []
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add chromedriver to path

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    site = 'http://portalsiat.uberlandia.mg.gov.br/dsf_udi_portal/inicial.do?evento=montaMenu&acronym=EXTRATO#'
    try:
        driver.get(site)
        iframe_xpath = '/html/body/div[1]/div[4]/iframe'
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, iframe_xpath))
            )
        except:
            driver.get(site)
            try:
                iframe = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, iframe_xpath))
                )
            except:
                driver.quit()
                driver.get(site)
                iframe = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, iframe_xpath))
                )
        driver.switch_to.frame(iframe)
        #setting paths
        
        string_start = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div['
        string_start_len = len(string_start)
        dropdown_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[4]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[1]/select'
        #error_dropdown_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[5]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[1]/select'
        input_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[4]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/input'
       # error_input_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[5]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/input'
        search_button_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[3]/li[2]/span/input'
        #error_search_button_xpath ='/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[4]/li[2]/span/input'
        property_data_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[4]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td[2]/input'
       # error_property_data_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[5]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td[2]/input'
        table_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[10]/div/div/table'
        #error_table_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[11]/div/div/table'
        def default_paths(search_button_xpath,input_xpath,dropdown_xpath):
            search_button_xpath = list(search_button_xpath)
            input_xpath = list(input_xpath)
            #property_data_xpath = list(property_data_xpath)
            #table_xpath = list(table_xpath)
            dropdown_xpath = list(dropdown_xpath)

            search_button_xpath[string_start_len] = '3'
            #print(search_button_xpath)
            input_xpath[string_start_len] = '4'
            #property_data_xpath[string_start_len] = '4'
            #table_xpath[string_start_len+1] = '0'
            dropdown_xpath[string_start_len] = '4'

            search_button_xpath = ''.join(search_button_xpath)
            input_xpath = ''.join(input_xpath)
            #property_data_xpath = ''.join(property_data_xpath)
           #table_xpath = ''.join(table_xpath)
            dropdown_xpath = ''.join(dropdown_xpath)
            #print(search_button_xpath)
            return search_button_xpath,input_xpath,dropdown_xpath
        def error_paths(search_button_xpath,input_xpath,dropdown_xpath):
            search_button_xpath = list(search_button_xpath)
            input_xpath = list(input_xpath)
            #property_data_xpath = list(property_data_xpath)
            #table_xpath = list(table_xpath)
            dropdown_xpath = list(dropdown_xpath)

            search_button_xpath[string_start_len] = '4'
            input_xpath[string_start_len] = '5'
            #property_data_xpath[string_start_len] = '5'
            #table_xpath[string_start_len+1] = '1'
            dropdown_xpath[string_start_len] = '5'

            search_button_xpath = ''.join(search_button_xpath)
            input_xpath = ''.join(input_xpath)
           # property_data_xpath = ''.join(property_data_xpath)
           # table_xpath = ''.join(table_xpath)
            dropdown_xpath = ''.join(dropdown_xpath)
            return search_button_xpath,input_xpath,dropdown_xpath
                
        
        for number in numbers:
            
            try:
                # Now, you should be inside the iframe, locate the dropdown
              #  driver.switch_to.default_content()
               # driver.switch_to.frame(iframe)
               # time.sleep(1)
                dropdown_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, dropdown_xpath))
                )

                # Change the value of the dropdown to reduced property code
                drop = Select(dropdown_element)
                drop.select_by_value("IR")

                #filling the input with the property code
                
                input_element = driver.find_element(By.XPATH, input_xpath)
                input_element.clear()
                input_element.send_keys(number)
                
                #clicking the search button
                
                search_button = driver.find_element(By.XPATH, search_button_xpath)
                search_button.click()
                #time.sleep(1)
                #iframe = '/html/body/div[1]/div[4]/iframe'
                #
                #getting the property adress
                
                #try:
                    
                property_data = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, property_data_xpath))
                )
                adress = property_data.get_attribute("value")
                
                # Wait for the table to load
                table = WebDriverWait(driver, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, table_xpath))
                )
                
                # Wait for the rows to be visible
                rows = WebDriverWait(table, 0.2).until(
                    EC.visibility_of_all_elements_located((By.TAG_NAME, "tr"))
                )
                first_row = rows[1]
            
                # Get the "cadastro" column
                cadastro_column = first_row.find_elements(By.TAG_NAME, "td")
                codigo_str = cadastro_column[1].text
                codigo_formatado = codigo_str[5:len(codigo_str)].replace(".", "")

                ##print(cadastro_text)
                
                # Exit the iframe to interact with elements outside the iframe
                #driver.switch_to.default_content()
                search_button_xpath, input_xpath, dropdown_xpath = default_paths(search_button_xpath, input_xpath, dropdown_xpath)
                
                #print(f"\n\n\n\n\n\nAdress: {adress} ->{number}\n\n\n\n\n\n")
                
                data = {"codigo": codigo_formatado, "endereco": adress,"codigo_completo": codigo_str, "codigo_reduzido": number}
                alldata.append(data)
            except NoSuchElementException as e:
                #print(f"\n\n\n\n\nNOsuchelementexception {100 * '*'} {e} {100 * '*'}\n\n\n\n\n")
                #print(f"Property with number {number} not found. Skipping...")
                #path to elements change when the property is not found
                search_button_xpath, input_xpath, dropdown_xpath = error_paths(search_button_xpath, input_xpath, dropdown_xpath)
                driver.get(site)
                iframe = WebDriverWait(driver, 0.3).until(
                    EC.presence_of_element_located((By.XPATH, iframe_xpath))
                )
                driver.switch_to.frame(iframe)
                #time.sleep(50)
                continue
            except TimeoutException as e:
                #print(f"{100*'*'} TimeoutException ")
                #print(f"Property with number {number} not found. Skipping...")
                #path to elements change when the property is not found
                search_button_xpath, input_xpath, dropdown_xpath = error_paths(search_button_xpath, input_xpath, dropdown_xpath)
                
                driver.get(site)
                iframe = WebDriverWait(driver, 0.3).until(
                    EC.presence_of_element_located((By.XPATH, iframe_xpath))
                )
                driver.switch_to.frame(iframe)
                #time.sleep(50)
                continue
        
    finally:
        
        driver.quit() 
    return alldata
        # Close the browser
if __name__ == "__main__":
    print(get_property_number_and_adress([125069,125070,125071,125069,125085]))
    print("Fim do programa.")