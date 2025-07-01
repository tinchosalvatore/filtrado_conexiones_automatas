
# Esta funcion es la encargada de realizar la conexion entre la lista de datos validos y la lista de fechas de entrada del Usuario
# Estos ultimos son sus dos parametros de entrada
def match_fechas(lista_fechas, lista_datos_validos):

    # Ejemplo: [{"Usuario": "user1", "MAC_Cliente": "00:1A:2B:3C:4D:5E"}, ...]
    dispositivos = []
    
    # Preprocesamiento: convertir lista_fechas a conjunto para búsquedas más rápidas con set
    fechas_no_laborables = set(lista_fechas)
        
    # Por cada conexion de la lista de datos validados en validar.py        
    for conexion in lista_datos_validos:
        # Consigue el Inicio de la conexion y con .strip lo limpia para evitar errores
        fecha_inicio = conexion.get('Inicio_de_Conexión_Dia', '').strip()   
        
        # Si la fecha de de inicion se encuentra en los dias no laborales
        if fecha_inicio in fechas_no_laborables:
            # Extraemos todos los campos relevantes para mostrarlos en el front
            datos_conexion = {
                "Usuario": conexion.get('Usuario', '').strip(),
                "MAC_Cliente": conexion.get('MAC_Cliente', '').strip(),
                "Inicio_de_Conexión_Dia": fecha_inicio,
                "Hora_de_conexión": conexion.get('Inicio_de_Conexión_Hora', '').strip(),
                "Fin_de_conexión": conexion.get('FIN_de_Conexión_Dia', '').strip(),
                "Hora_fin_de_conexion": conexion.get('FIN_de_Conexión_Hora', '').strip()
            }
            
            # Definimos como variable a los usuarios y las macs para despues poder compararlas y no mostrar repetidas veces el mismo Usuario
            # Esto sucede con los invitado-deca, que es un Usuario otorgado a distintas macs
            usuario = datos_conexion["Usuario"]
            mac = datos_conexion["MAC_Cliente"]

            if usuario and mac:
                # Verificamos si ya existe este usuario + MAC exactos, con lo cual se estarian repitiendo
                existe = any(
                    d["Usuario"] == usuario and d["MAC_Cliente"] == mac
                    for d in dispositivos
                )
                # Si no esta en la lista de dispositivos, lo añade
                if not existe:
                    dispositivos.append(datos_conexion)
    
    # Devuelve la lista de dispositivos para imprimir en el front
    return dispositivos