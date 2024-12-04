import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def take_full_page_screenshot(driver, file_path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(file_path)
    driver.set_window_size(original_size['width'], original_size['height'])

def generate_html_report(events, output_file):
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Reporte de Formulario Login Test</title></head><body>')
        f.write('<h1>Reporte de Formulario Login Test</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(formulario_login_test_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

formulario_login_test_dir = os.path.join(screenshots_dir, 'FormularioLoginTest')

if os.path.exists(formulario_login_test_dir):
    shutil.rmtree(formulario_login_test_dir, onerror=remove_readonly)

os.makedirs(formulario_login_test_dir, exist_ok=True)

driver = webdriver.Chrome()

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

    forgot_password_link = driver.find_element(By.LINK_TEXT, '¿Olvidaste tu contraseña?')
    forgot_password_link.click()
    events.append("Forgot password link clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1
    driver.back()
    time.sleep(1)

    register_client_link = driver.find_element(By.LINK_TEXT, 'Registrarse como cliente o delivery')
    register_client_link.click()
    events.append("Register client link clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1
    driver.back()
    time.sleep(1)

    register_business_link = driver.find_element(By.LINK_TEXT, 'Registrar comercio')
    register_business_link.click()
    events.append("Register business link clicked successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1
    driver.back()
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    events.append("Login submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(5)
    events.append("Final state loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_full_page_screenshot(driver, os.path.join(formulario_login_test_dir, 'error.png'))

finally:
    driver.quit()

generate_html_report(events, os.path.join(formulario_login_test_dir, 'report.html'))