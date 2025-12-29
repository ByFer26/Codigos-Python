import customtkinter
import serial
import serial.tools.list_ports
from CTkSpinbox import*
from datetime import datetime
import numpy as np

estadoPuerto=1

def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

def actualizarPuertos():
    Puertos.configure(values=listadoPuertos())

def conectar():
    condicion1=True
    global estadoPuerto
    global ESP32

   # try:
   #     crearTabla("TCS230","Objeto","Estado","Hora")
   # except:
   #     pass

    if estadoPuerto==1:
        while (condicion1):
            try:
                ESP32=serial.Serial(Puerto.get(),int(Velocidad.get()))
                condicion1=False
                botonConectar.configure(text="Desconectar")
                print("Conexión exitosa")
            except:
                pass
                print("Error de conexión")

    if estadoPuerto==2:
        print("Desconectando...")
        botonConectar.configure(text="Conectar")
        ESP32.close()
    

    estadoPuerto=estadoPuerto+1

    if estadoPuerto>=3:
        estadoPuerto=1

ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Sensor MQ135")

barraLateral=customtkinter.CTkFrame(ventana,width=300,height=580)
barraLateral.grid(row=0, column=0, rowspan=4)

Puerto=customtkinter.StringVar(ventana)
Puertos=customtkinter.CTkComboBox(ventana,values=listadoPuertos(),width=150,height=30,variable=Puerto,font=('helvetica',18))
Puertos.set("Puerto")
Puertos.place(x=75,y=100)

Velocidad=customtkinter.StringVar(ventana)
Velocidades=customtkinter.CTkComboBox(ventana,values=["4800","9600","31250","38400","57600","196200","230400"],width=150,height=30,
                                      variable=Velocidad,font=('helvetica',18))
Velocidades.set("Velocidad")
Velocidades.place(x=75,y=200)

botonConectar=customtkinter.CTkButton(ventana,width=150,height=30,text="Conectar",font=('helvetica',20),command=conectar,
                                      corner_radius=6,fg_color="#D52585")
botonConectar.place(x=75,y=350)

botonRefrescarPuertos=customtkinter.CTkButton(ventana,width=150,height=30,text="Actualizar",font=('helvetica',20),
                                              command=actualizarPuertos,corner_radius=6,fg_color="#611D6A")
botonRefrescarPuertos.place(x=75,y=400)

ventana.mainloop()