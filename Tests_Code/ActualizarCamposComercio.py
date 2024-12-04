import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        f.write('<html><head><title>Reporte de Actualizar Campos Comercio</title></head><body>')
        f.write('<h1>Reporte de Actualizar Campos Comercio</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(actualizar_campos_comercio_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'
os.makedirs(screenshots_dir, exist_ok=True)

actualizar_campos_comercio_dir = os.path.join(screenshots_dir, 'ActualizarCamposComercio')
if os.path.exists(actualizar_campos_comercio_dir):
    shutil.rmtree(actualizar_campos_comercio_dir, onerror=remove_readonly)
os.makedirs(actualizar_campos_comercio_dir, exist_ok=True)

driver = webdriver.Chrome()

events = []
step_number = 1

try:
    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'identifier').send_keys('bipomoc548@cantozil.com')
    driver.find_element(By.ID, 'password').send_keys('2233')
    events.append("Credentials entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    events.append("Login submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Perfil')))
    events.append("Home page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    perfil_link = driver.find_element(By.LINK_TEXT, 'Perfil')
    perfil_link.click()
    events.append("Perfil page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'business_name')))

    nombre_input = driver.find_element(By.NAME, 'business_name')
    nombre_input.clear()
    nombre_input.send_keys('Pica Pollo la Cierva')
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    direccion_input = driver.find_element(By.NAME, 'address')
    direccion_input.clear()
    direccion_input.send_keys('Av. Anacaona, Santo Domingo')
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    assert nombre_input.get_attribute('value') != '', "El campo 'Nombre del Comercio' está vacío."
    assert direccion_input.get_attribute('value') != '', "El campo 'Dirección' está vacío."
    events.append("Form filled successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    actualizar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Guardar cambios']"))
    )
    actualizar_button.click()
    events.append("Form submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))
    events.append("Update successful.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(actualizar_campos_comercio_dir, 'report.html'))