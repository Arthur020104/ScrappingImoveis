import os
import time
import urllib3
import shutil
from helper import deleteFilesInFolderAndFolder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.firefox.service import Service
import geckodriver_autoinstaller
import random
from infoExtract import extract_info, read_pdf

# Suppress warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize the global variable
global counter_download 
counter_download = 0  

# Ensure the temp directory exists
temp_dir = os.path.join(os.getcwd(), "temp")
os.makedirs(temp_dir, exist_ok=True)

def is_network_available():
    try:
        urllib3.PoolManager().request('GET', 'http://www.google.com', timeout=1)
        return True
    except:
        return False

def wait_for_file(file_paths, driver, timeout=30):
    start_time = time.time()
    while True:
        for file_path in file_paths:
            if os.path.exists(file_path):
                file_size = os.stat(file_path).st_size
                time.sleep(1)
                for _ in range(30):
                    time.sleep(4)  # Check file size every 4 seconds
                    new_size = os.stat(file_path).st_size
                    if new_size == file_size and new_size >= 164 * 1024:  # File size is at least 164 KB, download complete
                        time.sleep(5)
                        return True
                    file_size = new_size  # Update file size for next iteration
                return False

        if time.time() - start_time > timeout:
            return False  # Timeout reached

        try:
            error_message_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[2]/div/div'
            error_message = driver.find_element(By.XPATH, error_message_xpath).text
            if error_message:
                print(f"Error message: {error_message}")
                return False
        except NoSuchElementException:
            time.sleep(1)
            continue

def download_pdf(number):
    global counter_download
    counter_download += 1

    number_folder = os.path.join(temp_dir, number)
    os.makedirs(number_folder, exist_ok=True)

    if not is_network_available():
        print("Connection error occurred. Retrying in 60 seconds.")
        time.sleep(60)
        return download_pdf(number)

    try:
        service = Service(executable_path=geckodriver_autoinstaller.install(), log_path='geckodriver.log')
        options = webdriver.FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", number_folder)
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        options.set_preference("pdfjs.disabled", True)
        options.set_preference("permissions.default.stylesheet", 2)
        options.set_preference("permissions.default.image", 2)
        options.set_preference("webdriver.firefox.silentOutput", True)
        options.set_preference("security.insecure_field_warning.contextual.enabled", False)
        options.set_preference("security.insecure_password.ui.enabled", False)
        options.set_preference("security.insecure_password.logging.enabled", False)
        options.set_preference("security.insecure_form_warning.contextual.enabled", False)
        options.set_preference("security.insecure_connection_text.enabled", False)
        options.set_preference("security.insecure_connection_icon.enabled", False)
        options.set_preference("security.insecure_connection_icon.pbmode.enabled", False)
        options.headless = True
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # Disable the sandbox mode
        options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--disable-infobars")  # Disable info bars
        options.add_argument("--disable-extensions")  # Disable extensions
        options.add_argument("--disable-popup-blocking")  # Disable popup blocking
        options.add_argument("--disable-notifications")  # Disable notifications
        options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Firefox(service=service, options=options)
        time.sleep(random.uniform(1, 8))

        site = 'http://portalsiat.uberlandia.mg.gov.br/dsf_udi_portal/inicial.do?evento=montaMenu&acronym=CERT_NEG'
        driver.get(site)

        iframe_xpath = '/html/body/div[1]/div[4]/iframe'
        try:
            iframe = WebDriverWait(driver, 95).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
        except TimeoutException:
            driver.get(site)
            iframe = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))

        driver.switch_to.frame(iframe)
        content_input_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[4]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/input'
        imprimir_button_xpath = '/html/body/table/tbody/tr/td/div/span/ajax/span/ajax/form/span/ajax/div[3]/li[2]/span/input'
        content_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, content_input_xpath)))
        content_btn.send_keys(number)
        time.sleep(random.uniform(1, 8))
        imprimir_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, imprimir_button_xpath)))
        imprimir_btn.click()

        downloaded_files = [
            f'{number_folder}/CERTIDAO NEGATIVA DE DEBITOS IMOBILIARIO.pdf',
            f'{number_folder}/CERTIDAO POSITIVA DE DEBITOS IMOBILIARIO.pdf',
            f'{number_folder}/CERTIDAO POSITIVA COM EFEITO NEGATIVA IMOBILIARIO.pdf'
        ]

        if not wait_for_file(downloaded_files, driver, 100):
            print("Download failed.")
            if os.path.exists(number_folder):
                deleteFilesInFolderAndFolder(os.path.abspath(number_folder))
            return False

        for downloaded_file in downloaded_files:
            if os.path.isfile(downloaded_file):
                os.rename(downloaded_file, f"{number_folder}/{number}.pdf")
                time.sleep(4)
                break

        all_files = os.listdir(os.path.abspath(number_folder))
        for file_name in all_files:
            if file_name != f"{number}.pdf" and os.path.isfile(os.path.join(number_folder, file_name)):
                os.remove(os.path.join(number_folder, file_name))

        if len(os.listdir(os.path.abspath(number_folder))) > 1:
            if os.path.exists(number_folder):
                deleteFilesInFolderAndFolder(os.path.abspath(number_folder))
            return False

        return True
    except (urllib3.exceptions.NewConnectionError, WebDriverException, Exception) as e:
        print(f"An error occurred: {e}")
        if os.path.exists(number_folder):
            deleteFilesInFolderAndFolder(os.path.abspath(number_folder))
        return False
    finally:
        try:
            driver.quit()
        except WebDriverException as e:
            print(f"Error while quitting the driver: {e}")

def process_item(item):
    number = item["Insc_Cadastral"].replace(' ', '')
    response = download_pdf(number)
    if response:
        file_path = f"temp/{number}/{number}.pdf"
        if os.path.isfile(file_path):
            try:
                pages_content = read_pdf(file_path)
                if pages_content:
                    info = extract_info(pages_content[0][pages_content[0].find("IMÓVEL:"):])
                    info['Insc_Cadastral'] = item["Insc_Cadastral"]
                    return item, info
            except Exception as e:
                print(f"An error occurred while reading the PDF file: {e}")
    return None

if __name__ == "__main__":
    print(process_item({"Insc_Cadastral": "00 55 0505 55 55 0001 5999"}))
    print("Program finished.")
