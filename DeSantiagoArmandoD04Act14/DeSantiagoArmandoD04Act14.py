import random
import time
import keyboard
import os

# Definición de estados
ESTADOS = {
    "Nuevo": "N",
    "Listo": "L",
    "Ejecución": "E",
    "Bloqueado": "B",
    "Terminado": "T"
}

# Definición de clases
class Proceso:
    def __init__(self, numero_programa, tiempo_maximo_estimado, operacion, dato1, dato2, tamaño):
        self.numero_programa = numero_programa
        self.tiempo_maximo_estimado = tiempo_maximo_estimado
        self.operacion = operacion
        self.dato1 = dato1
        self.dato2 = dato2
        self.tamaño = tamaño
        self.tiempo_llegada = None
        self.tiempo_finalizacion = None
        self.tiempo_retorno = None
        self.tiempo_respuesta = None
        self.tiempo_espera = 0
        self.tiempo_servicio = 0
        self.estado = ESTADOS["Nuevo"]
        self.resultado = None
        self.tiempo_restante_cpu = self.tiempo_maximo_estimado
        self.paginas = self.calcular_paginas()

    def calcular_paginas(self):
        num_paginas = self.tamaño // 5
        if self.tamaño % 5 != 0:
            num_paginas += 1
        return num_paginas

    def realizar_operacion(self):
        if self.operacion == "+":
            self.resultado = self.dato1 + self.dato2
        elif self.operacion == "-":
            self.resultado = self.dato1 - self.dato2
        elif self.operacion == "*":
            self.resultado = self.dato1 * self.dato2
        elif self.operacion == "/":
            if self.dato2 == 0:
                raise ZeroDivisionError("División por cero")
            else:
                self.resultado = self.dato1 / self.dato2
        else:
            raise ValueError("Operación inválida")

    def actualizar_tiempo(self, tiempo, tiempo_actual):
        if self.estado == ESTADOS["Ejecución"]:
            if self.tiempo_llegada is None:
                self.tiempo_llegada = tiempo_actual
            self.tiempo_servicio += tiempo
            self.tiempo_restante_cpu -= tiempo
        elif self.estado == ESTADOS["Bloqueado"]:
            if self.tiempo_llegada is None:
                self.tiempo_llegada = tiempo_actual
            self.tiempo_espera += tiempo

    def calcular_tiempos(self, tiempo_actual):
        if self.tiempo_finalizacion is not None:
            if self.tiempo_llegada is not None:
                self.tiempo_retorno = self.tiempo_finalizacion - self.tiempo_llegada
            else:
                # Si tiempo_llegada no está definido, se establece como 0
                self.tiempo_retorno = self.tiempo_finalizacion
            self.tiempo_respuesta = self.tiempo_servicio if self.estado == ESTADOS["Terminado"] else (tiempo_actual - self.tiempo_llegada)

# Funciones auxiliares
def generar_proceso(numero_anterior):
    numero_programa = numero_anterior + 1
    tiempo_maximo_estimado = random.randint(5, 18)
    operacion = random.choice("+-/%")
    dato1 = random.randint(1, 100)
    dato2 = random.randint(1, 100)
    tamaño = random.randint(6, 26)
    return Proceso(numero_programa, tiempo_maximo_estimado, operacion, dato1, dato2, tamaño)

def mostrar_procesos_en_estado(estado, procesos):
    print(f"\n{estado}:")
    for proceso in procesos:
        if proceso.estado == estado:
            print(f"- Número de Programa: {proceso.numero_programa}")
            print(f"- Tamaño: {proceso.tamaño}")
            print(f"- Tiempo Máximo Estimado: {proceso.tiempo_maximo_estimado}")
            if estado == ESTADOS["Bloqueado"]:
                print(f"- Tiempo Transcurrido Bloqueado: {proceso.tiempo_espera}")
            else:
                print(f"- Tiempo Restante CPU: {proceso.tiempo_restante_cpu}")

def mostrar_proceso_en_ejecucion(proceso, tiempo_transcurrido_quantum):
    print("\nProceso en Ejecución:")
    print(f"- Número de Programa: {proceso.numero_programa}")
    print(f"- Tamaño: {proceso.tamaño}")
    print(f"- Tiempo Máximo Estimado: {proceso.tiempo_maximo_estimado}")
    print(f"- Operación: {proceso.operacion} {proceso.dato1} {proceso.operacion} {proceso.dato2}")
    print(f"- Tiempo Transcurrido en Ejecución: {proceso.tiempo_servicio}")
    print(f"- Tiempo Restante por Ejecutar: {proceso.tiempo_restante_cpu}")
    print(f"- Tiempo Transcurrido del Quantum: {tiempo_transcurrido_quantum}")

def mostrar_cola_de_bloqueados(cola_de_bloqueados):
    print("\nCola de Bloqueados:")
    for proceso in cola_de_bloqueados:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Tiempo Transcurrido en Bloqueado: {proceso.tiempo_espera}")

def mostrar_procesos_terminados(procesos_terminados):
    print("\nProcesos Terminados:")
    for proceso in procesos_terminados:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Operación: {proceso.operacion} {proceso.dato1} {proceso.operacion} {proceso.dato2}")
        if proceso.resultado is not None:
            print(f"- Resultado: {proceso.resultado}")
        else:
            print("- Estado: ERROR")

def mostrar_reloj(tiempo_transcurrido):
    print(f"\nReloj: Tiempo total transcurrido: {tiempo_transcurrido}")

def mostrar_memoria(memoria):
    print("\nEstado de la Memoria:")
    for i, marco in enumerate(memoria):
        if marco == "SO":
            print(f"Marco {i}: Sistema Operativo")
        elif marco == "Libre":
            print(f"Marco {i}: Libre")
        else:
            print(f"Marco {i}: Proceso {marco}")

def mostrar_tabla_procesos(procesos_listos, procesos_nuevos, cola_de_bloqueados, procesos_terminados):
    print("\nTabla de Procesos:")
    print("Procesos Nuevos:")
    for proceso in procesos_nuevos:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Tamaño: {proceso.tamaño}")
        print(f"- Tiempo Máximo Estimado: {proceso.tiempo_maximo_estimado}")
    print("Procesos Listos:")
    for proceso in procesos_listos:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Tamaño: {proceso.tamaño}")
        print(f"- Tiempo Máximo Estimado: {proceso.tiempo_maximo_estimado}")
    print("Cola de Bloqueados:")
    for proceso in cola_de_bloqueados:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Tiempo Transcurrido en Bloqueado: {proceso.tiempo_espera}")
    print("Procesos Terminados:")
    for proceso in procesos_terminados:
        print(f"- Número de Programa: {proceso.numero_programa}")
        print(f"- Operación: {proceso.operacion} {proceso.dato1} {proceso.operacion} {proceso.dato2}")
        if proceso.resultado is not None:
            print(f"- Resultado: {proceso.resultado}")
        else:
            print("- Estado: ERROR")

def mostrar_tabla_paginas(memoria):
    print("\nTabla de Páginas:")
    for i, marco in enumerate(memoria):
        if marco == "SO":
            print(f"Marco {i}: Sistema Operativo")
        elif marco == "Libre":
            print(f"Marco {i}: Libre")
        else:
            print(f"Marco {i}: Proceso {marco}")

# Inicialización de variables
num_procesos = int(input("Ingrese el número de procesos a crear: "))
procesos_nuevos = []
procesos_listos = []
cola_de_bloqueados = []
procesos_terminados = []
memoria = ["Libre"] * 46
tiempo_global = 0
quantum = 3
numero_anterior = 0  # Para generar números de programa únicos

while True:
    # Generar nuevos procesos si es necesario
    while len(procesos_nuevos) < num_procesos:
        nuevo_proceso = generar_proceso(numero_anterior)
        procesos_nuevos.append(nuevo_proceso)
        numero_anterior += 1

    # Actualizar estado de la memoria, procesos y tiempo global
    # Admitir procesos en memoria si hay suficiente espacio
    for proceso in procesos_nuevos:
        if proceso.tamaño <= memoria.count("Libre"):
            procesos_listos.append(proceso)
            for i in range(proceso.paginas):
                indice_libre = memoria.index("Libre")
                memoria[indice_libre] = proceso.numero_programa
            procesos_nuevos.remove(proceso)

    # Realizar cambios de contexto si es necesario
    if not procesos_listos and procesos_nuevos:
        quantum = 3
        continue

    # Ejecutar procesos en la cola de listos
    if procesos_listos:
        proceso_ejecucion = procesos_listos[0]
        tiempo_transcurrido_quantum = 0
        while tiempo_transcurrido_quantum < quantum and proceso_ejecucion.tiempo_restante_cpu > 0:
            proceso_ejecucion.actualizar_tiempo(1, tiempo_global)
            tiempo_transcurrido_quantum += 1
            tiempo_global += 1
        if proceso_ejecucion.tiempo_restante_cpu <= 0:
            proceso_ejecucion.tiempo_finalizacion = tiempo_global
            procesos_terminados.append(proceso_ejecucion)
            for i in range(proceso_ejecucion.paginas):
                memoria[memoria.index(proceso_ejecucion.numero_programa)] = "Libre"
            procesos_listos.pop(0)
        else:
            procesos_listos.append(proceso_ejecucion)
            procesos_listos.pop(0)

    # Incrementar tiempo global si no hay procesos listos
    else:
        tiempo_global += 1

    # Manejo de eventos del teclado
    if keyboard.is_pressed('e'):
        proceso_bloqueado = procesos_listos.pop(0)
        proceso_bloqueado.estado = ESTADOS["Bloqueado"]
        cola_de_bloqueados.append(proceso_bloqueado)
        time.sleep(8)  # Tiempo de bloqueo
        proceso_bloqueado.estado = ESTADOS["Listo"]
        procesos_listos.append(proceso_bloqueado)

    # Manejo de otros eventos del teclado
    if keyboard.is_pressed('w'):
        proceso_terminado = procesos_listos.pop(0)
        proceso_terminado.estado = ESTADOS["Terminado"]
        procesos_terminados.append(proceso_terminado)

    if keyboard.is_pressed('p'):
        print("El programa ha sido pausado. Presione 'C' para continuar.")
        Vuelta = 0
        while True:
            if Vuelta == 0:
                mostrar_memoria(memoria)
                Vuelta == 1
            if keyboard.is_pressed('c'):
                print("El programa ha sido reanudado.")
                break

    if keyboard.is_pressed('n'):
        nuevo_proceso = generar_proceso(numero_anterior)
        procesos_nuevos.append(nuevo_proceso)
        numero_anterior += 1

    if keyboard.is_pressed('b'):
        mostrar_tabla_procesos(procesos_listos, procesos_nuevos, cola_de_bloqueados, procesos_terminados)

    if keyboard.is_pressed('t'):
        mostrar_tabla_paginas(memoria)

    # Mostrar estado del sistema
    mostrar_procesos_en_estado(ESTADOS["Nuevo"], procesos_nuevos)
    mostrar_proceso_en_ejecucion(proceso_ejecucion, tiempo_transcurrido_quantum)
    mostrar_cola_de_bloqueados(cola_de_bloqueados)
    mostrar_procesos_terminados(procesos_terminados)
    mostrar_reloj(tiempo_global)
    time.sleep(1)
    os.system ("cls")