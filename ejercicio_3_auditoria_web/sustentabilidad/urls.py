from django.urls import path

from sustentabilidad.views import vista_panel_sustentabilidad

app_name = "sustentabilidad"

urlpatterns = [
    path("", vista_panel_sustentabilidad, name="panel"),
]
