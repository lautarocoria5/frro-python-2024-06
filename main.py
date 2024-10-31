from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from app import db, create_app
from app.models import Inmueble
import re
from sqlalchemy.exc import IntegrityError
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.DEBUG)  # Cambia DEBUG a WARNING
logging.getLogger("urllib3").setLevel(logging.WARNING)  # Cambia DEBUG a WARNING

# Crear la aplicación y empujar el contexto de aplicación
app = create_app()

# Usar el contexto de la aplicación para las operaciones de base de datos
with app.app_context():
    # Configurar el servicio de GeckoDriver
    service = FirefoxService(executable_path=GeckoDriverManager().install())

    # Crear una instancia de Firefox con GeckoDriver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Ejecutar Firefox en modo headless
    driver = webdriver.Firefox(service=service, options=options)

    # URL de la página web de inmuebles en MercadoLibre
    base_url = 'https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/santa-fe/rosario/'
    page = 1

    try:
        while True:
            url = base_url if page == 1 else f"{base_url}_Desde_{(page - 1) * 50 + 1}"
            print(f"Accediendo a la URL: {url}")

            driver.get(url)
            time.sleep(5)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-layout__item')))
                #WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ui-search-layout__item'))) ##li.ui-search-layout__item
            except TimeoutException:
                print("Timeout: No se encontraron elementos en el tiempo especificado.")
                break

            #listings = driver.find_elements(By.CSS_SELECTOR, 'li.ui-search-layout__item')
            listings = driver.find_elements(By.CLASS_NAME, 'ui-search-layout__item')

            if not listings:
                print("No se encontraron listados, se detiene la extracción.")
                break

            def clean_price(price_text):
                """Limpia y convierte el texto del precio a float."""
                if price_text:
                    try:
                        price_text = re.sub(r'[^\d,]', '', price_text)
                        if ',' in price_text:
                            price_text = price_text.replace('.', '').replace(',', '.')
                        price_value = float(price_text)
                        return price_value if price_value > 0 else None
                    except ValueError as e:
                        print(f"Error al convertir a float: '{price_text}': {e}")
                        return None
                return None

            def extract_value(element, keyword):
                """Extrae el valor correspondiente a un keyword del elemento."""
                try:
                    values = element.find_elements(By.CSS_SELECTOR, 'li.poly-attributes-list__item')
                    value_text = next((el.text for el in values if keyword in el.text), None)
                    return int(value_text.split(' ')[0]) if value_text else None
                except Exception as e:
                    print(f'Error al extraer {keyword}: {e}')
                    return None

            inmuebles_nuevos = []  # Lista para almacenar nuevos inmuebles
            for listing in listings:
                try:
                    title_element = listing.find_element(By.CSS_SELECTOR, 'h2')
                    title = title_element.text

                    price_element = listing.find_element(By.CSS_SELECTOR, 'span.andes-money-amount__fraction')
                    price_value = clean_price(price_element.text.strip() if price_element else None)

                    location_element = listing.find_element(By.CSS_SELECTOR, 'span.poly-component__location')
                    location = location_element.text
                    link_element = listing.find_element(By.CSS_SELECTOR, 'a')
                    link = link_element.get_attribute('href')

                    # Verificar si el inmueble ya existe en la base de datos por título y link
                    if Inmueble.query.filter_by(title=title, link=link).first():
                        print(f"Inmueble ya existe en la base de datos: {title}")
                        continue  # Saltar este inmueble si ya existe

                    print(f'Título: {title}, Precio: {price_value}, Ubicación: {location}, Link: {link}')

                    # Extraer ambientes
                    ambientes_value = extract_value(listing, 'amb.')
                    if ambientes_value is None:
                        ambientes_value = 0  # Valor por defecto

                    # Extraer baños
                    banos_value = extract_value(listing, 'baño')
                    if banos_value is None:
                        banos_value = 0  # Valor por defecto

                    # Extraer metros cuadrados
                    metros_element = listing.find_elements(By.CSS_SELECTOR, 'li.poly-attributes-list__item')
                    metros_text = next((el.text for el in metros_element if 'm²' in el.text), None)
                    metros_value = float(metros_text.split(' ')[0].replace(',', '.')) if metros_text else 0.0

                    # Solo agregar inmuebles con precios válidos
                    if price_value is not None:
                        inmueble = Inmueble(
                            title=title,
                            price=price_value,
                            location=location,
                            ambientes=ambientes_value,
                            banos=banos_value,
                            metros_cuadrados=metros_value,
                            link=link
                        )
                        inmuebles_nuevos.append(inmueble)

                except Exception as e:
                    print(f'Error al procesar el listado: {e}')

            # Insertar nuevos inmuebles en la base de datos
            if inmuebles_nuevos:
                db.session.add_all(inmuebles_nuevos)
                try:
                    db.session.commit()
                    print(f'{len(inmuebles_nuevos)} inmuebles guardados.')
                except IntegrityError as e:
                    print(f'Error de integridad: {e.orig}')
                    db.session.rollback()
                except Exception as e:
                    print(f'Error al guardar los inmuebles: {e}')
                    db.session.rollback()

            page += 1

    except Exception as e:
        print(f'Error en el script principal: {e}')
        import traceback
        traceback.print_exc()

    finally:
        driver.quit()
