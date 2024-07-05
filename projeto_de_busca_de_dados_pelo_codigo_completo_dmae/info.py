import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def guardar_info(driver, all_info, list_dict):
   # cpf_site = driver.find_element("xpath",'/html/body/div[3]/form/div/table[3]/tbody/tr[1]/td[2]/span[2]')
    cpf_certo = WebDriverWait(driver, 35).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[1]/td[2]/span[2]'))
    ).text

    nome_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[1]/td[1]/span[2]'))
    )
    nome_certo = nome_site.text

    endereco_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[2]/td[1]/span[2]'))
    )
    endereco_certo = endereco_site.text

    bairro_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[2]/td[2]/span[2]'))
    )
    bairro_certo = bairro_site.text

    cep_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[2]/td[3]/span[2]'))
    )
    cep_certo = cep_site.text

    cod_prefeitura_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[3]/tbody/tr[1]/td[3]/span[2]'))
    )
    cod_prefeitura_certo = cod_prefeitura_site.text

    # Parte do imóvel
    inscricao_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[5]/tbody/tr[1]/td[1]/span[2]'))
    )
    inscricao_certo = inscricao_site.text

    quadra_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[5]/tbody/tr[1]/td[2]/span[2]'))
    )
    quadra_certo = quadra_site.text

    lote_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[5]/tbody/tr[1]/td[3]/span[2]'))
    )
    lote_certo = lote_site.text

    reduzido_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[5]/tbody/tr[1]/td[4]/span[2]'))
    )
    reduzido_certo = reduzido_site.text

    endereco_imovel_site = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div/table[5]/tbody/tr[2]/td[1]/span[2]'))
    )
    endereco_imovel_certo = endereco_imovel_site.text

    bairro_imovel_site = driver.find_element("xpath",'/html/body/div[3]/form/div/table[5]/tbody/tr[2]/td[2]/span[2]')
    bairro_imovel_certo = bairro_imovel_site.text

    all_info = {
        'Cod_Reduzido': reduzido_certo,
        'Insc_Cadastral': inscricao_certo,
        'Imovel_Endereco': endereco_imovel_certo,
        'Bairro': bairro_imovel_certo,
        'Quadra': quadra_certo,
        'Lote': lote_certo,
        'Area Territorial': 0, 
        'Area Predial': 0, 
        'Testada': 0,
        'Cod_Prefeitura': cod_prefeitura_certo,
        'Contribuinte_CPF': cpf_certo,
        'Contribuinte_Nome': nome_certo,
        'Contribuinte_Endereco': endereco_certo,
        'Contribuinte_CEP': cep_certo,
        'Bairro_Contribuinte': bairro_certo,
        }
    return all_info
    