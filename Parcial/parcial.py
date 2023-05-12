# Valentin Rodriguez Lloret - División D - Parcial
import csv
import json
import re
import unicodedata
import random
from datetime import datetime 

# Función para cargar los datos desde el archivo CSV
def cargar_personajes() -> tuple:
    with open("Parcial\DBZ.csv", newline='', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=',', quotechar='"') 
        personajes = []
        razas = set()
        habilidades = set()
        for fila in lector_csv:
            id, nombre, raza, poder_pelea, poder_ataque, habilidades_str = fila
            habilidades_list = habilidades_str.split('|$%')
            personajes.append({
                'id': int(id),
                'nombre': nombre,
                'raza': raza,
                'poder_pelea': int(poder_pelea),
                'poder_ataque': int(poder_ataque),
                'habilidades': habilidades_list
            })
            razas.add(raza)
            habilidades.update(habilidades_list)
        return personajes, razas, habilidades

# Funciones para Sanitizar y Normalizar datos

def limpiar_nombre(nombre: str) -> str:

    nombre_limpio = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('utf-8')
    nombre_limpio = re.sub(r'[^\w\s-]', '', nombre_limpio)
    nombre_limpio = nombre_limpio.strip().replace(' ', '_')
    return nombre_limpio

def limpiar_habilidad(habilidad: str) -> str:
    habilidad_limpia = unicodedata.normalize('NFKD', habilidad).encode('ASCII', 'ignore').decode('utf-8')
    habilidad_limpia = re.sub(r'[^\w\s-]', '', habilidad_limpia)
    habilidad_limpia = habilidad_limpia.strip().replace(' ', '_')
    return habilidad_limpia
# Función para listar la cantidad de personajes por raza
def listar_cantidad_por_raza(personajes: list, razas: str) -> str:
    
    print('Cantidad de personajes por raza:')
    for raza in razas:
        cantidad = sum(1 for personaje in personajes if personaje['raza'] == raza)
        print(f'- {raza}: {cantidad}')

# Función para listar los personajes por raza
def listar_personajes_por_raza(personajes: list) -> list:
    
    razas = set([personaje['raza'] for personaje in personajes])

    for raza in razas:
        print(f'{raza.upper()}:')
        if re.search(r"Saiyan", raza):
            personajes_saiyan = [p for p in personajes if re.search(r"Saiyan(-Humano)?", p['raza'])]
            for personaje in personajes_saiyan:
                nombre = personaje['nombre']
                poder_ataque = personaje['poder_ataque']
                print(f'\t- {nombre} ({poder_ataque} de poder de ataque)')
        elif re.search(r"Androide", raza):
            personajes_androide = [p for p in personajes if re.search(r"Androide(-Humano)?", p['raza'])]
            for personaje in personajes_androide:
                nombre = personaje['nombre']
                poder_ataque = personaje['poder_ataque']
                print(f'\t- {nombre} ({poder_ataque} de poder de ataque)')
        else:
            for personaje in personajes:
                if personaje['raza'] == raza:
                    nombre = personaje['nombre']
                    poder_ataque = personaje['poder_ataque']
                    print(f'\t- {nombre} ({poder_ataque} de poder de ataque)')

# Funcion para listar los personajes por habilidad
def listar_personajes_por_habilidad(personajes: list) -> list:
    
    habilidad = input("Ingrese la descripción de la habilidad a buscar: ")
    for personaje in personajes:
        habilidades_personaje = "|$%".join(personaje["habilidades"])
        if re.search(habilidad, habilidades_personaje):
            nombre = personaje["nombre"]
            raza = personaje["raza"]
            poder = (int(personaje["poder_pelea"]) + int(personaje["poder_ataque"])) / 2
            print(f"Nombre: {nombre}, Raza: {raza}, Promedio de poder: {poder}")
        

# Función para el compate


def jugar_batalla(personajes: list) -> None:

    def seleccionar_personaje(personajes: list) -> dict:
        print("Selecciona tu personaje para la batalla:")
        for i, personaje in enumerate(personajes):
            print(f"{i+1}. {personaje['nombre']}")
        while True:
            opcion = input("Ingresa el número correspondiente al personaje: ")
            if opcion.isdigit() and 1 <= int(opcion) <= len(personajes):
                return personajes[int(opcion) - 1]
            else:
                print("Opción inválida. Ingresa un número válido.")

    def seleccionar_personaje_aleatorio(personajes: list) -> dict:
        return random.choice(personajes)

    def guardar_batalla(ganador: dict, perdedor: dict) -> None:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"{fecha_actual} - Ganador: {ganador['nombre']} - Perdedor: {perdedor['nombre']}\n"

        with open("batallas.txt", "a") as archivo:
            archivo.write(registro)

    personaje_usuario = seleccionar_personaje(personajes)
    personaje_maquina = seleccionar_personaje_aleatorio(personajes)

    if personaje_usuario['poder_ataque'] > personaje_maquina['poder_ataque']:
        ganador = personaje_usuario
        perdedor = personaje_maquina
    else:
        ganador = personaje_maquina
        perdedor = personaje_usuario

    guardar_batalla(ganador, perdedor)

    print("¡Batalla concluida!")
    print(f"Ganador: {ganador['nombre']}")
    print(f"Perdedor: {perdedor['nombre']}")


# Función para guardar el JSON
def guardar_personajes_json(personajes: list) -> None:
    
    raza = input("Ingrese la raza: ")
    habilidad = input("Ingrese la habilidad: ")
    
    personajes_filtrados = []
    habilidades_no_buscadas = []

    raza_pattern = re.compile(fr"\b{re.escape(raza)}\b", re.IGNORECASE)
    habilidad_pattern = re.compile(fr"\b{re.escape(habilidad)}\b", re.IGNORECASE)

    for personaje in personajes:
        if raza_pattern.search(personaje['raza']):
            habilidades_personaje = personaje['habilidades']
            if any(habilidad_pattern.search(hab) for hab in habilidades_personaje):
                personajes_filtrados.append(personaje)
            else:
                habilidades_no_buscadas.extend([hab for hab in habilidades_personaje if not habilidad_pattern.search(hab)])

    habilidades_no_buscadas = list(set(habilidades_no_buscadas))

    nombre_archivo = f"{raza.replace(' ', '_')}_{habilidad.replace(' ', '_')}.json"

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        datos_json = {
            "Nombre del archivo": nombre_archivo,
            "Datos": []
        }

        for personaje in personajes_filtrados:
            nombre = personaje['nombre']
            poder_ataque = personaje['poder_ataque']
            habilidades = personaje['habilidades']
            datos_json["Datos"].append({
                "Nombre": nombre,
                "Poder de ataque": poder_ataque,
                "Habilidades": habilidades
            })

        json.dump(datos_json, archivo, indent=4, ensure_ascii=False)

    print(f"Nombre del archivo: {nombre_archivo}")
    print("Datos:")

    for personaje in personajes_filtrados:
        nombre = personaje['nombre']
        poder_ataque = personaje['poder_ataque']
        habilidades = ' + '.join(personaje['habilidades'])
        print(f"{nombre} - {poder_ataque} - {habilidades}")

    print("Habilidades no buscadas:")
    print('\n'.join(habilidades_no_buscadas))


# Función para leer el JSON
def leer_json(nombre_archivo: str) -> None:
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)
            nombre_archivo = datos_json.get("Nombre del archivo")
            datos = datos_json.get("Datos")

            if nombre_archivo is None or datos is None:
                raise ValueError("El archivo JSON no contiene la estructura esperada.")

            print(f"Nombre del archivo: {nombre_archivo}")
            print("Datos:")
            for personaje in datos:
                nombre = personaje.get("Nombre")
                poder_ataque = personaje.get("Poder de ataque")
                habilidades = personaje.get("Habilidades")

                if nombre and poder_ataque and habilidades:
                    habilidades_str = ' + '.join(habilidades)
                    print(f"{nombre} - {poder_ataque} - {habilidades_str}")
                else:
                    raise ValueError("Los datos del personaje están incompletos.")
    except FileNotFoundError:
        print("El archivo JSON no existe.")
    except json.JSONDecodeError:
        print("El archivo JSON está mal formado.")

# Agregar una opción que permita otorgarle un 50% más de poder de pelea y un 70% más de poder de ataque a los Saiyan, y agregaran a sus habilidades la “transformación nivel dios”.
# Guardar en un archivo CSV los personajes que hayan recibido esta actualización.

def actualizar_y_guardar_personajes(personajes):
    personajes_actualizados = []
    for personaje in personajes:
        if personaje["raza"] == "Saiyan":
            personaje["poder_pelea"] *= 1.5
            personaje["poder_ataque"] *= 1.7
            personaje["habilidades"].append("Transformación nivel dios")
            personajes_actualizados.append(personaje)
    
    if personajes_actualizados:
        with open('personajes_actualizados.csv', 'w', newline='') as file:
            fieldnames = ["id", "nombre", "raza", "poder_pelea", "poder_ataque", "habilidades"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(personajes_actualizados)
        
        print("Personajes actualizados guardados en el archivo personajes_actualizados.csv")   

# Menú principal del programa
def menu():
    
    opcion = 0
    while opcion != 8:
        print('--- MENÚ ---')
        print('1. Traer datos desde archivo')
        print('2. Listar cantidad por raza')
        print('3. Listar personajes por raza')
        print('4. Listar personajes por habilidad')
        print('5. Jugar batalla')
        print('6. Guardar Json')
        print('7. Leer Json')
        print('8. Aumentar poderes')
        print('9. Salir del programa')
        opcion = int(input('Ingrese una opción: '))
        match opcion:
            case 1:
                personajes, razas, habilidades = cargar_personajes()
                print('Se cargaron los datos correctamente.')
            case 2:
                listar_cantidad_por_raza(personajes, razas)
            case 3:
                listar_personajes_por_raza(personajes)
            case 4:
                listar_personajes_por_habilidad(personajes)
            case 5:
                jugar_batalla(personajes)
            case 6:
                guardar_personajes_json(personajes)
            case 7:
                nombre_archivo = input("Ingrese el nombre del archivo JSON: ")
                leer_json(nombre_archivo)
            case 8:
                actualizar_y_guardar_personajes(personajes)
            case 9:
                print("¡Adios!")
                break
            case _:
                print("Opcion invalida")

menu()


