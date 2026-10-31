import json
from pathlib import Path

FACTOR_EMISION_DEFECTO = 0.4

ARCHIVO_CONSUMO = (
    Path(__file__).resolve().parent / "data" / "datos_consumo.json"
)


def calcular_emisiones_carbono(consumo_kwh, factor_emision=FACTOR_EMISION_DEFECTO):
    if consumo_kwh < 0:
        raise ValueError(f"El consumo no puede ser negativo: {consumo_kwh}")
    return consumo_kwh * factor_emision


def cargar_registros_consumo(ruta_archivo=ARCHIVO_CONSUMO):
    with open(ruta_archivo, encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_metricas_consumo(registros):
    if not registros:
        return {
            "emisiones_totales": 0.0,
            "planta_mayor_consumo": "Sin datos",
            "consumo_planta_lider": 0.0,
            "detalle": [],
            "total_registros": 0,
        }

    consumo_por_planta = {}
    emisiones_totales = 0.0

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]
        emisiones = calcular_emisiones_carbono(consumo)
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + consumo
        emisiones_totales += emisiones

    planta_lider = max(consumo_por_planta, key=consumo_por_planta.get)

    detalle = [
        {
            "planta": planta,
            "consumo_kwh": consumo,
            "emisiones": round(
                calcular_emisiones_carbono(consumo), 2
            ),
        }
        for planta, consumo in sorted(
            consumo_por_planta.items(), key=lambda item: item[1], reverse=True
        )
    ]

    return {
        "emisiones_totales": round(emisiones_totales, 2),
        "planta_mayor_consumo": planta_lider,
        "consumo_planta_lider": consumo_por_planta[planta_lider],
        "detalle": detalle,
        "total_registros": len(registros),
    }
