from django.shortcuts import render

from sustentabilidad.logica import (
    FACTOR_EMISION_DEFECTO,
    cargar_registros_consumo,
    obtener_metricas_consumo,
)


def vista_panel_sustentabilidad(request):
    registros = cargar_registros_consumo()
    metricas = obtener_metricas_consumo(registros)
    contexto = {
        **metricas,
        "factor_emision": FACTOR_EMISION_DEFECTO,
    }
    return render(request, "sustentabilidad/panel.html", contexto)
