import mysql.connector
import json

conexion = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="pilk12345",
    database="MundoMultijugador"
)
cursor = conexion.cursor()


cursor.execute("SELECT * FROM jugadores")
for jugador in cursor.fetchall():
    print(jugador)

def crear_jugador(nombre_usuario, nivel, puntuacion, equipo, inventario):
    query = """
    INSERT INTO jugadores (nombre_usuario, nivel, puntuacion, equipo, inventario)
    VALUES (%s, %s, %s, %s, %s)
    """
    datos = (nombre_usuario, nivel, puntuacion, equipo, json.dumps(inventario))
    cursor.execute(query, datos)
    conexion.commit()
    print(f"Jugador '{nombre_usuario}' creado con éxito.")

def consultar_jugadores():
    cursor.execute("SELECT * FROM jugadores")
    for jugador in cursor.fetchall():
        print(jugador)
        
def actualizar_jugador(id_jugador, nuevo_nivel):
    query = "UPDATE jugadores SET nivel = %s WHERE id = %s"
    cursor.execute(query, (nuevo_nivel, id_jugador))
    conexion.commit()

def eliminar_jugador(id_jugador):
    query = "DELETE FROM jugadores WHERE id = %s"
    cursor.execute(query, (id_jugador,))
    conexion.commit()
    

class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_ubicacion(self, ubicacion):
        if ubicacion not in self.nodos:
            self.nodos[ubicacion] = []

    def agregar_ruta(self, desde, hacia, peso):
        self.nodos[desde].append((hacia, peso))

def guardar_grafo_en_db(grafo, nombre_mundo):
    grafo_json = json.dumps(grafo.nodos)
    query = "INSERT INTO mundos (grafo_serializado) VALUES (%s)"
    cursor.execute(query, (grafo_json,))
    conexion.commit()
    

class Nodo:
    def __init__(self, fecha, resultado):
        self.fecha = fecha
        self.resultado = resultado
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo):
        if not self.raiz:
            self.raiz = nodo
        else:
            self._insertar_recursivo(self.raiz, nodo)

    def _insertar_recursivo(self, actual, nodo):
        if nodo.fecha < actual.fecha:
            if actual.izquierda is None:
                actual.izquierda = nodo
            else:
                self._insertar_recursivo(actual.izquierda, nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nodo
            else:
                self._insertar_recursivo(actual.derecha, nodo)

def agregar_item_inventario(id_jugador, item, descripcion):
    cursor.execute("SELECT inventario FROM jugadores WHERE id = %s", (id_jugador,))
    inventario = cursor.fetchone()[0]
    
    if inventario:
        inventario = json.loads(inventario)
    else:
        inventario = {} 

    inventario[item] = descripcion
    query = "UPDATE jugadores SET inventario = %s WHERE id = %s"
    cursor.execute(query, (json.dumps(inventario), id_jugador))
    conexion.commit()
    print(f"Ítem '{item}' añadido al inventario de jugador {id_jugador}.")
    
cursor.execute("CALL actualizar_ranking()")
conexion.commit()
    
equipos = {
    "equipo1": {"jugadores": [], "promedio_puntuacion": 0},
    "equipo2": {"jugadores": [], "promedio_puntuacion": 0},
}

def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar un jugador")
        print("2. Eliminar un jugador")
        print("3. Consultar jugadores")
        print("4. Actualizar jugador")
        print("5. Crear un mundo virtual")
        print("6. Eliminar mundo virtual")
        print("7. Jugar una partida")
        print("8. Consultar ranking")
        print("9. Consultar inventario")
        print("10. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            registrar_jugador()
        elif opcion == "2":
            quitar_jugador()
        elif opcion == "3":
            consultar_jugadores()
        elif opcion == "4":
            actualizar_datos_jugador()
        elif opcion == "5":
            crear_mundo_virtual()
        elif opcion == "6":
            eliminar_mundo()
        elif opcion == "7":
            jugar_partida()
        elif opcion == "8":
            consultar_ranking()
        elif opcion == "9":
            id_jugador = input("ID del jugador para consultar inventario: ")
            consultar_inventario(id_jugador)
        elif opcion == "10":
            print("¡Gracias por jugar!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

def registrar_jugador():
    nombre_usuario = input("Nombre del jugador: ")
    nivel = int(input("Nivel inicial: "))
    puntuacion = int(input("Puntuación inicial: "))
    equipo = input("Equipo: ")
    
    inventario = {}  
    
    while True:
        item = input("Añadir un ítem al inventario (deja vacío para terminar): ")
        if not item:
            break
        descripcion = input(f"Descripción del ítem '{item}': ")
        inventario[item] = descripcion
    
    crear_jugador(nombre_usuario, nivel, puntuacion, equipo, inventario)
    print(f"Jugador '{nombre_usuario}' registrado con éxito.")

def quitar_jugador():
    id_jugador = input("Id del jugador que desea eliminar: ")
    
    cursor.execute("SELECT id FROM jugadores WHERE id = %s", (id_jugador,))
    resultado = cursor.fetchone()
    
    if resultado:
        query = "DELETE FROM jugadores WHERE id = %s"
        cursor.execute(query, (id_jugador,))
        conexion.commit()
    
        eliminar_jugador(id_jugador)
        print(f"Ese jugador fue eliminado con exito.")
    else:
        print("Este usuario no existe")


    
def consultar_jugadores():
    print("\n--- Lista de jugadores ---")
    cursor.execute("SELECT * FROM jugadores")
    for jugador in cursor.fetchall():
        print(jugador)
        
def actualizar_datos_jugador():
    print("\n--- Actualizar datos de un jugador ---")
    id_jugador = input("ID del jugador a actualizar: ")
    
    cursor.execute("SELECT id FROM jugadores WHERE id = %s", (id_jugador,))
    resultado = cursor.fetchone()
    
    if resultado:
        nuevo_nivel = int(input("Nuevo nivel: "))
        actualizar_jugador(id_jugador, nuevo_nivel)
        print(f"Jugador con ID {id_jugador} actualizado con éxito.")
    else:
        print("El jugador con el ID especificado no existe.")

def crear_mundo_virtual():
    print("\n--- Creación de mundo virtual ---")
    nombre_mundo = input("Nombre del mundo: ")
    grafo = Grafo()
    
    
    while True:
        ubicacion = input("Agregar ubicación (deja vacío para terminar): ")
        if not ubicacion:
            break
        grafo.agregar_ubicacion(ubicacion)
    
    
    while True:
        desde = input("Desde (deja vacío para terminar): ")
        if not desde:
            break
        hacia = input("Hacia: ")
        peso = int(input("Peso: "))
        grafo.agregar_ruta(desde, hacia, peso)
    
    
    try:
        query = "INSERT INTO mundos (nombre, grafo_serializado) VALUES (%s, %s)"
        grafo_json = json.dumps(grafo.nodos)
        cursor.execute(query, (nombre_mundo, grafo_json))
        conexion.commit()
        print(f"Mundo '{nombre_mundo}' creado con éxito.")
    except Exception as e:
        print(f"Error al crear el mundo: {e}")

def eliminar_mundo():
    print("\n--- Eliminar un mundo virtual ---")
    nombre_mundo = input("Nombre del mundo a eliminar: ")
    
    try:
        
        cursor.execute("SELECT id FROM mundos WHERE nombre = %s", (nombre_mundo,))
        resultado = cursor.fetchone()
        
        if resultado:
            id_mundo = resultado[0]
            query = "DELETE FROM mundos WHERE id = %s"
            cursor.execute(query, (id_mundo,))
            conexion.commit()
            print(f"Mundo '{nombre_mundo}' eliminado con éxito.")
        else:
            print(f"El mundo '{nombre_mundo}' no existe en la base de datos.")
    except Exception as e:
        print(f"Error al eliminar el mundo: {e}")


def jugar_partida():
    print("\n--- Iniciar una partida ---")
    equipo1 = input("Nombre del Equipo 1: ")
    equipo2 = input("Nombre del Equipo 2: ")
    resultado = input("Resultado (e.g., 'Equipo1 ganó'): ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    
    
    try:
        nodo = Nodo(fecha, resultado)
        if 'arbol' not in globals():
            global arbol
            arbol = ArbolBinario()
        arbol.insertar(nodo)
        
        
        query = "INSERT INTO partidas (fecha, equipo1, equipo2, resultado) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fecha, equipo1, equipo2, resultado))
        conexion.commit()
        print("Partida registrada con éxito.")
    except Exception as e:
        print(f"Error al registrar la partida: {e}")
    
    
        
def consultar_ranking():
    print("\n--- Ranking Global ---")
    cursor.execute("SELECT nombre_usuario, puntuacion FROM jugadores ORDER BY puntuacion DESC")
    ranking = cursor.fetchall()
    
    if ranking:
        for posicion, jugador in enumerate(ranking, 1):
            print(f"Posición {posicion}: {jugador[0]} - Puntuación: {jugador[1]}")
    else:
        print("No hay jugadores registrados.")

def consultar_inventario(id_jugador):
    cursor.execute("SELECT inventario FROM jugadores WHERE id = %s", (id_jugador,))
    inventario = cursor.fetchone()[0]
    
    if inventario:
        inventario = json.loads(inventario)
        print("\n--- Inventario del Jugador ---")
        for item, descripcion in inventario.items():
            print(f"{item}: {descripcion}")
    else:
        print("Este jugador no tiene inventario.")


if __name__ == "__main__":
    menu()
    