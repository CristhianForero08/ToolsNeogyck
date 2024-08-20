from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import requests

# Lista de proxies
PROXIES = [
    'http://114.129.2.82:8081',
    'http://58.246.58.150:9002',
    'socks4://184.170.249.65:4145',
    'http://119.9.77.49:443',
    'http://125.77.25.177:8080',
    'http://220.248.70.237:9002',
    'http://58.20.248.139:9002',
    'http://103.153.154.6:80',
    'http://137.66.36.81:80',
    'http://185.217.143.96:80',
    'http://67.43.227.226:6923',
    'http://190.103.177.131:80',
    'http://72.10.164.178:14349',
    'http://116.63.129.202:6000',
    'socks4://184.178.172.25:15291',
    'socks4://67.43.236.18:26015',
    'socks4://38.152.31.61:8800'
]

# Configura el servicio de 2Captcha
API_KEY = 'f6fd5649947953f045354b872ba1ef03'
CAPTCHA_API_URL = 'http://2captcha.com/in.php'
CAPTCHA_RESULT_URL = 'http://2captcha.com/res.php'

def get_random_proxy():
    return random.choice(PROXIES)

def solve_captcha(captcha_site_key, page_url):
    response = requests.post(CAPTCHA_API_URL, data={
        'key': API_KEY,
        'method': 'userrecaptcha',
        'googlekey': captcha_site_key,
        'pageurl': page_url,
        'json': 1
    })
    
    result = response.json()
    if result['status'] != 1:
        if result['request'] == 'ERROR_KEY_DOES_NOT_EXIST':
            raise Exception('Error: La clave del sitio proporcionada no existe en 2Captcha.')
        else:
            raise Exception('Error al resolver captcha: {}'.format(result['request']))
    
    captcha_id = result['request']
    
    while True:
        time.sleep(5)
        response = requests.get(CAPTCHA_RESULT_URL, params={
            'key': API_KEY,
            'action': 'get',
            'id': captcha_id,
            'json': 1
        })
        result = response.json()
        if result['status'] == 1:
            return result['request']
        elif result['status'] == 0 and result['request'] == 'CAPCHA_NOT_READY':
            continue
        else:
            raise Exception('Error al obtener el resultado del captcha: {}'.format(result['request']))

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comentamos esta línea para que el navegador sea visible

    service = Service('C:/Users/crist/OneDrive/Escritorio/Neogyck-Tools/NeogyckSeo/home/drive/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def search_google(keyword, country='co', language='es'):
    driver = setup_driver()
    driver.get(f"https://www.google.com/search?q={keyword}&hl={language}&gl={country}")
    
    time.sleep(random.uniform(2, 5))  # Introduce tiempo de espera aleatorio
    
    try:
        # Verificar si hay un captcha en la página
        captcha_iframe = driver.find_elements(By.CSS_SELECTOR, 'iframe[src*="api2/anchor"]')
        if captcha_iframe:
            print("Captcha detectado. Por favor, resuélvelo manualmente.")
            input("Presiona Enter una vez que hayas resuelto el captcha y la página haya cargado...")

            # Esperar hasta que los resultados estén cargados
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3'))
            )

        # Obtener URLs de los resultados
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3'))
        )
        urls = [result.find_element(By.XPATH, '..').get_attribute('href') for result in results[:20]]
    
    except TimeoutException:
        print("TimeoutException: No se encontraron resultados en el tiempo esperado.")
        urls = []
    finally:
        driver.quit()
    
    return urls
