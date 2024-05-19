import time
import random
import keyboard
import os

def main():
    finalizar = False
    Mesas = ["x"] * 22  # Creamos una lista de 22 elementos, inicializados con 'x'
    Posicion_1 = 0  # Variable para rastrear la posición del consumidor
    Posicion_2 = 0  # Variable para rastrear la posición del productor
    while not finalizar:
        if keyboard.is_pressed('Esc'):
            break
        Pro_Con = Producto_Consumidor()  # Determina si se va a producir o consumir
        Dado = Cantidad()  # Genera un número aleatorio de elementos a producir o consumir

        if Pro_Con == 0:
            print("Está consumiendo")
            Posicion_1 = Consumir(Mesas, Dado, Posicion_1)  # Realiza la operación de consumo
            if Posicion_1 == len(Mesas):  # Verifica si el consumidor llegó al final de la lista
                Posicion_1 = 0  # Si es así, vuelve al principio de la lista
        else:
            print("Está produciendo")
            Posicion_2 = Producir(Mesas, Dado, Posicion_2)  # Realiza la operación de producción
            if Posicion_2 == len(Mesas):  # Verifica si el productor llegó al final de la lista
                Posicion_2 = 0  # Si es así, vuelve al principio de la lista

        Imprimir_lista(Mesas)  # Imprime el estado actual de la lista de mesas

        print("\n")

        time.sleep(1)  # Espera un segundo antes de la próxima iteración

        os.system("cls")  # Limpia la pantalla antes de la próxima iteración
        if keyboard.is_pressed('Esc'):
            break

def Producto_Consumidor():
    return random.randint(0, 1)  # Retorna 0 para consumir y 1 para producir

def Cantidad():
    return random.randint(3, 6)  # Retorna un número aleatorio de elementos a producir o consumir

def Imprimir_lista(Mesas):
    for x in Mesas:
        if x == 'x':
            print('\033[93m' + x + '\033[0m', end=' ')  # Imprime 'x' en amarillo
        elif x == 'o':
            print('\033[92m' + x + '\033[0m', end=' ')  # Imprime 'o' en verde
        else:
            print(x, end=' ')

def Consumir(Mesas, cantidad, posicion):
    for i in range(posicion, min(posicion + cantidad, len(Mesas))):
        if Mesas[i] == 'x':
            Mesas[i] = 'o'  # Reemplaza 'x' con 'o'
    return min(posicion + cantidad, len(Mesas))  # Retorna la nueva posición del consumidor

def Producir(Mesas, cantidad, posicion):
    for i in range(posicion, min(posicion + cantidad, len(Mesas))):
        if Mesas[i] == 'o':
            Mesas[i] = 'x'  # Reemplaza 'o' con 'x'
    return min(posicion + cantidad, len(Mesas))  # Retorna la nueva posición del productor

main()
