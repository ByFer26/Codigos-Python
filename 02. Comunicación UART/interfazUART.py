import customtkinter
from tkinter import*
import serial
import serial.tools.list_ports
import datetime
from threading import Thread

condicion1=True
condicion2=True
texto_previo_enviado = ""
longAnt=0

try:
    ESP32=serial.Serial("NADA",0)

except:
    pass

def conectar():
    condicion1=True
    global ESP32
    while (condicion1):
        try:
            ESP32=serial.Serial(Puerto.get(),int(Velocidad.get()))
            condicion1=False
            print("Conexión exitosa")
            hilo.start()
        except:
            pass
            print("Error de conexión")
    return ESP32

def horaFecha():
    actual = datetime.datetime.now()
    segundosR = round(actual.second + actual.microsecond / 1000000, 2)
    fechaR = actual.replace(second=int(segundosR), microsecond=0)
    return fechaR

def insertarEncabezado(event):
    textoNuevo=textbox.get("end-1c linestart", "end-1c")
    posicionCursor = textbox.index(customtkinter.INSERT)
    numeroLinea = int(posicionCursor.split('.')[0])
    encabezado = f"{horaFecha()}->: "
    textbox.insert(f"{numeroLinea}.0", encabezado)
    textoAEnviar=textoNuevo.encode('utf-8')
    ESP32.write(textoAEnviar)

def recibirInformacion(dispositivo):
    condicion2=True
    dispositivo.reset_input_buffer()
    while condicion2:
        try:
            datos=dispositivo.readline().decode("utf-8").replace('r\n', '')
            condicion2=False
        except ValueError or UnicodeDecodeError:
            pass
        except IndexError:
            pass
    return datos

def insertarInformacion():
    while True:
        mensaje=recibirInformacion(ESP32)
        mensajeConFormato=f"{str(horaFecha())}-> {mensaje}"
        try:
            recibidos.insert(f"1.0",mensajeConFormato)
        except IndexError or NameError:
            pass

hilo=Thread(target=insertarInformacion)

def conectarSerial():
    envio=f"velocidad${velocidad2.get()}"
    envio2=envio.encode('utf-8')
    try:
        ESP32.write(envio2)
        print("Se envio")
    except:
        pass

def borrarTB(TB):
    TB.delete(0.0,'end')


def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

def cerrar():
    ventana.destroy()
    ventana.quit()

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("coloresUART.json")  # Themes: "blue" (standard), "green", "dark-blue

ventana=customtkinter.CTk()
ventana.geometry(f"{1100}x{580}")
ventana.title("Comunicación UART")

barraLateral=customtkinter.CTkFrame(ventana,width=300,height=580)
barraLateral.grid(row=0, column=0, rowspan=4)

Puerto=customtkinter.StringVar(ventana)
Puertos=customtkinter.CTkComboBox(ventana,values=listadoPuertos(),width=150,height=30,variable=Puerto,font=('helvetica',18))
Puertos.set("Puerto")
Puertos.place(x=75,y=150)

Velocidad=customtkinter.StringVar(ventana)
Velocidades=customtkinter.CTkComboBox(ventana,values=["4800","9600","31250","38400","57600","196200","230400"],width=150,height=30,
                                      variable=Velocidad,font=('helvetica',18))
Velocidades.set("Velocidad")
Velocidades.place(x=75,y=300)

botonConectar=customtkinter.CTkButton(ventana,width=150,height=50,text="Conectar",font=('helvetica',18),command=conectar)
botonConectar.place(x=75,y=450)

textbox=customtkinter.CTkTextbox(ventana,width=500,height=200,font=('Consolas',13))
textbox.place(x=350,y=100)
textbox.bind("<Return>", insertarEncabezado)

botonBorrarTxb=customtkinter.CTkButton(ventana,width=100,height=50,text="Borrar",font=('helvetica',18),command=lambda:borrarTB(textbox))
botonBorrarTxb.place(x=900,y=150)

recibidos=customtkinter.CTkTextbox(ventana,width=500,height=200,font=('Consolas',13),bg_color="#FFFFFF")
recibidos.place(x=350,y=350)

botonConectarSerial=customtkinter.CTkButton(ventana,text="Conectar Serial",font=('helvetica',18),command=conectarSerial)
botonConectarSerial.place(x=900,y=50)

velocidad2=customtkinter.StringVar(ventana)
Velocidades2=customtkinter.CTkComboBox(ventana,values=["4800","9600","31250","38400","57600","196200","230400"],width=150,height=30,
                                      variable=velocidad2,font=('helvetica',18))

Velocidades2.set("Velocidad")
Velocidades2.place(x=350,y=50)

botonBorrarRecibido=customtkinter.CTkButton(ventana,width=100,height=50,text="Borrar",font=('helvetica',18),command=lambda:borrarTB(recibidos))
botonBorrarRecibido.place(x=900,y=400)

salir=customtkinter.CTkButton(ventana,width=100,height=50,text="Salir",font=('helvetica',18),command=cerrar)
salir.place(x=900,y=500)


ventana.mainloop()