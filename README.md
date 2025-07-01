# 📊 Análisis de Conexiones en Días No Laborables


Aplicación web en Flask que analiza conexiones de dispositivos en fechas no laborables a partir de archivos CSV.


## 🚀 Características principales


- **Validación inteligente de CSV**: Detecta y filtra datos corruptos usando expresiones regulares
- **Gestión de fechas**: Genera automáticamente listas de días feriados/no laborables
- **Optimización de procesos**: Cacheo inteligente de archivos ya procesados
- **Interfaz intuitiva**: Formulario simple con resultados en tabla ordenada


## 📦 Dependencias


El proyecto usa las siguientes dependencias (especificadas en `requirements.txt`):


## 🔧 Instalación
Clona el repositorio:


```bash
git clone https://github.com/francozapata05/tp5_automatas.git
cd tp5_automatas
```


## Crea y activa un entorno virtual (recomendado):


```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
## Instalar requerimientos
```bash
pip install -r requirements.txt
```


## 🖥️ Uso
Inicia la aplicación:

```bash
flask run
```


## Accede desde tu navegador:
```bash
http://localhost:5000
```


## Parámetros del formulario:
```text
Ruta CSV: Ruta absoluta o relativa al archivo CSV
Fecha inicio: Fecha inicial del análisis (formato YYYY-MM-DD)
Fecha fin: Fecha final del análisis (formato YYYY-MM-DD)
```
