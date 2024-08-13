# app/routes.py
from flask import render_template, request, redirect, url_for
from app.models import Inmueble
from app import db
import spacy

def setup_routes(app):
    # Cargar el modelo de lenguaje en español
    nlp = spacy.load("es_core_news_sm")

    @app.route('/')
    def index():
        try:
            inmuebles = Inmueble.query.all()
            if not inmuebles:
                print("No se encontraron inmuebles en la base de datos.")
            return render_template('index.html', inmuebles=inmuebles)
        except Exception as e:
            import traceback
            traceback.print_exc()  # Imprime el traceback completo del error
            print(f"Ocurrió un error en la consulta: {e}")
            return "Ocurrió un error al acceder a la base de datos."

    @app.route('/search', methods=['POST'])
    def search():
        query = request.form.get('query')
        if query:
            results = search_inmuebles(query)
            if not results:
                mensaje = "No se encontraron departamentos con las especificaciones indicadas."
            else:
                mensaje = None
            return render_template('index.html', inmuebles=results, mensaje=mensaje)
        return redirect(url_for('index'))

    def search_inmuebles(query):
        # Procesar la consulta con spaCy
        doc = nlp(query.lower())

        # Inicializar criterios de búsqueda
        price_max = None
        price_min = None
        num_ambientes = None
        num_banos = None
        location_keywords = []

        # Análisis de entidades y palabras clave
        for token in doc:
            print(f"Token encontrado: {token.text} - POS: {token.pos_}")  # Depuración de tokens

            # Buscar el número asociado a las palabras clave 'menor', 'mayor', 'igual'
            if token.like_num:
                if token.i > 0:
                    prev_token = doc[token.i - 1].text
                    if prev_token in ["menor", "menos", "bajo", "inferior"]:
                        price_max = float(token.text)
                    elif prev_token in ["mayor", "más", "sobre", "superior"]:
                        price_min = float(token.text)
                    elif prev_token in ["igual", "exacto"]:
                        price_min = float(token.text)
                        price_max = float(token.text)
                if token.i < len(doc) - 1:
                    next_token = doc[token.i + 1].text
                    if next_token in ["menor", "menos", "bajo", "inferior"]:
                        price_max = float(token.text)
                    elif next_token in ["mayor", "más", "sobre", "superior"]:
                        price_min = float(token.text)
                    elif next_token in ["igual", "exacto"]:
                        price_min = float(token.text)
                        price_max = float(token.text)

        # Detectar precios en frases como "menor a 200000", "mayor de 250000"
        for i, token in enumerate(doc):
            if token.like_num:
                if i > 0 and doc[i-1].text in ["menor", "menos", "bajo", "inferior"]:
                    price_max = float(token.text)
                elif i > 0 and doc[i-1].text in ["mayor", "más", "sobre", "superior"]:
                    price_min = float(token.text)
                elif i > 1 and doc[i-2].text in ["menor", "menos", "bajo", "inferior"] and doc[i-1].text in ["a", "de"]:
                    price_max = float(token.text)
                elif i > 1 and doc[i-2].text in ["mayor", "más", "sobre", "superior"] and doc[i-1].text in ["a", "de"]:
                    price_min = float(token.text)
                elif i > 1 and doc[i-2].text in ["igual", "exacto"] and doc[i-1].text in ["a", "de"]:
                    price_min = float(token.text)
                    price_max = float(token.text)

        # Manejo de ambientes y baños
        for token in doc:
            if token.text in ["ambientes", "ambiente"] and token.nbor(-1).like_num:
                num_ambientes = int(token.nbor(-1).text)
            elif token.text in ["baños", "baño"] and token.nbor(-1).like_num:
                num_banos = int(token.nbor(-1).text)
            elif token.text in ["ambientes", "ambiente"]:
                if token.nbor(1).like_num:
                    num_ambientes = int(token.nbor(1).text)
            elif token.text in ["baños", "baño"]:
                if token.nbor(1).like_num:
                    num_banos = int(token.nbor(1).text)

        # Verificar ubicación si hay palabras clave en la consulta
        for token in doc:
            if token.text in ["santa", "fe", "rosario"]:
                location_keywords.append(token.text)

        # Depuración de los valores extraídos
        print(f"Precio máximo: {price_max}")
        print(f"Precio mínimo: {price_min}")
        print(f"Ambientes: {num_ambientes}")
        print(f"Baños: {num_banos}")
        print(f"Palabras clave de ubicación: {location_keywords}")

        # Filtrar inmuebles
        query_obj = Inmueble.query
        if price_max is not None:
            query_obj = query_obj.filter(Inmueble.price <= price_max)
        if price_min is not None:
            query_obj = query_obj.filter(Inmueble.price >= price_min)
        if num_ambientes is not None:
            query_obj = query_obj.filter(Inmueble.ambientes == num_ambientes)
        if num_banos is not None:
            query_obj = query_obj.filter(Inmueble.banos == num_banos)
        for keyword in location_keywords:
            query_obj = query_obj.filter(Inmueble.location.ilike(f"%{keyword}%"))

        results = query_obj.all()
        return results

    @app.route('/scrape', methods=['POST'])
    def scrape():
        try:
            from app.scraping_script import scrape_inmuebles
            scrape_inmuebles()
            # Confirmar que los datos fueron cargados
            inmuebles = Inmueble.query.all()
            print(f"Datos cargados: {len(inmuebles)} inmuebles encontrados.")
            return redirect(url_for('index'))
        except Exception as e:
            import traceback
            traceback.print_exc()  # Imprime el traceback completo del error
            print(f"Ocurrió un error al recargar los datos: {e}")
            return "Ocurrió un error al recargar los datos."
