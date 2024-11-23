import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()



def test_buscar_agua(driver):
    driver.get("http://localhost:3000/tipos")
    if not os.path.exists('screenshots/test_buscarTipo'):
        os.makedirs('screenshots/test_buscarTipo')
    driver.save_screenshot('screenshots/test_buscarTipo/AbrirPagina.png')

    search_box = driver.find_element(By.NAME, "name")
    search_box.send_keys("Agua")
    driver.save_screenshot('screenshots/test_buscarTipo/EscribirTipoABuscar.png')

    search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    search_button.click()
    driver.save_screenshot('screenshots/test_buscarTipo/EnviarBusqueda.png')

    assert "Agua" in driver.page_source
    driver.save_screenshot('screenshots/test_buscarTipo/TipoEncontrado.png')