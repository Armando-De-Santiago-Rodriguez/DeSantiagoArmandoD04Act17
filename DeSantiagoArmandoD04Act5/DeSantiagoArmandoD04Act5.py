import tkinter as tk
import random

paused = False  # Variable para controlar si el programa está en pausa o no

def generar_procesos(cantidad):
    lista_procesos = []
    for i in range(cantidad):
        proceso = {}
        proceso['ID'] = i
        proceso['Nombre'] = random.choice(['Pedro','Juan','Carlos','Maria','Pablo','Armando','Adrian','Alejandra','Camila','Diego','Fernanda'])
        proceso['Operacion'] = random.choice(['+', '-', '*', '/', '%'])
        proceso['Tiempo'] = random.randint(2,10)
        proceso['Numero_1'] = random.randint(1,100)
        proceso['Numero_2'] = random.randint(1,100)
        lista_procesos.append(proceso)
    return lista_procesos

def imprimir_procesos():
    global paused
    cantidad = int(entry_cantidad.get())
    total_procesos = generar_procesos(cantidad)
    proceso_actual = 0
    tiempo_transcurrido = 0
    procesos_finalizados = []

    def imprimir_lote():
        nonlocal proceso_actual
        nonlocal tiempo_transcurrido
        nonlocal procesos_finalizados

        if not paused:  # Solo imprime si el programa no está en pausa
            lote_procesos = total_procesos[proceso_actual:proceso_actual+4]
            for proceso in lote_procesos:
                if proceso['Operacion'] == '/':  # Verifica si la operación es división
                    # Muestra un mensaje de error para la división por cero si la operación es '/'
                    if proceso['Numero_2'] == 0:
                        mensaje_error = f"Error en proceso ID: {proceso['ID']}. No se puede dividir por cero."
                        label_procesos_en_curso.config(text=label_procesos_en_curso.cget("text") + "\n" + mensaje_error)
                        return  # Detiene el proceso si hay un error
                
                texto = f"ID: {proceso['ID']}, Nombre: {proceso['Nombre']}, Operación: {proceso['Operacion']}, Tiempo: {proceso['Tiempo']}, Número 1: {proceso['Numero_1']}, Número 2: {proceso['Numero_2']}"
                label_procesos_en_curso.config(text=label_procesos_en_curso.cget("text") + "\n" + texto)
            
            # Calcular el tiempo total de este lote de procesos
            tiempo_lote = sum(proceso['Tiempo'] for proceso in lote_procesos)
            tiempo_transcurrido += tiempo_lote
            label_tiempo.config(text=f"Tiempo transcurrido: {tiempo_transcurrido} segundos")
            
            proceso_actual += 4
            
            if proceso_actual < cantidad:
                ventana.after(tiempo_lote * 1000, borrar_procesos)
            else:
                procesos_finalizados.extend(total_procesos[:proceso_actual-4])  # Excluir el proceso actual
                mostrar_finalizados(procesos_finalizados)

    def borrar_procesos():
        label_procesos_en_curso.config(text="")
        imprimir_lote()

    imprimir_lote()

def mostrar_finalizados(procesos_finalizados):
    for proceso in procesos_finalizados:
        resultado = eval(f"{proceso['Numero_1']} {proceso['Operacion']} {proceso['Numero_2']}")
        texto = f"ID: {proceso['ID']}, Nombre: {proceso['Nombre']}, Operación: {proceso['Operacion']}, Tiempo: {proceso['Tiempo']}, Número 1: {proceso['Numero_1']}, Número 2: {proceso['Numero_2']}, Resultado: {resultado}"
        label_lotes_finalizados.config(text=label_lotes_finalizados.cget("text") + "\n" + texto)

def comenzar():
    frame_inicio.pack_forget()
    frame_resultado.pack()
    imprimir_procesos()

def pause_resume(event):
    global paused
    if event.char == 'p':
        paused = True
    elif event.char == 'c':
        paused = False
        imprimir_procesos()
    elif event.char == 'i':
        ventana.quit()
    elif event.char == 'w':
        mensaje_error = "Error: Operación no válida en el próximo lote/proceso."
        label_procesos_en_curso.config(text=label_procesos_en_curso.cget("text") + "\n" + mensaje_error)
        paused = True  # Pausa el programa después de mostrar el mensaje de error

# Crear ventana
ventana = tk.Tk()
ventana.title("Generador de Procesos")
ventana.geometry("800x400")  # Tamaño de la ventana

# Widgets para el frame de inicio
frame_inicio = tk.Frame(ventana)
frame_inicio.pack(padx=10, pady=10, fill=tk.BOTH)

label_cantidad = tk.Label(frame_inicio, text="Cantidad de procesos:")
label_cantidad.pack(side=tk.LEFT)

entry_cantidad = tk.Entry(frame_inicio)
entry_cantidad.pack(side=tk.LEFT, padx=5)

boton_generar = tk.Button(frame_inicio, text="Generar procesos", command=comenzar)
boton_generar.pack(side=tk.LEFT)

# Crear frames para el resultado
frame_resultado = tk.Frame(ventana)
frame_resultado.pack(padx=10, pady=10, fill=tk.BOTH)

frame_izquierda = tk.LabelFrame(frame_resultado, text="Procesos en curso")
frame_izquierda.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_derecha = tk.LabelFrame(frame_resultado, text="Procesos finalizados")
frame_derecha.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_centro = tk.LabelFrame(frame_resultado, text="Tiempo transcurrido")
frame_centro.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Widgets para el frame de resultado
label_procesos_en_curso = tk.Label(frame_izquierda, text="")
label_procesos_en_curso.pack()

label_lotes_finalizados = tk.Label(frame_derecha, text="")
label_lotes_finalizados.pack()

label_tiempo = tk.Label(frame_centro, text="")
label_tiempo.pack()

# Manejo de eventos de teclado
ventana.bind("<Key>", pause_resume)

# Ejecutar ventana
ventana.mainloop()
