from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import chromedriver_autoinstaller
import time
import random
import pandas as pd
from datetime import datetime
import os
from .info import guardar_info

def configure_chrome_options():
    """
    Configura as opções do Chrome para o WebDriver.

    Returns:
        Options: Objeto de opções configurado para o Chrome.
    """
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    return chrome_options

def log_error(error_type, property_code, index, error_message):
    """
    Registra erros em um arquivo CSV.

    Args:
        error_type (str): Tipo de erro ocorrido.
        property_code (str): Código da propriedade que causou o erro.
        index (int): Índice do código da propriedade.
        error_message (str): Mensagem de erro.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'error_type': [error_type],
        'property_code': [property_code],
        'index': [index],
        'error_message': [error_message],
        'date_time': [current_time]
    }
    df = pd.DataFrame(data)
    file_path = 'error_log.csv'

    if os.path.exists(file_path):
        try:
            existing_df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            existing_df = pd.DataFrame()
        new_df = pd.concat([existing_df, df], ignore_index=True)
        new_df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, index=False)

def get_info_by_complete_property_code(property_codes, max_errors=5, errors_before_restart=2):
    """
    Obtém informações detalhadas pelo código completo da propriedade.

    Args:
        property_codes (list): Lista de códigos de propriedade formatados.
        max_errors (int): Número máximo de erros permitidos antes de parar a execução.
        errors_before_restart (int): Número de erros antes de reiniciar o navegador.

    Returns:
        list: Lista com informações coletadas sobre as propriedades.
    """
    chromedriver_autoinstaller.install()
    chrome_options = configure_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)

    site_url = 'http://plataforma.uberlandia.mg.gov.br/plataforma/f/t/segundaviaiptusel?tipoDivida=dmae'
    time.sleep(random.randint(1, 5))
    driver.get(site_url)
    time.sleep(random.randint(1, 15))

    total_codes = len(property_codes)
    collected_info = []
    progress_bar = tqdm(range(total_codes), desc="Progress", unit="property_code")
    error_count = 0
    restart_error_count = 0

    for index in range(total_codes):
        try:
            progress_bar.set_postfix({"Progress": f"{index + 1}/{total_codes}"})
            try:
                input_field = WebDriverWait(driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/center/table[4]/tbody/tr[4]/td[3]/span/input'))
                )
            except (NoSuchElementException, TimeoutException) as e:
                log_error(type(e).__name__, property_codes[index], index, str(e))
                print(f"{'*' * 50} Error: Tentando denovo para {property_codes[index]} {'*' * 50}")
                driver.get(site_url)
                if restart_error_count >= errors_before_restart and restart_error_count < max_errors:
                    restart_error_count = 0
                    driver.quit()
                    time.sleep(1)
                    driver = webdriver.Chrome(options=chrome_options)
                    time.sleep(1)
                    driver.get(site_url)
                elif error_count >= max_errors:
                    restart_error_count += 1
                    error_count = 0
                    continue
                error_count += 1
                continue

            input_field.clear()
            input_field.send_keys(str(property_codes[index]))
            driver.find_element(By.XPATH, '/html/body/div[3]/form/div/div[2]/button[1]').click()

            try:
                info = guardar_info(driver, {}, [])
                collected_info.append(info)
                driver.find_element(By.XPATH, '/html/body/div[3]/form/div/div[2]/button[2]').click()
            except (NoSuchElementException, TimeoutException) as e:
                log_error(type(e).__name__, property_codes[index], index, str(e))
                #print(f"{'*' * 50} Error: Tentando denovo para {property_codes[index]} {'*' * 50}")
                driver.get(site_url)
                if restart_error_count >= errors_before_restart and restart_error_count <= max_errors:
                    restart_error_count = 0
                    driver.quit()
                    time.sleep(1)
                    driver = webdriver.Chrome(options=chrome_options)
                    time.sleep(1)
                    driver.get(site_url)
                elif error_count >= max_errors:
                    restart_error_count += 1
                    error_count = 0
                    continue
                error_count += 1
                continue

            error_count = 0
            progress_bar.update(1)
        except WebDriverException as e:
            if "net::ERR_CONNECTION_TIMED_OUT" in str(e):
                print("Erro de conexão. Tentando novamente em 60 segundos")
                time.sleep(60)
            else:
                continue

    progress_bar.close()
    driver.quit()
    return collected_info

if __name__ == '__main__':
    print(get_info_by_complete_property_code(['00040201160900230000', '00040201160900240000']))
    print('Finished')
