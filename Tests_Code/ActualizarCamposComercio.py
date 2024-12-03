import os
import shutil
import stat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Función para manejar errores de permisos
def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Función para verificar si la ventana está abierta
def is_window_open(driver):
    try:
        driver.current_window_handle
        return True
    except:
        return False

# Función para tomar capturas de pantalla de página completa
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

# Ruta para el directorio de capturas
screenshots_dir = r'C:\Users\pc\OneDrive - Instituto Tecnológico de Las Américas (ITLA)\Desktop\TareaSeleniumP3\screenshots'

# Crear el directorio de capturas si no existe
os.makedirs(screenshots_dir, exist_ok=True)

# Ruta para el directorio específico de este test
actualizar_campos_comercio_dir = os.path.join(screenshots_dir, 'ActualizarCamposComercio')

# Eliminar el directorio si existe
if os.path.exists(actualizar_campos_comercio_dir):
    shutil.rmtree(actualizar_campos_comercio_dir, onerror=remove_readonly)

# Crear el directorio
os.makedirs(actualizar_campos_comercio_dir, exist_ok=True)

# Inicializar el WebDriver
driver = webdriver.Chrome()



try:
    # Paso 1: Abrir la página de login
    driver.get('http://localhost:3000/auth/login')
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step1_login_page.png'))

    # Paso 2: Ingresar credenciales del comercio
    driver.find_element(By.ID, 'identifier').send_keys('bipomoc548@cantozil.com')
    driver.find_element(By.ID, 'password').send_keys('2233')
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step2_credentials_entered.png'))

    # Paso 3: Enviar el formulario de login
    driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step3_login_submitted.png'))

    # Esperar a que la página de home del comercio cargue
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Perfil')))
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step4_home_loaded.png'))

    # Paso 4: Navegar a "Perfil"
    perfil_link = driver.find_element(By.LINK_TEXT, 'Perfil')
    perfil_link.click()
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step5_perfil_page.png'))

    # Esperar a que la página de perfil cargue
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'business_name')))

    # Paso 5: Editar el nombre del comercio
    nombre_input = driver.find_element(By.NAME, 'business_name')
    nombre_input.clear()
    nombre_input.send_keys('Pica Pollo la Esperanza')

    # Paso 6: Editar la dirección
    direccion_input = driver.find_element(By.NAME, 'address')
    direccion_input.clear()
    direccion_input.send_keys('Av. Independencia')

    # Validar que no queden campos vacíos
    assert nombre_input.get_attribute('value') != '', "El campo 'Nombre del Comercio' está vacío."
    assert direccion_input.get_attribute('value') != '', "El campo 'Dirección' está vacío."

    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step6_filled_form.png'))

    # Paso 7: Enviar el formulario de actualización
    # Esperar que el botón "Guardar cambios" sea clickeable
    actualizar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Guardar cambios']"))
    )
    actualizar_button.click()
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step7_form_submitted.png'))

    # Esperar la respuesta
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-success')))
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'step8_update_result.png'))

except Exception as e:
    print('An error occurred:', e)
    take_full_page_screenshot(driver, os.path.join(actualizar_campos_comercio_dir, 'error.png'))

finally:
    if is_window_open(driver):
        # Cerrar el navegador
        driver.quit()