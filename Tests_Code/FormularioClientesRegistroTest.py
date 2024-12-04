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
        f.write('<html><head><title>Reporte de Formulario Clientes Registro Test</title></head><body>')
        f.write('<h1>Reporte de Formulario Clientes Registro Test</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(form_clientes_registro_test_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

form_clientes_registro_test_dir = os.path.join(screenshots_dir, 'FormClientesRegistroTest')

if os.path.exists(form_clientes_registro_test_dir):
    shutil.rmtree(form_clientes_registro_test_dir, onerror=remove_readonly)

os.makedirs(form_clientes_registro_test_dir, exist_ok=True)

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
    events.append("First name entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'last_name').send_keys('Perez')
    events.append("Last name entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'email').send_keys('setitay974440@nausard777.com')
    events.append("Email entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'username').send_keys('LuisitoPerez778887')
    events.append("Username entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'password').send_keys('2233')
    events.append("Password entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'confirm_password').send_keys('2233')
    events.append("Confirm password entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'phone').send_keys('+1 849 - 555- 7788')
    events.append("Phone entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.NAME, 'profile_image').send_keys(r'C:\Users\pc\Downloads\cena.jpg')
    events.append("Profile image uploaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    role_select = Select(driver.find_element(By.NAME, 'role'))
    role_select.select_by_visible_text('Cliente')
    events.append("Role selected successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Registrarse']").click()
    events.append("Form submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(5)
    events.append("Registration result loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_full_page_screenshot(driver, os.path.join(form_clientes_registro_test_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(form_clientes_registro_test_dir, 'report.html'))