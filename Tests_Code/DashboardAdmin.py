import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def take_screenshot(driver, file_path):
    if is_window_open(driver):
        driver.save_screenshot(file_path)
    else:
        print('La ventana del navegador está cerrada. No se puede tomar la captura de pantalla.')

def generate_html_report(events, output_file):
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Reporte de Dashboard Admin</title></head><body>')
        f.write('<h1>Reporte de Dashboard Admin</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(dashboard_admin_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

os.makedirs(screenshots_dir, exist_ok=True)

dashboard_admin_dir = os.path.join(screenshots_dir, 'DashboardAdmin')

if os.path.exists(dashboard_admin_dir):
    shutil.rmtree(dashboard_admin_dir, onerror=remove_readonly)

os.makedirs(dashboard_admin_dir, exist_ok=True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

events = []
step_number = 1

try:
    wait = WebDriverWait(driver, 20)

    driver.get('http://localhost:3000/auth/login')
    events.append("Login page loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    email_field = wait.until(EC.presence_of_element_located((By.ID, 'identifier')))
    email_field.send_keys('Admin')
    events.append("Email entered successfully.")

    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('3322')
    events.append("Password entered successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()
    events.append("Login submitted successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    dashboard_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Dashboard')))
    events.append("Dashboard loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_screenshot(driver, os.path.join(dashboard_admin_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(dashboard_admin_dir, 'report.html'))