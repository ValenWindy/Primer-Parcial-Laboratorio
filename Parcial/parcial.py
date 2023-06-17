# Valentin Rodriguez Lloret - División D - Parcial
import csv
import json
import re
import unicodedata
import random
from datetime import datetime 

# Variables globales
personajes = []
razas = set()
habilidades = set()

# Función para cargar los datos desde el archivo CSV
def cargar_personajes() -> None:
    global personajes, razas, habilidades
    with open("DBZ.csv", newline='', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo,) 
        personajes = []
        razas = set()
        habilidades = set()
        for fila in lector_csv:
            id, nombre, raza, poder_pelea, poder_ataque, habilidades_str =  fila 
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

# Función para listar la cantidad de personajes por raza y los personajes por raza
def listar_cantidad_y_personajes_por_raza(personajes: list, razas: set) -> None:
    print('Cantidad de personajes por raza:')
    for raza in razas:
        cantidad = sum(1 for personaje in personajes if personaje['raza'] == raza)
        print(f'- {raza}: {cantidad}')
    
    print('\nPersonajes por raza:')
    for raza in razas:
        print(f'{raza.upper()}:')
        personajes_raza = [p for p in personajes if re.search(fr"{raza}(-Humano)?", p['raza'])]
        
        for personaje in personajes_raza:
            nombre = personaje['nombre']
            poder_ataque = personaje['poder_ataque']
            print(f'\t- {nombre} ({poder_ataque} de poder de ataque)')

# Funcion para listar los personajes por habilidad
def listar_personajes_por_habilidad(personajes: list) -> None:
    habilidad = input("Ingrese la descripción de la habilidad a buscar: ")
    
    resultados = []
    
    for personaje in personajes:
        habilidades_personaje = personaje["habilidades"]
        
        if any(habilidad in habilidad_personaje for habilidad_personaje in habilidades_personaje):
            nombre = personaje["nombre"]
            raza = personaje["raza"]
            poder = (int(personaje["poder_pelea"]) + int(personaje["poder_ataque"])) / 2
            resultados.append({"nombre": nombre, "raza": raza, "promedio_poder": poder})
    
    for resultado in resultados:
        print(f"Nombre: {resultado['nombre']}, Raza: {resultado['raza']}, Promedio de poder: {resultado['promedio_poder']}")
        
# Función para el combate
def combate_personajes(personajes: list) -> None:

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
    raza = input("Ingrese la raza: ").lower()
    habilidad = input("Ingrese la habilidad: ").lower()

    personajes_filtrados = []
    habilidades_no_buscadas = set()

    for personaje in personajes:
        if raza in personaje['raza'].lower():
            habilidades_personaje = [hab.lower() for hab in personaje['habilidades']]
            if any(habilidad in habilidades_personaje for habilidad in habilidades_personaje):
                habilidades_personaje = [hab for hab in habilidades_personaje if habilidad not in hab]
                personajes_filtrados.append({
                    "Nombre": personaje['nombre'],
                    "Poder de ataque": personaje['poder_ataque'],
                    "Habilidades": habilidades_personaje
                })
            else:
                habilidades_no_buscadas.update(personaje['habilidades'])

    habilidades_no_buscadas = list(habilidades_no_buscadas)

    if len(personajes_filtrados) == 0:
        print("No se encontraron personajes que cumplan con los criterios de búsqueda.")
        return

    nombre_archivo = f"{limpiar_nombre(raza)}_{limpiar_habilidad(habilidad)}.json"

    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        datos_json = {
            "Nombre del archivo": nombre_archivo,
            "Datos": personajes_filtrados
        }
        json.dump(datos_json, archivo, indent=4, ensure_ascii=False)

    print(f"Nombre del archivo: {nombre_archivo}")
    print("Datos:")

    for personaje in personajes_filtrados:
        nombre = personaje['Nombre']
        poder_ataque = personaje['Poder de ataque']
        habilidades = ' + '.join(personaje['Habilidades'])
        print(f"{nombre} - {poder_ataque} - {habilidades}")

    print("Habilidades no buscadas:")
    print('\n'.join(habilidades_no_buscadas))

# Función para leer el JSON

def leer_json(nombre_archivo: str) -> None:
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        try:
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

                if nombre is None or poder_ataque is None or habilidades is None:
                    raise ValueError("Los datos del personaje están incompletos.")

                habilidades_str = ' + '.join(habilidades)
                print(f"{nombre} - {poder_ataque} - {habilidades_str}")

        except FileNotFoundError:
            print("El archivo JSON no existe.")
        except json.JSONDecodeError:
            print("El archivo JSON está mal formado.")


# Funcion para Actualizar los Saiyan
def actualizar_saiyan(personajes):
    personajes_actualizados = [
        {
            "id": personaje["id"],
            "nombre": personaje["nombre"],
            "raza": personaje["raza"],
            "poder_pelea": personaje["poder_pelea"] * 1.5,
            "poder_ataque": personaje["poder_ataque"] * 1.7,
            "habilidades": personaje["habilidades"] + ["Transformación nivel dios"]
        }
        for personaje in personajes
        if personaje["raza"] == "Saiyan"
    ]
    
    if personajes_actualizados:
        with open('personajes_actualizados.csv','w',encoding="utf-8") as file:
            fieldnames = ["id", "nombre", "raza", "poder_pelea", "poder_ataque", "habilidades"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(personajes_actualizados)
        
        print("Personajes actualizados guardados en el archivo personajes_actualizados.csv")

# Función para ordenar personajes por atributo

def ordenar_personajes_por_atributo(atributo, orden):
    lista_ordenada = sorted(personajes, key=lambda x: sorted(list(x[atributo])) if isinstance(x[atributo], set) else x[atributo], reverse=not orden)
    for personaje in lista_ordenada:
        print(f"- Nombre: {personaje['nombre']}")
        print(f"  Raza: {personaje['raza']}")
        print(f"  Poder de pelea: {personaje['poder_pelea']}")
        print(f"  Poder de ataque: {personaje['poder_ataque']}")
        print(f"  Habilidades: {', '.join(personaje['habilidades'])}")
        print()  # Salto de línea entre personajes
    return lista_ordenada


# Función para generar código Pokemón

def generar_codigo_pokemon(personajes: list) -> str:
    def seleccionar_personaje_pokemon(personajes: list) -> dict:
        print("Selecciona tu personaje:")
        for i, personaje in enumerate(personajes):
            print(f"{i+1}. {personaje['nombre']}")
        while True:
            opcion = input("Ingresa el número correspondiente al personaje: ")
            if opcion.isdigit() and 1 <= int(opcion) <= len(personajes):
                return personajes[int(opcion) - 1]
            else:
                print("Opción inválida. Ingresa un número válido.")
                
    personaje = seleccionar_personaje_pokemon(personajes)
    
    nombre = personaje["nombre"]
    poder_pelea = personaje["poder_pelea"]
    poder_ataque = personaje["poder_ataque"]
    id_personaje = str(personaje["id"]).zfill(9)

    inicial_nombre = nombre[0].upper()
    if poder_pelea > poder_ataque:
        ganador = "A"
    elif poder_ataque > poder_pelea:
        ganador = "D"
    else:
        ganador = "AD"

    valor_mas_alto = max(poder_ataque, poder_pelea)

    codigo_pokemon = f"{inicial_nombre}-{ganador}-{valor_mas_alto}-{id_personaje}"
    print("¡Has generado tu código Pokémon!")
    print(codigo_pokemon)
# Menú principal del programa
def menu():
    cargar_personajes()
    print('¡Bienvenido al menu de Dragon Ball Z!')
    opcion = 0
    while opcion != 9:
        print('--- MENÚ ---')
        print('1. Listar cantidad y personajes por raza')
        print('2. Listar personajes por habilidad')
        print('3. Jugar batalla')
        print('4. Guardar Json')
        print('5. Leer Json')
        print('6. Aumentar poderes')
        print('7. Ordenar personajes por Atributo')
        print('8. Generar el Código Pokemon')
        print('9. Salir del programa')
        opcion = int(input('Ingrese una opción: '))
        match opcion:
            case 1:
                listar_cantidad_y_personajes_por_raza(personajes, razas)
            case 2:
                listar_personajes_por_habilidad(personajes)
            case 3:
                combate_personajes(personajes)
            case 4:
                guardar_personajes_json(personajes)
            case 5:
                nombre_archivo = input("Ingrese el nombre del archivo JSON: ")
                leer_json(nombre_archivo)
            case 6:
                actualizar_saiyan(personajes)
            case 7:
                atributo = input("Ingrese el nombre del atributo: ")
                orden = True  
                ordenar_personajes_por_atributo(atributo, orden)
            case 8:
                generar_codigo_pokemon(personajes)
            case 9:
                print("¡Adios!")
                break
            case _:
                print("Opcion invalida")

menu()


