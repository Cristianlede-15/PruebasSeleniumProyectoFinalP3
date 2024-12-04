import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
        f.write('<html><head><title>Reporte de Activar/Desactivar Comercios</title></head><body>')
        f.write('<h1>Reporte de Activar/Desactivar Comercios</h1>')
        for event in events:
            f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(activar_desactivar_comercios_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'
os.makedirs(screenshots_dir, exist_ok=True)

activar_desactivar_comercios_dir = os.path.join(screenshots_dir, 'ActivarDesactivarComercios')
if os.path.exists(activar_desactivar_comercios_dir):
    shutil.rmtree(activar_desactivar_comercios_dir, onerror=remove_readonly)
os.makedirs(activar_desactivar_comercios_dir, exist_ok=True)

driver = webdriver.Chrome()

events = []
step_number = 1

try:
    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'identifier').send_keys('Admin')
    driver.find_element(By.ID, 'password').send_keys('3322')
    events.append("Credentials entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    events.append("Login submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(3)
    events.append("Dashboard loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    comercios_link = driver.find_element(By.LINK_TEXT, 'Comercios')
    comercios_link.click()
    events.append("Comercios page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(3)

    comercio = driver.find_element(By.CSS_SELECTOR, '.commerce')
    inactivar_button = comercio.find_element(By.CSS_SELECTOR, 'button.btn-warning')
    inactivar_button.click()
    events.append("Comercio inactivated successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(2)

    comercio = driver.find_element(By.CSS_SELECTOR, '.commerce')
    activar_button = comercio.find_element(By.CSS_SELECTOR, 'button.btn-success')
    activar_button.click()
    events.append("Comercio activated successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(2)

except Exception as e:
    events.append(f"An error occurred: {e}")

finally:
    driver.quit()

generate_html_report(events, os.path.join(activar_desactivar_comercios_dir, 'report.html'))