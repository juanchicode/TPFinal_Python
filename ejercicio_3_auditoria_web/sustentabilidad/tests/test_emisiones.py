import pytest

from sustentabilidad.logica import (
    calcular_emisiones_carbono,
    cargar_registros_consumo,
    obtener_metricas_consumo,
)


class TestCalculoEmisiones:
    def test_calculo_valor_nominal(self):
        assert calcular_emisiones_carbono(1000) == pytest.approx(400.0)

    def test_calculo_con_factor_personalizado(self):
        assert calcular_emisiones_carbono(250, factor_emision=0.2) == pytest.approx(50.0)

    def test_consumo_cero_no_emite(self):
        assert calcular_emisiones_carbono(0) == pytest.approx(0.0)

    def test_consumo_negativo_lanza_value_error(self):
        with pytest.raises(ValueError):
            calcular_emisiones_carbono(-10)

    def test_consumo_negativo_mensaje_descriptivo(self):
        with pytest.raises(ValueError, match="no puede ser negativo"):
            calcular_emisiones_carbono(-0.5)


class TestMetricasConsumo:
    def test_totales_sobre_registros_de_ejemplo(self):
        registros = [
            {"planta": "Planta Norte", "mes": "2026-07", "consumo_kwh": 100},
            {"planta": "Planta Sur", "mes": "2026-07", "consumo_kwh": 300},
        ]
        metricas = obtener_metricas_consumo(registros)
        assert metricas["emisiones_totales"] == pytest.approx(160.0)
        assert metricas["planta_mayor_consumo"] == "Planta Sur"
        assert metricas["consumo_planta_lider"] == 300
        assert metricas["total_registros"] == 2
        assert len(metricas["detalle"]) == 2

    def test_acumula_varios_registros_de_la_misma_planta(self):
        registros = [
            {"planta": "Planta Norte", "mes": "2026-07", "consumo_kwh": 200},
            {"planta": "Planta Norte", "mes": "2026-08", "consumo_kwh": 250},
            {"planta": "Planta Sur", "mes": "2026-07", "consumo_kwh": 300},
        ]
        metricas = obtener_metricas_consumo(registros)
        assert metricas["planta_mayor_consumo"] == "Planta Norte"
        assert metricas["consumo_planta_lider"] == 450
        assert metricas["emisiones_totales"] == pytest.approx(300.0)

    def test_lista_vacia_devuelve_cero(self):
        metricas = obtener_metricas_consumo([])
        assert metricas["emisiones_totales"] == 0.0
        assert metricas["planta_mayor_consumo"] == "Sin datos"
        assert metricas["detalle"] == []

    def test_archivo_json_de_datos_es_valido(self):
        registros = cargar_registros_consumo()
        assert len(registros) > 0
        metricas = obtener_metricas_consumo(registros)
        assert metricas["planta_mayor_consumo"] == "Planta Norte - Rosario"
