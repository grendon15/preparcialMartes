import random

def registrar_empleado(id, nombre, documento, contraseña):
    emplead0={}
    empleado=["id"]=id
    empleado=["nombre"]=nombre
    empleado=["documento"]=documento
    empleado=["contraseña"]=contraseña
    return empleado

def acceder_plataforma(documento, documento_bd, contraseña, constraseña_bd):
    for intento in range (1,4):
        if documento==documento_bd and contraseña==constraseña_bd:
            print("👍 bienvendio")
            return True
        else:
            print("😒 Fallaste, intento {intento}")
    return False

def simular_medicion(numero_medidas, rango_inicial, rango_final):
    mediciones=[]
    for _ in range(numero_medidas):
        medida=random.randint(rango_final, rango_final)
        mediciones.append(medida)
    return mediciones

# def calcular_promedio(mediciones):
#     suma=0
#     for medicion in mediciones:
#         suma+=medicion
#     promedio=suma/len(mediciones)

def calcular_promedio(mediciones):
    return sum(mediciones)/len(mediciones)

def clasificar_medida(promedio):
    if promedio>0 and promedio<=250:
        print("apagar sistema")
    elif promedio>250 and promedio<=400:
        print("todo va super bien")
    elif promedio>400:
        print("alarma")
    else:
        print("revisa tus medidas")
        
        