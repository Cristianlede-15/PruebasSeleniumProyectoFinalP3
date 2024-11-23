import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_buscar_pikachu(driver):
    driver.get("http://localhost:3000/")
    if not os.path.exists('screenshots/test_buscar_nombre_Pokemon'):
        os.makedirs('screenshots/test_buscar_nombre_Pokemon')
   
   
    driver.save_screenshot('screenshots/test_buscar_nombre_Pokemon/AbrirPagina.png')
    search_box = driver.find_element(By.NAME, "name")
    driver.save_screenshot('screenshots/test_buscar_nombre_Pokemon/LocalizarBarraBusqueda.png')
    search_box.send_keys("Pikachu")
    driver.save_screenshot('screenshots/test_buscar_nombre_Pokemon/IngresarTexto.png')
    search_box.send_keys(Keys.RETURN)
    driver.save_screenshot('screenshots/test_buscar_nombre_Pokemon/Buscar.png')
    assert "Pikachu" in driver.page_source
    driver.save_screenshot('screenshots/test_buscar_nombre_Pokemon/PokemonEncontrado.png')