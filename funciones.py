import random
import os

# Base de datos simulada para el Login (usuario y contraseña)
# En un caso real, esto estaría en una base de datos segura.
credenciales_validas = {
    "admin@ejemplo.com": "password123"
}

# Lista principal donde se almacenarán los usuarios del servicio
usuarios_servicio = []

# --- Funciones del Sistema (Login) ---

def login():
    """Maneja el proceso de autenticación con hasta 3 intentos."""
    intentos = 3
    while intentos > 0:
        print("\n" + "="*40)
        print("       INICIO DE SESIÓN")
        print("="*40)
        correo = input("Correo electrónico: ")
        contraseña = input("Contraseña: ")

        # Validación de credenciales
        if correo in credenciales_validas and credenciales_validas[correo] == contraseña:
            print("\n¡Login exitoso! Bienvenido a la plataforma.")
            return True
        else:
            intentos -= 1
            if intentos > 0:
                print(f"\n⚠️ Credenciales incorrectas. Intentos restantes: {intentos}")
            else:
                print("\n❌ Demasiados intentos fallidos. Acceso bloqueado.")
                return False
    return False

# --- Funciones de Gestión de Usuarios (Lógica de Negocio) ---

def generar_consumos_aleatorios():
    """Genera una lista de 30 consumos energéticos aleatorios (KWH)."""
    # Simula el consumo de 30 días de un mes
    return [round(random.uniform(5.0, 30.0), 2) for _ in range(30)]

def crear_usuario():
    """Solicita los datos al usuario y añade un nuevo usuario a la lista."""
    print("\n--- Crear Nuevo Usuario ---")
    try:
        # Generar ID automático (siguiente número)
        nuevo_id = len(usuarios_servicio) + 1

        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return

        documento = input("Número de documento: ").strip()
        if not documento:
            print("Error: El documento no puede estar vacío.")
            return

        # Validación de estrato (1-6)
        try:
            estrato = int(input("Estrato (1-6): "))
            if estrato not in range(1, 7):
                print("Error: El estrato debe estar entre 1 y 6.")
                return
        except ValueError:
            print("Error: Debes ingresar un número entero.")
            return

        # Lista de consumos inicialmente vacía
        consumo_inicial = []

        # Estado por defecto (ACTIVO)
        estado = "ACTIVO"

        # Crear el diccionario del usuario
        nuevo_usuario = {
            "id": nuevo_id,
            "nombre": nombre,
            "documento": documento,
            "estrato": estrato,
            "consumoEnergetico": consumo_inicial,
            "estado": estado
        }

        usuarios_servicio.append(nuevo_usuario)
        print(f"✅ Usuario '{nombre}' creado exitosamente con ID {nuevo_id}.")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def editar_estado_usuario():
    """Cambia el estado de un usuario (ACTIVO/SUSPENDIDO) buscándolo por ID."""
    print("\n--- Editar Estado de Usuario ---")
    if not usuarios_servicio:
        print("No hay usuarios registrados.")
        return

    try:
        # Mostrar lista rápida para referencia
        print("Usuarios disponibles:")
        for user in usuarios_servicio:
            print(f"  ID: {user['id']} - {user['nombre']} (Estado actual: {user['estado']})")

        id_usuario = int(input("\nIngresa el ID del usuario a modificar: "))

        # Buscar usuario por ID
        usuario_encontrado = None
        for usuario in usuarios_servicio:
            if usuario["id"] == id_usuario:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            print(f"Usuario encontrado: {usuario_encontrado['nombre']} - Estado actual: {usuario_encontrado['estado']}")
            nuevo_estado = input("Ingresa el nuevo estado (ACTIVO/SUSPENDIDO): ").strip().upper()
            if nuevo_estado in ["ACTIVO", "SUSPENDIDO"]:
                usuario_encontrado["estado"] = nuevo_estado
                print(f"✅ Estado actualizado a '{nuevo_estado}'.")
            else:
                print("Error: Estado no válido. Debe ser ACTIVO o SUSPENDIDO.")
        else:
            print(f"Error: No se encontró un usuario con ID {id_usuario}.")

    except ValueError:
        print("Error: Debes ingresar un número de ID válido.")

def ingresar_consumos():
    """Asigna una lista aleatoria de 30 consumos a un usuario específico."""
    print("\n--- Ingresar Consumos Energéticos ---")
    if not usuarios_servicio:
        print("No hay usuarios registrados.")
        return

    try:
        print("Usuarios disponibles:")
        for user in usuarios_servicio:
            # Indicar si ya tiene consumos registrados
            tiene_consumos = "Sí" if user['consumoEnergetico'] else "No"
            print(f"  ID: {user['id']} - {user['nombre']} (¿Tiene consumos?: {tiene_consumos})")

        id_usuario = int(input("\nIngresa el ID del usuario para cargar consumos: "))

        for usuario in usuarios_servicio:
            if usuario["id"] == id_usuario:
                # Generar nuevos consumos aleatorios
                usuario["consumoEnergetico"] = generar_consumos_aleatorios()
                print(f"✅ Se han generado 30 consumos aleatorios para {usuario['nombre']}.")
                # Mostrar una pequeña muestra
                print(f"   Muestra: {usuario['consumoEnergetico'][:5]}... (KWH)")
                return

        print(f"Error: No se encontró un usuario con ID {id_usuario}.")

    except ValueError:
        print("Error: Debes ingresar un número de ID válido.")

def ordenar_por_consumo():
    """Ordena la lista de usuarios por su consumo total (menor a mayor)."""
    print("\n--- Ordenar Usuarios por Consumo (Menor a Mayor) ---")
    if not usuarios_servicio:
        print("No hay usuarios para ordenar.")
        return

    # Verificar que los usuarios tengan consumos para poder ordenarlos
    usuarios_sin_consumo = [u for u in usuarios_servicio if not u['consumoEnergetico']]
    if usuarios_sin_consumo:
        print("⚠️  Nota: Hay usuarios sin consumos registrados. Se considerará su consumo como 0 KWH.")

    # Crear una copia ordenada para no perder la referencia (o podemos modificar la original)
    # Vamos a modificar la original con .sort()
    try:
        # Ordenar in-place usando una función lambda que calcula el consumo total
        usuarios_servicio.sort(key=lambda usuario: sum(usuario['consumoEnergetico']) if usuario['consumoEnergetico'] else 0)

        print("✅ Usuarios ordenados por consumo total (menor a mayor):")
        print("-" * 70)
        print(f"{'ID':<5} {'Nombre':<20} {'Total Consumo (KWH)':<20} {'Estado':<12}")
        print("-" * 70)
        for usuario in usuarios_servicio:
            total_consumo = sum(usuario['consumoEnergetico']) if usuario['consumoEnergetico'] else 0
            print(f"{usuario['id']:<5} {usuario['nombre']:<20} {total_consumo:<20.2f} {usuario['estado']:<12}")
        print("-" * 70)

    except Exception as e:
        print(f"Error al ordenar: {e}")

def mostrar_usuarios():
    """Función auxiliar para visualizar todos los usuarios y sus datos."""
    if not usuarios_servicio:
        print("No hay usuarios registrados.")
        return

    print("\n--- Lista de Usuarios del Servicio ---")
    print("="*100)
    for usuario in usuarios_servicio:
        total_consumo = sum(usuario['consumoEnergetico']) if usuario['consumoEnergetico'] else 0
        print(f"ID: {usuario['id']}")
        print(f"  Nombre: {usuario['nombre']}")
        print(f"  Documento: {usuario['documento']}")
        print(f"  Estrato: {usuario['estrato']}")
        print(f"  Estado: {usuario['estado']}")
        print(f"  Consumo Total: {total_consumo:.2f} KWH")
        if usuario['consumoEnergetico']:
            print(f"  Consumos (primeros 5): {usuario['consumoEnergetico'][:5]}")
        else:
            print("  Consumos: No registrados")
        print("-" * 40)

# --- Menús de la Aplicación ---

def menu_gestion_usuarios():
    """Submenú para la gestión de los usuarios del servicio."""
    while True:
        print("\n" + "="*50)
        print("       MENÚ DE GESTIÓN DE USUARIOS")
        print("="*50)
        print("1. Crear nuevo usuario")
        print("2. Editar estado de usuario")
        print("3. Ingresar consumos a usuario")
        print("4. Ordenar usuarios por consumo (menor a mayor)")
        print("5. Mostrar lista de usuarios")
        print("6. Volver al menú principal")
        print("="*50)

        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            editar_estado_usuario()
        elif opcion == "3":
            ingresar_consumos()
        elif opcion == "4":
            ordenar_por_consumo()
        elif opcion == "5":
            mostrar_usuarios()
        elif opcion == "6":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def menu_principal():
    """Menú principal de la aplicación."""
    while True:
        print("\n" + "="*40)
        print("       SISTEMA DE GESTIÓN ENERGÉTICA")
        print("="*40)
        print("1. Gestionar usuarios del servicio")
        print("2. Salir")
        print("="*40)

        opcion = input("Selecciona una opción (1-2): ").strip()

        if opcion == "1":
            menu_gestion_usuarios()
        elif opcion == "2":
            print("👋 Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

# --- Punto de entrada principal ---
if __name__ == "__main__":
    print("🌟 Bienvenido a la Herramienta de Gestión de Consumos Energéticos 🌟")

    # Iniciar proceso de login
    if login():
        # Si el login es exitoso, mostrar el menú principal
        menu_principal()
    else:
        print("Programa terminado.")