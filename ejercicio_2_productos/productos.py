"""Ejercicio 2 - Modelo de productos, excepciones y persistencia."""

import json


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock negativo."""


class DispositivoEcológico:
    def __init__(self, nombre, precio, stock, material):
        self.nombre = nombre
        self.precio = precio
        self.material = material
        self.stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise StockInvalidoError(f"El stock debe ser numerico, recibido: {valor!r}")
        if valor < 0:
            raise StockInvalidoError(
                f"El stock no puede ser negativo para '{self.nombre}': {valor}"
            )
        self._stock = int(valor)

    def ficha_tecnica(self):
        return (
            f"Producto: {self.nombre}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Stock: {self.stock} unidades\n"
            f"Material: {self.material}"
        )

    def a_diccionario(self):
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "material": self.material,
            **self.datos_especificos(),
        }

    def datos_especificos(self):
        return {}

    def __str__(self):
        return f"{self.nombre} (stock: {self.stock})"


class PanelSolar(DispositivoEcológico):
    def __init__(self, nombre, precio, stock, material, potencia_wp, eficiencia):
        super().__init__(nombre, precio, stock, material)
        self.potencia_wp = potencia_wp
        self.eficiencia = eficiencia

    def ficha_tecnica(self):
        ficha_base = super().ficha_tecnica()
        return (
            f"{ficha_base}\n"
            f"Potencia: {self.potencia_wp} Wp\n"
            f"Eficiencia: {self.eficiencia}%"
        )

    def datos_especificos(self):
        return {"potencia_wp": self.potencia_wp, "eficiencia": self.eficiencia}


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        catalogo = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, ensure_ascii=False, indent=2)
        return ruta_archivo


if __name__ == "__main__":
    catalogo = [
        DispositivoEcológico("Termotanque Solar 150L", 289999.0, 12, "Acero inoxidable"),
        PanelSolar("Panel Monocristalino 450Wp", 189999.0, 40, "Silicio", 450, 21.5),
        PanelSolar("Panel Policristalino 330Wp", 129999.0, 25, "Silicio", 330, 17.8),
    ]

    print("=" * 62)
    print("ALTA DE PRODUCTO CON STOCK INVALIDO")
    print("=" * 62)
    try:
        PanelSolar("Panel de Prueba", 9999.0, -5, "Silicio", 100, 15.0)
    except StockInvalidoError as error:
        print(f"Excepcion capturada -> StockInvalidoError: {error}")

    print()
    print("=" * 62)
    print("FICHA TECNICA (polimorfismo)")
    print("=" * 62)
    for producto in catalogo:
        print(producto.ficha_tecnica())
        print("-" * 62)

    ruta = GestorInventario.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Catalogo exportado correctamente a: {ruta}")
