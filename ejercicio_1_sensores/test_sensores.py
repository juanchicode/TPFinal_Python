import pytest

from ejercicio_1_sensores.sensores import (
    generar_resumen_sensores,
    limpiar_registro_sensor,
)


def test_limpiar_registro_quita_espacios_y_unidades():
    resultado = limpiar_registro_sensor(
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"}
    )
    assert resultado == {
        "sensor_id": "SENSOR-001",
        "temperatura": 24.5,
        "ubicacion": "Planta Norte",
    }


def test_temperatura_con_coma_decimal():
    resultado = limpiar_registro_sensor(
        {"sensor_id": "S2", "temperatura": " 31,8 °C", "ubicacion": "Planta Sur"}
    )
    assert resultado["temperatura"] == pytest.approx(31.8)


def test_ubicacion_vacia_usa_valor_por_defecto():
    resultado = limpiar_registro_sensor(
        {"sensor_id": "S3", "temperatura": "19C", "ubicacion": "   "}
    )
    assert resultado["ubicacion"] == "No especificada"
    assert limpiar_registro_sensor({"sensor_id": "S4", "temperatura": "19C"})[
        "ubicacion"
    ] == "No especificada"


def test_temperatura_invalida_lanza_value_error():
    with pytest.raises(ValueError):
        limpiar_registro_sensor({"sensor_id": "S5", "temperatura": "alta"})


def test_resumen_alertas_y_promedio():
    limpios = [
        {"sensor_id": "A", "temperatura": 33.0, "ubicacion": "Norte"},
        {"sensor_id": "B", "temperatura": 28.5, "ubicacion": "Sur"},
        {"sensor_id": "C", "temperatura": 31.2, "ubicacion": "Norte"},
    ]
    en_alerta, promedio = generar_resumen_sensores(limpios, umbral_temperatura=30)
    assert en_alerta == ["A", "C"]
    assert promedio == pytest.approx(30.9)


def test_resumen_lista_vacia():
    assert generar_resumen_sensores([], 30) == ([], 0.0)
