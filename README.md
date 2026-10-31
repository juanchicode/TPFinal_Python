# TP Final — Programación con Python

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.1.2-green)
![pytest](https://img.shields.io/badge/pytest-9.2.0-success)
![Tests](https://img.shields.io/badge/tests-31-brightgreen)

Trabajo final del curso **Programación con Python**.

- **Docente:** Diego Ariel Simonelli
- **Autor:** Juan Matías Sommaruga

El TP está dividido en tres ejercicios: sanitización y análisis de sensores,
modelado de productos con orientación a objetos, y un panel web de auditoría
de sustentabilidad desarrollado en Django con tests automatizados.

---

## Índice

- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejercicio 1 — Sensores](#ejercicio-1--sensores)
- [Ejercicio 2 — Productos](#ejercicio-2--productos)
- [Ejercicio 3 — Panel web con Django](#ejercicio-3--panel-web-con-django)
- [Tests](#tests)
- [Tecnologías](#tecnologías)

---

## Estructura del proyecto

```
TPFinal_Python/
├── README.md                      # este archivo
├── requirements.txt               # dependencias (Django, pytest, pytest-django)
├── pytest.ini                     # configuración de los tests
├── catalogo_ecotech.json          # archivo que genera el Ejercicio 2
├── ejercicio_1_sensores/
│   ├── sensores.py                # código del Ejercicio 1
│   ├── test_sensores.py           # tests extra del Ejercicio 1
│   └── __init__.py
├── ejercicio_2_productos/
│   ├── productos.py               # código del Ejercicio 2
│   ├── test_productos.py          # tests extra del Ejercicio 2
│   └── __init__.py
└── ejercicio_3_auditoria_web/     # proyecto Django completo
    ├── manage.py
    ├── ecoauditoria/              # configuración del proyecto
    └── sustentabilidad/           # la "app"
        ├── logica.py              # algoritmo de emisiones
        ├── views.py               # la vista del panel
        ├── urls.py
        ├── data/datos_consumo.json
        ├── templates/sustentabilidad/panel.html
        └── tests/                 # tests de emisiones y de la vista
```

---

## Requisitos previos

- Python 3.14 o superior
- pip

---

## Instalación

Clonar el repositorio y crear el entorno virtual:

```bash
git clone https://github.com/juanchicode/TPFinal_Python.git
cd TPFinal_Python

python -m venv .venv
```

Activar el entorno virtual e instalar las dependencias:

**PowerShell (Windows):**

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Bash / Linux / macOS:**

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows también se puede ejecutar todo sin activar el entorno usando
`.\.venv\Scripts\python.exe` en lugar de `python`.

---

## Ejercicio 1 — Sensores

Toma lecturas de sensores "sucias" (con espacios, con unidades pegadas como
`"24.5C"` o `"31,8 °C"`, sin ubicación) y las deja prolijas; después calcula
quién supera un umbral y el promedio general.

### Funciones principales

| Función | Qué hace |
|---|---|
| `limpiar_registro_sensor(registro_raw)` | Devuelve un diccionario limpio: `sensor_id` sin espacios y en mayúsculas (`"sensor-004 "` → `"SENSOR-004"`), `temperatura` como `float` sin unidad, `ubicacion` (o `"No especificada"`). Lanza `ValueError` si la temperatura no es numérica. |
| `generar_resumen_sensores(lista, umbral)` | Devuelve una tupla `(lista_sensores_alerta, promedio_temperatura)`. Con lista vacía devuelve `([], 0.0)`. |

### Ejecutar

```powershell
.\.venv\Scripts\python.exe ejercicio_1_sensores\sensores.py
```

**Salida esperada:** un reporte con 5 sensores, umbral 30 °C, alertas para
SENSOR-002 y SENSOR-005 y el promedio general.

---

## Ejercicio 2 — Productos

Modela el catálogo de productos ecológicos con clases, evita stocks negativos
con una excepción propia y guarda el catálogo en un archivo JSON.

### Conceptos de POO aplicados

| Elemento | Concepto |
|---|---|
| `StockInvalidoError` | Excepción personalizada (hereda de `Exception`) |
| `DispositivoEcológico` | Clase base; el `stock` es una **propiedad** con validación en el setter (**encapsulamiento**) |
| `PanelSolar` | Hereda de la base y reimprime `ficha_tecnica()` (**herencia** y **polimorfismo**) |
| `GestorInventario` | Serializa el catálogo a JSON con `ensure_ascii=False` e `indent=2` |

### Ejecutar

```powershell
.\.venv\Scripts\python.exe ejercicio_2_productos\productos.py
```

**Salida esperada:**

1. Intenta crear un `PanelSolar` con `stock = -5` → captura
   `StockInvalidoError: El stock no puede ser negativo para 'Panel de Prueba': -5`.
2. Imprime las fichas técnicas de los 3 productos.
3. Crea `catalogo_ecotech.json` en la raíz del proyecto.

---

## Ejercicio 3 — Panel web con Django

Proyecto Django **ecoauditoria** con la app **sustentabilidad**: calcula
emisiones de carbono a partir del consumo de energía de varias plantas y las
muestra en un panel web.

### El algoritmo

`calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)` en
`sustentabilidad/logica.py`:

```python
emisiones = consumo_kwh * 0.4
```

Lanza `ValueError` si el consumo es negativo.

### Métricas y vista

- `obtener_metricas_consumo(registros)` devuelve `emisiones_totales`,
  `planta_mayor_consumo` y el `detalle` por planta.
- `vista_panel_sustentabilidad(request)` lee
  `sustentabilidad/data/datos_consumo.json` (10 registros de 4 plantas) y
  renderiza `templates/sustentabilidad/panel.html`.

### Flujo

```
datos_consumo.json
        │
        ▼
cargar_registros_consumo()
        │
        ▼
obtener_metricas_consumo(registros)
        │  (usa calcular_emisiones_carbono por cada registro)
        ▼
vista_panel_sustentabilidad(request)
        │
        ▼
panel.html  →  el navegador
```

### Levantar la web

Verificar que el proyecto esté sano:

```powershell
.\.venv\Scripts\python.exe ejercicio_3_auditoria_web\manage.py check
```

Levantar el servidor de desarrollo:

```powershell
.\.venv\Scripts\python.exe ejercicio_3_auditoria_web\manage.py runserver
```

Abrir <http://127.0.0.1:8000/> para ver un panel con diseño premium (tema
oscuro y glassmorphism):

- 3 tarjetas KPI con iconos SVG animados: emisiones totales, planta de mayor
  consumo y factor de emisión (las cifras hacen un conteo animado)
- tabla con las 4 plantas: barras de consumo relativo, insignia y resaltado
  ámbar para la líder
- fondo de partículas animado con **Three.js** (CDN). Sin internet se ve igual
  el panel: solo se pierde el fondo y la fuente Inter (usa fallback del sistema)
- accesible y responsive: `prefers-reduced-motion` desactiva las animaciones

---

## Tests

El proyecto usa **pytest** con **pytest-django** (configurado en `pytest.ini`).

Correr todos los tests desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Resultado esperado: 31 passed.**

Ver detalle test por test:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Correr los tests por separado:

```powershell
# Solo Ejercicio 1
.\.venv\Scripts\python.exe -m pytest ejercicio_1_sensores -v

# Solo Ejercicio 2
.\.venv\Scripts\python.exe -m pytest ejercicio_2_productos -v

# Solo el algoritmo de emisiones del Ejercicio 3
.\.venv\Scripts\python.exe -m pytest ejercicio_3_auditoria_web\sustentabilidad\tests\test_emisiones.py -v
```

### Cobertura

| Archivo | Qué cubre |
|---|---|
| `ejercicio_1_sensores/test_sensores.py` | Limpieza de registros y resumen de sensores |
| `ejercicio_2_productos/test_productos.py` | Stock negativo/no numérico (`StockInvalidoError`), ficha técnica con polimorfismo, `a_diccionario()` y guardado/lectura del catálogo JSON |
| `sustentabilidad/tests/test_emisiones.py` | Exactitud numérica, factor personalizado, consumo 0, `ValueError` con consumo negativo, métricas y JSON de datos |
| `sustentabilidad/tests/test_vista.py` | La página responde 200, muestra la planta líder y funciona la URL por nombre |

---

## Tecnologías

- [Python](https://www.python.org/) 3.14
- [Django](https://www.djangoproject.com/) 6.1.2
- [pytest](https://pytest.org/) 9.2.0
- [pytest-django](https://pytest-django.readthedocs.io/) 4.14.0

---

## Licencia

Proyecto académico sin fines comerciales.
