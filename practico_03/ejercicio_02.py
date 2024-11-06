"""Variables y Métodos de Clase"""
from typing import Optional


class Articulo:
    """Clase con "nombre" como variable de instancia y un id incremental
    generado automáticamente.

    Restricciones:
        - Utilizar sólamente el constructor (__init__) y un método de
          clase (@classmethod) con una variable de clase
    """
    id_incremental = 0
    # Completar
    def __init__(self, nombre: Optional [str] = None):
        self.nombre = nombre
        self.id_ = Articulo._generaid_()
    
    @classmethod
    def _generaid_(cls) -> int:
        cls.id_incremental += 1
        return cls.id_incremental

    @classmethod
    def _last_id(cls) -> int:
        return cls.id_incremental
    
# NO MODIFICAR - INICIO
art1 = Articulo("manzana")
art2 = Articulo("pera")
art3 = Articulo()   
art3.nombre = "tv"

assert art1.nombre == "manzana"
assert art2.nombre == "pera"
assert art3.nombre == "tv"

assert art1.id_ == 1
assert art2.id_ == 2
assert art3.id_ == 3
assert Articulo._last_id() == 3
# NO MODIFICAR - FIN
