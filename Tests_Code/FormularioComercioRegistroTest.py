from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
import stat

def take_full_page_screenshot(driver, file_path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(file_path)
    driver.set_window_size(original_size['width'], original_size['height'])

def generate_html_report(events, output_file):
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Reporte de Formulario Comercio Registro Test</title></head><body>')
        f.write('<h1>Reporte de Formulario Comercio Registro Test</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_screenshot_filename(step_number):
    return os.path.join(form_registro_test_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

form_registro_test_dir = os.path.join(screenshots_dir, 'FormRegistroTest')

if os.path.exists(form_registro_test_dir):
    shutil.rmtree(form_registro_test_dir, onerror=remove_readonly)

os.makedirs(form_registro_test_dir, exist_ok=True)

driver = webdriver.Chrome()

events = []
step_number = 1

try:
    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    register_link = driver.find_element(By.LINK_TEXT, 'Registrar comercio')
    register_link.click()
    events.append("Register page loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'business_name').send_keys('Comedor Maria')
    events.append("Business name entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'phone').send_keys('+1 809-888-9999')
    events.append("Phone entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'email').send_keys('ComedorMaria57865@nausard.com')
    events.append("Email entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'logo').send_keys(r'C:\Users\pc\Downloads\logorestaurante.webp')
    events.append("Logo uploaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.execute_script("document.getElementById('opening_time').value = '08:00'")
    events.append("Opening time entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.execute_script("document.getElementById('closing_time').value = '21:00'")
    events.append("Closing time entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    business_type_element = driver.find_element(By.ID, 'business_type')
    options = business_type_element.find_elements(By.TAG_NAME, 'option')
    for option in options:
        print('Available option:', option.text)
    events.append("Business type options displayed successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    business_type = Select(business_type_element)
    business_type.select_by_visible_text('Restaurantes')
    events.append("Business type selected successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'password').send_keys('2233')
    events.append("Password entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.ID, 'confirm_password').send_keys('2233')
    events.append("Confirm password entered successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    driver.find_element(By.XPATH, "//button[text()='Registrar Comercio']").click()
    events.append("Form submitted successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    time.sleep(5)
    events.append("Registration result loaded successfully.")
    take_full_page_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_full_page_screenshot(driver, os.path.join(form_registro_test_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(form_registro_test_dir, 'report.html'))