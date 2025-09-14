import tkinter as tk

# Crear la aplicación tkinter
app = tk.Tk()
app.title("Ejemplo de Label acumulativo")

# Crear el widget Text y configurarlo como un Label
text_widget = tk.Text(app, wrap="word", width=40, height=10, state="disabled", highlightthickness=0, selectbackground="transparent") 
text_widget.pack()

# Función para agregar un nuevo mensaje al Texto (simulando un Label)
def agregarMensaje(mensaje):
    # Obtener el contenido actual del Texto
    contenido_actual = text_widget.get("1.0", "end-1c")
    
    # Obtener el número de líneas actuales
    num_lineas = int(text_widget.index("end-1c").split(".")[0])
    
    # Formatear el nuevo mensaje con el encabezado
    mensaje_formateado = f"Linea {num_lineas}: {mensaje}\n"
    
    # Agregar el nuevo mensaje al contenido existente
    nuevo_contenido = contenido_actual + mensaje_formateado
    
    # Actualizar el contenido del Texto (simulando un Label)
    text_widget.config(state="normal")  # Habilitar la edición temporalmente
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", nuevo_contenido)
    text_widget.config(state="disabled")  # Deshabilitar la edición nuevamente

# Ejemplo de uso: agregar un nuevo mensaje al Texto (simulando un Label)
agregarMensaje("Este es el primer mensaje.")
agregarMensaje("Este es el segundo mensaje.")

# Ejecutar la aplicación tkinter
app.mainloop()



