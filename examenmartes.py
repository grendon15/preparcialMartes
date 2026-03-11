import random
import sys
import time

# ==============================================================================
# ESTRUCTURA DE DATOS GLOBALES
# ==============================================================================

# Lista para almacenar credenciales de acceso (Auth)
# Estructura: {'email': str, 'password': str}
usuarios_auth = []

# Lista para almacenar usuarios del servicio de energía
# Estructura: {'id': int, 'nombre': str, 'documento': str, 'estrato': int, 
#              'consumoEnergetico': list, 'estado': str}
usuarios_servicio = []

# ==============================================================================
# FUNCIONES DE INICIALIZACIÓN Y DATOS
# ==============================================================================

def inicializar_usuarios_servicio():
    """
    Crea los 10 usuarios iniciales con la estructura requerida.
    """
    nombres_base = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Elena", "Pedro", "Sofia", "Diego", "Laura"]
    
    for i in range(10):
        usuario = {
            'id': i + 1,
            'nombre': nombres_base[i],
            'documento': str(1000000000 + i),
            'estrato': random.randint(1, 6),
            # Generamos 5 consumos iniciales aleatorios entre 50 y 300 KWH
            'consumoEnergetico': [random.randint(50, 300) for _ in range(5)],
            'estado': "ACTIVO" if random.random() > 0.2 else "SUSPENDIDO" # 80% probabilidad de activo
        }
        usuarios_servicio.append(usuario)
    
    print(">> Sistema inicializado: 10 usuarios de servicio cargados correctamente.")

# ==============================================================================
# FUNCIONES DE AUTENTICACIÓN (REGISTRO Y LOGIN)
# ==============================================================================

def registrar_usuario():
    """
    Permite crear un nuevo usuario para el acceso al sistema.
    """
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    email = input("Ingrese su correo electrónico: ").strip()
    
    # Validar que el email no exista ya
    for user in usuarios_auth:
        if user['email'] == email:
            print("Error: Este correo ya está registrado.")
            return False

    password = input("Ingrese su contraseña: ").strip()
    
    if not email or not password:
        print("Error: Los campos no pueden estar vacíos.")
        return False

    # Guardar en la lista
    usuarios_auth.append({'email': email, 'password': password})
    print("Registro exitoso. Ahora puede iniciar sesión.")
    return True

def login():
    """
    Gestiona el inicio de sesión con máximo 3 intentos.
    Retorna True si el login es exitoso, False si se bloquea.
    """
    print("\n--- INICIO DE SESIÓN ---")
    intentos_maximos = 3
    intentos_restantes = intentos_maximos

    while intentos_restantes > 0:
        email = input("Correo: ").strip()
        password = input("Contraseña: ").strip()

        # Buscar usuario
        usuario_encontrado = False
        for user in usuarios_auth:
            if user['email'] == email and user['password'] == password:
                usuario_encontrado = True
                break
        
        if usuario_encontrado:
            print("Login exitoso")
            return True
        else:
            intentos_restantes -= 1
            if intentos_restantes > 0:
                print(f"Credenciales incorrectas. Intentos restantes: {intentos_restantes}")
            else:
                print("Cuenta bloqueada temporalmente")
                return False
    
    return False

# ==============================================================================
# FUNCIONES DEL MENÚ DE GESTIÓN DE SERVICIOS
# ==============================================================================

def mostrar_usuarios_servicio():
    """Auxiliar para mostrar la lista de usuarios de forma legible."""
    print(f"\n{'ID':<5} {'Nombre':<15} {'Documento':<12} {'Estrato':<8} {'Estado':<12} {'Consumo Total':<15}")
    print("-" * 70)
    for u in usuarios_servicio:
        total_consumo = sum(u['consumoEnergetico'])
        print(f"{u['id']:<5} {u['nombre']:<15} {u['documento']:<12} {u['estrato']:<8} {u['estado']:<12} {total_consumo:<15} KWH")
    print("-" * 70)

def crear_usuario_servicio():
    """Opción 1 del menú gestión: Crear un nuevo usuario de servicio."""
    print("\n--- CREAR NUEVO USUARIO DE SERVICIO ---")
    try:
        nuevo_id = max([u['id'] for u in usuarios_servicio], default=0) + 1
        nombre = input("Nombre: ").strip()
        documento = input("Documento: ").strip()
        estrato = int(input("Estrato (1-6): "))
        
        if not (1 <= estrato <= 6):
            print("Error: El estrato debe estar entre 1 y 6.")
            return

        # Generar 5 consumos iniciales
        consumos = [random.randint(50, 300) for _ in range(5)]
        
        nuevo_usuario = {
            'id': nuevo_id,
            'nombre': nombre,
            'documento': documento,
            'estrato': estrato,
            'consumoEnergetico': consumos,
            'estado': "ACTIVO"
        }
        
        usuarios_servicio.append(nuevo_usuario)
        print(f"Usuario {nombre} creado exitosamente con ID {nuevo_id}.")
    except ValueError:
        print("Error: Ingrese datos numéricos válidos donde corresponda.")

def ingresar_consumo():
    """Opción 2 del menú gestión: Ingresar consumo aleatorio si está activo."""
    print("\n--- INGRESAR CONSUMO ENERGÉTICO ---")
    try:
        id_buscar = int(input("Ingrese el ID del usuario: "))
        usuario = None
        
        # Buscar usuario
        for u in usuarios_servicio:
            if u['id'] == id_buscar:
                usuario = u
                break
        
        if not usuario:
            print("Error: Usuario no encontrado.")
            return

        if usuario['estado'] != "ACTIVO":
            print(f"Error: El usuario {usuario['nombre']} está {usuario['estado']}. No se puede registrar consumo.")
            return

        # Generar consumo aleatorio
        nuevo_consumo = random.randint(50, 400)
        usuario['consumoEnergetico'].append(nuevo_consumo)
        print(f"Consumo de {nuevo_consumo} KWH registrado exitosamente para {usuario['nombre']}.")
        print(f"Historial de consumos: {usuario['consumoEnergetico']}")
        
    except ValueError:
        print("Error: El ID debe ser un número entero.")

def ordenar_consumo():
    """Opción 3 del menú gestión: Ordenar por consumo total (menor a mayor)."""
    print("\n--- ORDENAR POR CONSUMO TOTAL ---")
    # Ordenamos la lista in-place usando la suma de la lista de consumos como clave
    usuarios_servicio.sort(key=lambda u: sum(u['consumoEnergetico']))
    print("Usuarios ordenados por consumo total (Menor a Mayor):")
    mostrar_usuarios_servicio()

def cambiar_estado():
    """Opción 4 del menú gestión: Cambiar estado ACTIVO/SUSPENDIDO."""
    print("\n--- CAMBIAR ESTADO DE USUARIO ---")
    try:
        id_buscar = int(input("Ingrese el ID del usuario: "))
        usuario = None
        
        for u in usuarios_servicio:
            if u['id'] == id_buscar:
                usuario = u
                break
        
        if not usuario:
            print("Error: Usuario no encontrado.")
            return

        estado_actual = usuario['estado']
        nuevo_estado = "SUSPENDIDO" if estado_actual == "ACTIVO" else "ACTIVO"
        
        confirmacion = input(f"¿Cambiar estado de {estado_actual} a {nuevo_estado}? (s/n): ").lower()
        if confirmacion == 's':
            usuario['estado'] = nuevo_estado
            print(f"Estado actualizado a {nuevo_estado}.")
        else:
            print("Operación cancelada.")
            
    except ValueError:
        print("Error: El ID debe ser un número entero.")

def menu_gestion_servicios():
    """Submenú para gestionar los usuarios del servicio."""
    while True:
        print("\n=== MENÚ GESTIÓN DE USUARIOS DEL SERVICIO ===")
        print("1. Crear usuarios")
        print("2. Ingresar consumos")
        print("3. Ordenar consumo")
        print("4. Cambiar de estado")
        print("5. Volver al menú anterior")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_usuario_servicio()
        elif opcion == '2':
            ingresar_consumo()
        elif opcion == '3':
            ordenar_consumo()
        elif opcion == '4':
            cambiar_estado()
        elif opcion == '5':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# ==============================================================================
# MENÚ PRINCIPAL Y EJECUCIÓN
# ==============================================================================

def menu_principal():
    """Menú principal después del login exitoso."""
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Gestionar usuarios del servicio")
        print("2. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_gestion_servicios()
        elif opcion == '2':
            print("Saliendo del programa. ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida. Intente nuevamente.")

def main():
    """Función principal que orquesta el flujo del programa."""
    print("==============================================")
    print("   SISTEMA DE GESTIÓN ENERGÉTICA - PYTHON   ")
    print("==============================================")
    
    # 1. Inicializar datos de servicio (Los 10 usuarios requeridos)
    inicializar_usuarios_servicio()
    
    # 2. Fase de Autenticación
    # El requerimiento dice: Permita Registro... luego hacer login
    # Para hacerlo funcional, permitimos registrarse hasta que haya al menos uno, luego login.
    
    while len(usuarios_auth) == 0:
        print("\nNo hay usuarios registrados en el sistema.")
        registrar_usuario()
    
    # Permitir registrar más usuarios si se desea antes de loguearse (Opcional, pero buena práctica)
    while True:
        print("\n--- AUTENTICACIÓN ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión (Login)")
        choice = input("Seleccione: ")
        
        if choice == '1':
            registrar_usuario()
        elif choice == '2':
            if login():
                break # Login exitoso, salir del bucle de auth
            else:
                # Login fallido (bloqueado)
                print("Finalizando programa por seguridad.")
                sys.exit()
        else:
            print("Opción inválida.")

    # 3. Fase de Menú Principal
    menu_principal()

if __name__ == "__main__":
    main()