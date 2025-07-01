import csv
import re

# Este diccionario contiene la expresión regular para validar cada columna del CSV
# Las claves corresponden al nombre exacto de cada columna en el archivo CSV, son necesarias para interactuar con los datos del csv
regex_validaciones = {
    'ID': r'^\d+$',  # Número entero positivo
    'ID_Sesion': r'^[A-F0-9]{8}-[A-F0-9]{8}$',  # Formato hexadecimal con guión, como UUID parcial
    'ID_Conexión_unico': r'^[a-f0-9]+$',  # Hexadecimal simple, sin guiones
    'Usuario': r'^[a-zA-Z0-9\-]+$',  # Alfanumérico con guiones (ej. invitado-deca)
    'IP_NAS_AP': r'^(\d{1,3}\.){3}\d{1,3}$',  # Dirección IP v4 (ej. 192.168.0.1)
    'Tipo__conexión': r'^[a-zA-Z0-9\-\.]+$',  # Texto como "wireless-802.11"
    'Inicio_de_Conexión_Dia': r'^\d{4}-\d{2}-\d{2}$',  # Fecha en formato YYYY-MM-DD
    'Inicio_de_Conexión_Hora': r'^\d{2}:\d{2}:\d{2}$',  # Hora en formato HH:MM:SS
    'FIN_de_Conexión_Dia': r'^\d{4}-\d{2}-\d{2}$', # Fecha en formato YYYY-MM-DD
    'FIN_de_Conexión_Hora': r'^\d{2}:\d{2}:\d{2}$', # Hora en formato HH:MM:SS
    'Session_Time': r'^\d+$',  # Número entero (segundos)
    'Input_Octects': r'^\d+$', # Número entero
    'Output_Octects': r'^\d+$', # Número entero
    'MAC_AP': r'^([A-Fa-f0-9]{2}[-:]){5}[A-Fa-f0-9]{2}(:[A-Z0-9]{4})?$',  # Dirección MAC con "-" o ":"
    'MAC_Cliente': r'^([A-Fa-f0-9]{2}[-:]){5}[A-Fa-f0-9]{2}$',
    'Razon_de_Terminación_de_Sesión': r'^[a-zA-Z\s\-]+$',  # Letras, espacios y guiones (ej. "User-Request")  \s permite espacios
}

# La llamamos abajo para validar cada fila del CSV, retorna True si es válida, False si no lo es
def validar_fila(fila):

    for campo, regex in regex_validaciones.items():
        valor = fila.get(campo, '').strip()  # Obtener y limpiar 
        if not re.match(regex, valor):  # La funcion match, incluida en re, Valida las filas con la expresión regular designada a cada una
            return False  # Si no cumple el patrón, devuelve False

    # Lógica extra: verifica el rango de los octetos de las IPs 0-255
    try:
        octetos = fila['IP_NAS_AP'].split('.')  #Este split separa la ip cada vez que hay un punto

        if any(int(o) < 0 or int(o) > 255 for o in octetos):  # Se verifica si son menores a 0 o mayores a 255
            return False   # Si la IP es invalida
    except:
        return False  

    return True  # Si pasa todas las validaciones, se considera una fila válida


# Valida el csv entero, llamando a la funcion de validar_filas() 
def validar_csv(csv_entrada):
   
    lista_datos_validos = []
    lista_datos_corruptos = []

    # Abrimos el archivo de entrada usando el módulo csv y lo renombramos entrada
    with open(csv_entrada, newline='', encoding='utf-8') as entrada:
        lector = csv.DictReader(entrada)  # El lector interpreta a cada fila como un diccionario
        
        # En campos usando fieldnames, obtenemos los nombres de las columnas para que los use el diccionario regex
        campos = lector.fieldnames  
            
        # Procesamos fila por fila
        for fila in lector:
            if validar_fila(fila) == True:  # Fila válida
                # Creamos un nuevo diccionario para la fila válida
                fila_valida = {campo: fila[campo] for campo in campos}      
                lista_datos_validos.append(fila_valida)
                
            elif validar_fila(fila) == False:
                # idem, pero para las filas inválidas
                fila_invalida = {campo: fila[campo] for campo in campos}
                lista_datos_corruptos.append(fila_invalida)

    # Por ultimo la funcion devuelve ambas listas para ser utilizadas en match.py
    return lista_datos_validos, lista_datos_corruptos