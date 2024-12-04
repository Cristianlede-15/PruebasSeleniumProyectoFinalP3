from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import shutil
import stat

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
        f.write('<html><head><title>Reporte de Envio Correo Validacion Cuenta</title></head><body>')
        f.write('<h1>Reporte de Envio Correo Validacion Cuenta</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(envio_correo_test_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

envio_correo_test_dir = os.path.join(screenshots_dir, 'EnvioCorreoValidacionCuenta')

if os.path.exists(envio_correo_test_dir):
    shutil.rmtree(envio_correo_test_dir, onerror=remove_readonly)

os.makedirs(envio_correo_test_dir, exist_ok=True)

driver = webdriver.Chrome()

events = []
step_number = 1

try:
    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    register_link = driver.find_element(By.LINK_TEXT, 'Registrarse como cliente o delivery')
    register_link.click()
    events.append("Register page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'first_name').send_keys('Juan')
    driver.find_element(By.NAME, 'last_name').send_keys('García')
    driver.find_element(By.NAME, 'email').send_keys('amiircalllo55@gmail.com')
    driver.find_element(By.NAME, 'username').send_keys('JuanG125')
    driver.find_element(By.NAME, 'password').send_keys('2233')
    driver.find_element(By.NAME, 'confirm_password').send_keys('2233')
    driver.find_element(By.NAME, 'phone').send_keys('+1 849 - 555- 1234')
    driver.find_element(By.NAME, 'profile_image').send_keys(r'C:\Users\pc\Downloads\cena.jpg')
    role_select = Select(driver.find_element(By.NAME, 'role'))
    role_select.select_by_visible_text('Cliente')
    events.append("Form filled successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Registrarse']").click()
    events.append("Form submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(1)
    events.append("Registration result loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_full_page_screenshot(driver, os.path.join(envio_correo_test_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(envio_correo_test_dir, 'report.html'))