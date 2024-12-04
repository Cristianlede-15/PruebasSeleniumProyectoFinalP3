import os
import shutil
import stat
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def is_window_open(driver):
    try:
        driver.current_window_handle
        return True
    except:
        return False

def take_full_page_screenshot(driver, file_path):
    if is_window_open(driver):
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        driver.save_screenshot(file_path)
        driver.set_window_size(original_size['width'], original_size['height'])
    else:
        print('La ventana del navegador está cerrada. No se puede tomar la captura de pantalla.')

def generate_html_report(events, output_file):
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Reporte de Buscar Productos Cliente</title></head><body>')
        f.write('<h1>Reporte de Buscar Productos Cliente</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(buscar_productos_cliente_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

buscar_productos_cliente_dir = os.path.join(screenshots_dir, 'BuscarProductosCliente')

if os.path.exists(buscar_productos_cliente_dir):
    shutil.rmtree(buscar_productos_cliente_dir, onerror=remove_readonly)

os.makedirs(buscar_productos_cliente_dir, exist_ok=True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

events = []
step_number = 1

try:
    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'identifier').send_keys('Man')
    driver.find_element(By.ID, 'password').send_keys('2233')
    events.append("Credentials entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    events.append("Login submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Home')))
    events.append("Home page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    tipos_comercios_link = driver.find_element(By.LINK_TEXT, 'Home')
    tipos_comercios_link.click()
    events.append("Tipos de Comercios page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.business-type')))
    events.append("Business types loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    primer_negocio = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.business-type a[href="/user/comercios/4"]'))
    )
    primer_negocio.click()
    events.append("First business clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-form')))
    events.append("Comercios page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    search_input = driver.find_element(By.NAME, 'nombre')
    search_input.clear()
    search_input.send_keys('parrilla')
    events.append("Search input filled with 'parrilla' successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    buscar_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]"))
    )
    buscar_button.click()
    events.append("Search button clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.business')))
    events.append("Search results for 'parrilla' loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    search_input = driver.find_element(By.NAME, 'nombre')
    search_input.clear()
    search_input.send_keys('pizza')
    events.append("Search input filled with 'pizza' successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    buscar_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]"))
    )
    buscar_button.click()
    events.append("Search button clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.business')))
    events.append("Search results for 'pizza' loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(buscar_productos_cliente_dir, 'report.html'))