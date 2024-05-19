import random
import time
import keyboard

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
    def __init__(self, numero_programa, tiempo_maximo_estimado, operacion, dato1, dato2):
        self.numero_programa = numero_programa
        self.tiempo_maximo_estimado = tiempo_maximo_estimado
        self.operacion = operacion
        self.dato1 = dato1
        self.dato2 = dato2
        self.tiempo_llegada = None
        self.tiempo_finalizacion = None
        self.tiempo_retorno = None
        self.tiempo_respuesta = None
        self.tiempo_espera = 0
        self.tiempo_servicio = 0
        self.estado = ESTADOS["Nuevo"]
        self.resultado = None
        self.tiempo_restante_cpu = self.tiempo_maximo_estimado

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
    return Proceso(numero_programa, tiempo_maximo_estimado, operacion, dato1, dato2)

def mostrar_procesos_en_estado(estado, procesos):
    print(f"\n{estado}:")
    for proceso in procesos:
        if proceso.estado == estado:
            print(f"- Número de Programa: {proceso.numero_programa}")
            print(f"- Tiempo Máximo Estimado: {proceso.tiempo_maximo_estimado}")
            if estado == ESTADOS["Bloqueado"]:
                print(f"- Tiempo Transcurrido Bloqueado: {proceso.tiempo_espera}")
            else:
                print(f"- Tiempo Restante CPU: {proceso.tiempo_restante_cpu}")

def mostrar_proceso_en_ejecucion(proceso, tiempo_transcurrido_quantum):
    print("\nProceso en Ejecución:")
    print(f"- Número de Programa: {proceso.numero_programa}")
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

# Main
def main():
    # Preguntar número de procesos inicial
    n_procesos = int(input("Ingrese el número de procesos inicial: "))

    # Preguntar valor del Quantum
    quantum = int(input("Ingrese el valor del Quantum: "))

    # Crear lista de procesos
    procesos = [generar_proceso(i) for i in range(n_procesos)]
    cola_de_listos = []
    cola_de_bloqueados = []
    procesos_terminados = []

    tiempo_actual = 0
    tiempo_transcurrido_quantum = 0

    proceso_en_ejecucion = None  # Inicializar proceso_en_ejecucion con None

    while True:
        # Verificar si quedan procesos en ejecución, en cola de listos o en bloqueados
        if not (procesos or cola_de_listos or cola_de_bloqueados):
            break

        # Mostrar información
        mostrar_procesos_en_estado(ESTADOS["Nuevo"], procesos)
        print(f"\nValor del Quantum: {quantum}")
        mostrar_cola_de_bloqueados(cola_de_listos)
        if cola_de_listos:
            proceso_en_ejecucion = cola_de_listos.pop(0)
            proceso_en_ejecucion.estado = ESTADOS["Ejecución"]
            mostrar_proceso_en_ejecucion(proceso_en_ejecucion, tiempo_transcurrido_quantum)
        else:
            print("\nNo hay proceso en ejecución.")
        mostrar_cola_de_bloqueados(cola_de_bloqueados)
        mostrar_procesos_terminados(procesos_terminados)
        mostrar_reloj(tiempo_actual)

        # Ejecutar proceso
        if proceso_en_ejecucion:
            proceso_en_ejecucion.actualizar_tiempo(1, tiempo_actual)  # Añade tiempo_actual como argumento
            tiempo_transcurrido_quantum += 1

            if proceso_en_ejecucion.tiempo_restante_cpu == 0:
                proceso_en_ejecucion.tiempo_finalizacion = tiempo_actual
                proceso_en_ejecucion.calcular_tiempos(tiempo_actual)
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                tiempo_transcurrido_quantum = 0
            elif tiempo_transcurrido_quantum == quantum:
                proceso_en_ejecucion.estado = ESTADOS["Listo"]
                cola_de_listos.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                tiempo_transcurrido_quantum = 0


        # Actualizar tiempo de bloqueo de procesos bloqueados
        for proceso in cola_de_bloqueados:
            proceso.actualizar_tiempo(1)
            if proceso.tiempo_espera == 8:
                proceso.estado = ESTADOS["Listo"]
                cola_de_listos.append(proceso)
                cola_de_bloqueados.remove(proceso)

        # Generar nuevos procesos
        if keyboard.is_pressed('n'):  # Detecta si se presiona la tecla 'n'
            nuevo_proceso = generar_proceso(len(procesos))
            procesos.append(nuevo_proceso)
            cola_de_listos.append(nuevo_proceso)

        # Manejar entrada del usuario
        if keyboard.is_pressed('e'):  # Detecta si se presiona la tecla 'e'
            if proceso_en_ejecucion:
                proceso_en_ejecucion.estado = ESTADOS["Bloqueado"]
                cola_de_bloqueados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                tiempo_transcurrido_quantum = 0
        elif keyboard.is_pressed('w'):  # Detecta si se presiona la tecla 'w'
            if proceso_en_ejecucion:
                proceso_en_ejecucion.resultado = None
                proceso_en_ejecucion.tiempo_finalizacion = tiempo_actual
                proceso_en_ejecucion.calcular_tiempos(tiempo_actual)
                procesos_terminados.append(proceso_en_ejecucion)
                proceso_en_ejecucion = None
                tiempo_transcurrido_quantum = 0
        elif keyboard.is_pressed('p'):  # Detecta si se presiona la tecla 'p'
            input("Presione 'C' para continuar...")
        elif keyboard.is_pressed('b'):  # Detecta si se presiona la tecla 'b'
            mostrar_procesos_terminados(procesos)
            input("Presione 'C' para continuar...")

        tiempo_actual += 1
        time.sleep(1)  # Espera un segundo antes de continuar al siguiente ciclo para que el tiempo sea en tiempo real

    # Mostrar tabla de procesos al finalizar
    print("\nTabla de Procesos al Finalizar:")
    mostrar_procesos_terminados(procesos_terminados)

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
