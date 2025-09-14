import customtkinter
from tkinter import*
import serial
import serial.tools.list_ports
import datetime
from threading import Thread
import time

try:
    ESP32=serial.Serial("NADA",0)

except:
    pass

def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

    
def insertarDireccion(self):
    direccionEsclavo.delete("1.0","end-1c")
    direccionEsclavo.insert(f"1.0",int(esclavo.get()))


def horaFecha():
    actual = datetime.datetime.now()
    segundosR = round(actual.second + actual.microsecond / 1000000, 2)
    fechaR = actual.replace(second=int(segundosR), microsecond=0)
    return fechaR

def borrarTB(TB):
    TB.delete(0.0,'end')

def cerrar():
    ventana.destroy()
    ventana.quit()

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
            recibirTexto.insert(f"1.0",mensajeConFormato)
        except IndexError or NameError:
            pass

def iniciarI2C():
    enviar=f"{str(int(esclavo.get()))}$direccion"
    enviar1=f"iniciar"
    enviar2=enviar.encode('utf-8')
    enviar3=enviar1.encode('utf-8')
    enviar4="get_direccion"
    enviar5=enviar4.encode('utf-8')
    try:
        ESP32.write(enviar2)
        time.sleep(2)
        ESP32.write(enviar3)
        time.sleep(2)
        ESP32.write(enviar5)
    except:
        pass

hilo=Thread(target=insertarInformacion)

customtkinter.set_appearance_mode("Light")  # Modos: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Temas: "blue" (standard), "green", "dark-blue

ventana=customtkinter.CTk()
ventana.geometry(f"{1100}x{600}")
ventana.title("I2C Esclavo")

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

esclavo=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=1,to=99,number_of_steps=98,command=insertarDireccion)
esclavo.place(x=350,y=100)

direccionEsclavo=customtkinter.CTkTextbox(ventana,width=60,height=40,font=('helvetica',20),fg_color='transparent')
direccionEsclavo.place(x=450,y=50)

texto1=customtkinter.CTkLabel(ventana,width=60,height=40,font=('helvetica',20),fg_color='transparent',text="Dirección")
texto1.place(x=350,y=50)

recibirTexto=customtkinter.CTkTextbox(ventana,width=500,height=200,font=('Consolas',13),border_width=3)
recibirTexto.place(x=350,y=150)

borrarRecibido=customtkinter.CTkButton(ventana,width=100,height=50,text="Borrar",font=('helvetica',18),command=lambda:borrarTB(recibirTexto))
borrarRecibido.place(x=900,y=150)

salir=customtkinter.CTkButton(ventana,width=100,height=50,text="Salir",font=('helvetica',18),command=cerrar)
salir.place(x=900,y=250)

botonEstablecerDireccion=customtkinter.CTkButton(ventana,width=100,height=50,text="Iniciar I2C",font=('helvetica',18),command=iniciarI2C)
botonEstablecerDireccion.place(x=900,y=50)

ventana.mainloop()