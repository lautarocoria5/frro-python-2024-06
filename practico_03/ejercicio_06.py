"""Magic Methods"""

from __future__ import annotations
from typing import List


# NO MODIFICAR - INICIO
class Article:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        """Devuelve el nombre del artículo como una cadena."""
        return self.name

    def __repr__(self) -> str:
        """Devuelve la representación del artículo para reproducibilidad."""
        return f"Article('{self.name}')"

    def __eq__(self, other: object) -> bool:
        """Compara dos artículos para ver si tienen el mismo nombre."""
        if isinstance(other, Article):
            return self.name == other.name
        return False


class ShoppingCart:
    """Agregar los métodos que sean necesarios para que los test funcionen.
    Hint: los métodos necesarios son todos magic methods
    Referencia: https://docs.python.org/3/reference/datamodel.html#basic-customization
    """

    def __init__(self, articles: List[Article] = None) -> None:
        if articles is None:
            self.articles = []
        else:
            self.articles = articles

    def __str__(self) -> str:
        """Devuelve la lista de artículos como una cadena."""
        return str([str(article) for article in self.articles])

    def __repr__(self) -> str:
        """Devuelve una representación del carrito para su reproducibilidad."""
        return f"ShoppingCart({repr(self.articles)})"

    def __eq__(self, other: object) -> bool:
        """Compara dos carritos de compras verificando si contienen los mismos artículos, sin importar el orden."""
        if isinstance(other, ShoppingCart):
            return sorted(self.articles, key=lambda x: x.name) == sorted(other.articles, key=lambda x: x.name)
        return False

    def __add__(self, other: ShoppingCart) -> ShoppingCart:
        """Permite sumar dos carritos de compras (combinar sus artículos)."""
        if isinstance(other, ShoppingCart):
            return ShoppingCart(self.articles + other.articles)
        return self

    def add(self, article: Article) -> ShoppingCart:
        self.articles.append(article)
        return self

    def remove(self, remove_article: Article) -> ShoppingCart:
        self.articles = [article for article in self.articles if article != remove_article]
        return self

    # NO MODIFICAR - FIN

    # Completar


# NO MODIFICAR - INICIO

manzana = Article("Manzana")
pera = Article("Pera")
tv = Article("Television")

# Test de conversión a String
assert str(ShoppingCart().add(manzana).add(pera)) == "['Manzana', 'Pera']"

# Test de reproducibilidad
carrito = ShoppingCart().add(manzana).add(pera)
assert carrito == eval(repr(carrito))

# Test de igualdad
assert ShoppingCart().add(manzana) == ShoppingCart().add(manzana)

# Test de remover objeto
assert ShoppingCart().add(tv).add(pera).remove(tv) == ShoppingCart().add(pera)

# Test de igualdad con distinto orden
assert ShoppingCart().add(tv).add(pera) == ShoppingCart().add(pera).add(tv)

# Test de suma
combinado = ShoppingCart().add(manzana) + ShoppingCart().add(pera)
assert combinado == ShoppingCart().add(manzana).add(pera)

# NO MODIFICAR - FIN
