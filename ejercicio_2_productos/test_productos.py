import json

import pytest

from ejercicio_2_productos.productos import (
    DispositivoEcológico,
    GestorInventario,
    PanelSolar,
    StockInvalidoError,
)


def test_stock_negativo_lanza_error():
    with pytest.raises(StockInvalidoError, match="negativo"):
        DispositivoEcológico("Lámpara LED", 999.0, -3, "Aluminio")


def test_stock_negativo_en_subclase_tambien_lanza():
    with pytest.raises(StockInvalidoError):
        PanelSolar("Panel de Prueba", 9999.0, -5, "Silicio", 100, 15.0)


def test_stock_no_numerico_lanza_error():
    with pytest.raises(StockInvalidoError, match="numerico"):
        DispositivoEcológico("Lámpara LED", 999.0, "muchos", "Aluminio")


def test_stock_booleano_lanza_error():
    with pytest.raises(StockInvalidoError):
        DispositivoEcológico("Lámpara LED", 999.0, True, "Aluminio")


def test_stock_float_valido_se_convierte_a_entero():
    producto = DispositivoEcológico("Lámpara LED", 999.0, 40.0, "Aluminio")
    assert producto.stock == 40
    assert isinstance(producto.stock, int)


def test_stock_cero_es_valido():
    producto = DispositivoEcológico("Lámpara LED", 999.0, 0, "Aluminio")
    assert producto.stock == 0


def test_ficha_tecnica_base_contiene_los_campos():
    producto = DispositivoEcológico("Termotanque Solar 150L", 289999.0, 12, "Acero")
    ficha = producto.ficha_tecnica()
    assert "Termotanque Solar 150L" in ficha
    assert "289,999.00" in ficha
    assert "12 unidades" in ficha
    assert "Acero" in ficha


def test_ficha_tecnica_panel_solar_incluye_potencia_y_eficiencia():
    panel = PanelSolar("Panel Monocristalino 450Wp", 189999.0, 40, "Silicio", 450, 21.5)
    ficha = panel.ficha_tecnica()
    assert "Potencia: 450 Wp" in ficha
    assert "Eficiencia: 21.5%" in ficha


def test_a_diccionario_incluye_tipo_y_datos_especificos():
    panel = PanelSolar("Panel Policristalino 330Wp", 129999.0, 25, "Silicio", 330, 17.8)
    datos = panel.a_diccionario()
    assert datos["tipo"] == "PanelSolar"
    assert datos["potencia_wp"] == 330
    assert datos["eficiencia"] == 17.8
    assert datos["stock"] == 25


def test_a_diccionario_base_no_incluye_datos_de_hijo():
    producto = DispositivoEcológico("Termotanque Solar 150L", 289999.0, 12, "Acero")
    datos = producto.a_diccionario()
    assert datos["tipo"] == "DispositivoEcológico"
    assert "potencia_wp" not in datos


def test_str_describe_producto():
    producto = DispositivoEcológico("Lámpara LED", 999.0, 7, "Aluminio")
    assert str(producto) == "Lámpara LED (stock: 7)"


def test_json_guarda_y_lee(tmp_path):
    catalogo = [
        DispositivoEcológico("Termotanque Solar 150L", 289999.0, 12, "Acero inoxidable"),
        PanelSolar("Panel Monocristalino 450Wp", 189999.0, 40, "Silicio", 450, 21.5),
    ]
    ruta = tmp_path / "catalogo_test.json"

    ruta_devuelta = GestorInventario.guardar_catalogo_json(catalogo, ruta)
    assert ruta_devuelta == ruta

    with open(ruta, encoding="utf-8") as archivo:
        guardado = json.load(archivo)

    assert len(guardado) == 2
    assert guardado[0]["nombre"] == "Termotanque Solar 150L"
    assert guardado[1]["potencia_wp"] == 450
    assert guardado[1]["eficiencia"] == 21.5
