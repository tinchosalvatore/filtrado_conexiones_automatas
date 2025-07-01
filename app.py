from flask import Flask, render_template, request
import pandas as pd
import os
from validar import validar_csv
from match import match_fechas
from calendario import fechas_no_laborables

# Llama app a Flask, creando una instancia de la aplicación
app = Flask(__name__)

# Variable global para almacenar los datos validados, para que en caso de ejecutar nuevamente, no tengamos que validar los datos otra vez
datos_globales = {
    'datos_validados': None,
    'datos_corruptos': None,
    'archivo_origen': None
}

# Ruta principal
@app.route('/', methods=['GET', 'POST'])

# funcion main
def index():

    # Si el metodo es POST significa que se esta subiendo algo, osea, el archivo.csv
    if request.method == 'POST':

        # Le da una variable al archivo.csv y a las fechas ingresadas
        ruta_csv = request.form['ruta_csv']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        
        # Valida que los campos antes mencionados, no estén vacíos
        if not all([ruta_csv, fecha_inicio, fecha_fin]):
            return render_template('index.html', error="Todos los campos son requeridos")
        

        try:
            
        # Verifica si ya se ha validado el archivo,
        # Chequea la existencia del archivo y si es el mismo que se está subiendo nuevamente
            if datos_globales['archivo_origen'] != ruta_csv:
                datos_globales['archivo_origen'] = ruta_csv
                datos_globales['datos_validados'] = None
                

            # Si no se ha validado el archivo, lo valida
            if not datos_globales['datos_validados']:
                
                # Error si la ruta del archivo no existe
                if not os.path.exists(ruta_csv):
                    return render_template('index.html', error="No se encontró el archivo.")
                
                # Error si el archivo no termina en .csv
                if not ruta_csv.lower().endswith('.csv'):
                    return render_template('index.html', error="El archivo debe tener extensión .csv")
                
                # Intenta validar el archivo CSV, en caso de fallar, muestra un mensaje de error
                try:
                    datos_globales['datos_validados'], datos_globales['datos_corruptos'] = validar_csv(ruta_csv)
                
                # Error inesperado
                except Exception as e:   
                    return render_template('index.html', error="Error al validar el archivo")


            # Evalua las fechas ingresadas con la función de las fechas_no_laborables
            lista_fechas = fechas_no_laborables(fecha_inicio, fecha_fin)

            # Evalua las fechas ingresadas con la función match_fechas para buscar coincidencias en conexiones
            dispositivos = match_fechas(lista_fechas, datos_globales['datos_validados'])

            # Exporta el resultado a Excel automáticamente
            df_resultado = pd.DataFrame(dispositivos)
            df_resultado.to_excel('resultado.xlsx', index=False)

            
            # Si no hubo ningun match, muestra un mensaje de error informando que no se encontraron dispositivos
            if not dispositivos:
                return render_template('index.html', error="No se encontraron dispositivos conectados en el rango especificado.")
            
            # Si hubo coincidencias, renderiza la plantilla index.html enviando los dispositivos encontrados y los corruptos
            return render_template('index.html', dispositivos=dispositivos, datos_corruptos=datos_globales['datos_corruptos'])
        
        # Maneja cualquier error inesperado
        except Exception as e:
            return render_template('index.html', error="Ha ocurrido un error, intente nuevamente.")
    
    # Si el método es GET, simplemente renderiza la plantilla index.html (seria la primera vez que se accede)
    return render_template('index.html')


# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)