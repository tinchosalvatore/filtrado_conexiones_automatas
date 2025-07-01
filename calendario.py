from datetime import datetime, timedelta


# Lista de Feriados que su cumplen siempre
feriados = [
    "01-01",  # 1 de enero - Año Nuevo
    "03-24",  # 24 de marzo - Día Nacional de la Memoria por la Verdad y la Justicia
    "04-02",  # 2 de abril - Día del Veterano y de los Caídos en la Guerra de Malvinas
    "05-01",  # 1 de mayo - Día del Trabajador
    "05-25",  # 25 de mayo - Día de la Revolución de Mayo
    "07-09",  # 9 de julio - Día de la Independencia
    "12-08",  # 8 de diciembre - Día de la Inmaculada Concepción de María
    "12-25",  # 25 de diciembre - Navidad
]

# fecha_inicio_str y fecha_fin_str son indicados por el Usuairo desde el front, y gestionados por esta funcion en el Back
def fechas_no_laborables(fecha_inicio_str, fecha_fin_str):
    
    #Convierte a string las fechas ingresadas por el Usuairo
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()    
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

    # Separa el año de las fechas ingresadas por el usuario
    años = {fecha_inicio.year, fecha_fin.year}     
    
    feriados_convertidos = []        

    # Agrega el año a los feriados que se cumplen siempre
    for año in años:
        feriados_convertidos.extend(        # Con extend agrega datos a la lista
            datetime.strptime(f"{año}-{f}", "%Y-%m-%d").date()      # Con esto añade a la string de la fecha, el año actual que esta siendo evaluado
            for f in feriados   #Lo hace en todos los feriados de la lista de feriados
        )

    fecha_actual = fecha_inicio     # cambiamos el nombre de la variable para evitar problemas
    
    no_laborables = []      # Esta es la lista que va a devolver la funcion

    # Mientras que la fecha de inicio sea menor que la final
    while fecha_actual <= fecha_fin:
    
    # La función weekday() del módulo datetime da un valor numérico a los días de la semana: 0 a 6
    # Si es sábado o domingo (>=5) o está en la lista de feriados, se agrega a la lista de no laborables.
        if fecha_actual.weekday() >= 5 or fecha_actual in feriados_convertidos:     
            no_laborables.append(fecha_actual.strftime("%Y-%m-%d")) 
        fecha_actual += timedelta(days=1)       # Avanza el dia

    # Por ultimo devuelve la lista de los dias no laborales para ser utilizada en match.py 
    return no_laborables