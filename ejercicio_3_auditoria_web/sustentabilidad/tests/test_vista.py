import pytest
from django.urls import reverse

from sustentabilidad.logica import calcular_emisiones_carbono


class TestPanelSustentabilidad:
    @pytest.mark.django_db
    def test_panel_responde_con_estado_200(self, client):
        respuesta = client.get("/")
        assert respuesta.status_code == 200

    @pytest.mark.django_db
    def test_panel_muestra_totales_y_planta_lider(self, client):
        respuesta = client.get("/")
        contenido = respuesta.content.decode("utf-8")
        assert "Panel de Sustentabilidad" in contenido
        assert "Planta Norte - Rosario" in contenido
        assert "Emisiones totales" in contenido
        assert respuesta.context["planta_mayor_consumo"] == "Planta Norte - Rosario"
        assert respuesta.context["emisiones_totales"] > 0

    @pytest.mark.django_db
    def test_url_por_nombre(self, client):
        assert client.get(reverse("sustentabilidad:panel")).status_code == 200

    def test_algoritmo_usado_por_el_panel(self):
        assert calcular_emisiones_carbono(1500) == pytest.approx(600.0)
