import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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
        f.write('<html><head><title>Reporte de Gestion Productos Comercios Test</title></head><body>')
        f.write('<h1>Reporte de Gestion Productos Comercios Test</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(gestion_productos_comercios_dir, f'Captura{step_number}.png')

gestion_productos_comercios_dir = os.path.join(
    r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots',
    'GestionProductosComerciosTest'
)

if os.path.exists(gestion_productos_comercios_dir):
    shutil.rmtree(gestion_productos_comercios_dir, onerror=remove_readonly)

os.makedirs(gestion_productos_comercios_dir, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.maximize_window()

events = []
step_number = 1

try:
    wait = WebDriverWait(driver, 10)

    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'identifier')))
    email_field.send_keys('laparrillagourmet@gmail.com')
    events.append("Email entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('2233')
    events.append("Password entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()
    events.append("Login submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    productos_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Mantenimiento de productos')))
    productos_link.click()
    events.append("Navigated to Mantenimiento de productos successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_full_page_screenshot(driver, os.path.join(gestion_productos_comercios_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(gestion_productos_comercios_dir, 'report.html'))