import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_crear_pokemon(driver):
    driver.get("http://localhost:3000/pokemones/new")
    if not os.path.exists('screenshots/test_crearPokemon'):
        os.makedirs('screenshots/test_crearPokemon')
    driver.save_screenshot('screenshots/test_crearPokemon/AbrirPagina.png')

    wait = WebDriverWait(driver, 10)

    nombre = wait.until(EC.presence_of_element_located((By.ID, "nombre")))
    nombre.send_keys("Raichu")
    driver.save_screenshot('screenshots/test_crearPokemon/EscribirNombre.png')

    tipo = Select(wait.until(EC.presence_of_element_located((By.ID, "tipo"))))
    tipo.select_by_visible_text("Eléctrico")
    driver.save_screenshot('screenshots/test_crearPokemon/SeleccionarTipo.png')

    region = Select(wait.until(EC.presence_of_element_located((By.ID, "region"))))
    region.select_by_visible_text("Kanto")
    driver.save_screenshot('screenshots/test_crearPokemon/SeleccionarRegion.png')

    url_imagen = wait.until(EC.presence_of_element_located((By.ID, "url_imagen")))
    url_imagen.send_keys("https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/detail/026.png")
    driver.save_screenshot('screenshots/test_crearPokemon/IngresarURLImagen.png')

    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()
    driver.save_screenshot('screenshots/test_crearPokemon/EnviarFormulario.png')

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pokemon-grid")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.save_screenshot('screenshots/test_crearPokemon/PgDn.png')

    assert "Raichu" in driver.page_source
    driver.save_screenshot('screenshots/test_crearPokemon/PokemonCreado.png')