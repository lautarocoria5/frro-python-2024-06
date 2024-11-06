"""Propiedades"""


class Auto:
    """La clase auto tiene dos propiedades, precio y marca. La marca se define
    obligatoriamente al construir la clase y siempre que se devuelve, se 
    devuelve con la primer letra en mayúscula y no se puede modificar. El precio
    puede modificarse pero cuando se muestra, se redondea a 2 decimales
    
    Restricción: Usar Properties
    
    Referencia: https://docs.python.org/3/library/functions.html#property"""


    def __init__(self, nombre: str, precio: float):
        self._precio = precio
        self._marca = nombre

    @property
    def precio(self):
        # Redondear el precio a 2 decimales cuando se obtiene
        return round(self._precio, 2)

    @property
    def nombre(self):
        # Retornar la marca capitalizada
        return self._marca.capitalize()

    @precio.setter
    def precio(self, value: float):
        # Redondear el valor del precio antes de asignarlo
        self._precio = round(value, 2)
        



# NO MODIFICAR - INICIO
auto = Auto("Ford", 12_875.456)

assert auto.nombre == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.nombre = "Chevrolet"
    assert False
except AttributeError:
    assert True
# NO MODIFICAR - FIN


###############################################################################


from dataclasses import dataclass

@dataclass
class Auto:
    """Re-Escribir utilizando DataClasses"""

    # Atributos de la clase
    _precio: float
    _nombre: str

    # Constructor __init__ para inicializar los valores
    def __init__(self, nombre: str, precio: float):
        self._precio = round(precio, 2)  # Redondear precio al crear la instancia
        self._nombre = nombre.capitalize()  # Capitalizar el nombre al crear la instancia

    # Propiedad para el precio
    @property
    def precio(self):
        return self._precio

    # Propiedad para el nombre (solo getter, no setter)
    @property
    def nombre(self):
        return self._nombre

    # Setter para el precio
    @precio.setter
    def precio(self, value: float):
        self._precio = round(value, 2)

# NO MODIFICAR - INICIO
auto = Auto("Ford", 12_875.456)

assert auto.nombre == "Ford"
assert auto.precio == 12_875.46
auto.precio = 13_874.349
assert auto.precio == 13_874.35

try:
    auto.nombre = "Chevrolet"
    assert False
except AttributeError:
    assert True
# NO MODIFICAR - FIN
