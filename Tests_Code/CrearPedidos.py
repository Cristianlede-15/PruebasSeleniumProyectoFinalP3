import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
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

def take_screenshot(driver, file_path):
    if is_window_open(driver):
        driver.save_screenshot(file_path)
    else:
        print('La ventana del navegador está cerrada. No se puede tomar la captura de pantalla.')

def generate_html_report(events, output_file):
    with open(output_file, 'w') as f:
        f.write('<html><head><title>Reporte de Crear Pedidos</title></head><body>')
        f.write('<h1>Reporte de Crear Pedidos</h1>')
        for event in events:
            if "An error occurred" not in event:
                f.write(f'<p>{event}</p>')
        f.write('</body></html>')

def get_screenshot_filename(step_number):
    return os.path.join(buscar_productos_cliente_dir, f'Captura{step_number}.png')

screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots\CrearPedido'
os.makedirs(screenshots_dir, exist_ok=True)

buscar_productos_cliente_dir = os.path.join(screenshots_dir)

if os.path.exists(buscar_productos_cliente_dir):
    shutil.rmtree(buscar_productos_cliente_dir, onerror=remove_readonly)

os.makedirs(buscar_productos_cliente_dir, exist_ok=True)

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
    email_field.send_keys('Man')
    events.append("Email entered successfully.")

    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    password_field.send_keys('2233')
    events.append("Password entered successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()
    events.append("Login submitted successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Home')))
    events.append("Home page loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    restaurantes_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Restaurantes')))
    restaurantes_link.click()
    events.append("Restaurantes page loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card-body')))
    events.append("Restaurantes page content loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    la_parrilla_element = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//a[@href='/user/comercio/3' and contains(., 'La Parrilla Gourmet')]"
    )))
    la_parrilla_element.click()
    events.append("La Parrilla Gourmet selected successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))
    events.append("La Parrilla Gourmet page loaded successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    agregar_parrillada = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[text()='Agregar al Carrito' and ancestor::form[input[@name='product_id' and @value='5']]]"
    )))
    agregar_parrillada.click()
    events.append("Parrillada added to cart successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    agregar_ensalada = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[text()='Agregar al Carrito' and ancestor::form[input[@name='product_id' and @value='6']]]"
    )))
    agregar_ensalada.click()
    events.append("Ensalada added to cart successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    continuar_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Continuar')))
    continuar_button.click()
    events.append("Continue button clicked successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    direccion_radio = wait.until(EC.element_to_be_clickable((By.ID, 'address4')))
    direccion_radio.click()
    events.append("Address selected successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

    confirmar_pedido_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[@type='submit' and contains(., 'Confirmar Pedido')]"
    )))
    confirmar_pedido_button.click()
    events.append("Order confirmed successfully.")
    take_screenshot(driver, get_screenshot_filename(step_number))
    step_number += 1

except Exception as e:
    events.append("An error occurred")
    take_screenshot(driver, os.path.join(buscar_productos_cliente_dir, 'error.png'))

finally:
    if is_window_open(driver):
        driver.quit()

generate_html_report(events, os.path.join(buscar_productos_cliente_dir, 'report.html'))