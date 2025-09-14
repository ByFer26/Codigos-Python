import customtkinter
from tkinter import*
import serial
import serial.tools.list_ports
import datetime
from threading import Thread

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

def insertarEncabezado(event):
    textoNuevo=envioTexto.get("end-1c linestart", "end-1c")
    posicionCursor = envioTexto.index(customtkinter.INSERT)
    numeroLinea = int(posicionCursor.split('.')[0])
    encabezado = f"{horaFecha()}->: "
    envioTexto.insert(f"{numeroLinea}.0", encabezado)
    textoAEnviar1=f"{str(int(esclavo.get()))}${textoNuevo}"
    textoAEnviar=textoAEnviar1.encode('utf-8')
    ESP32.write(textoAEnviar)

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

def InsertarAcuse(self):
    carAcuse.delete("1.0","end-1c")
    carAcuse.insert(f"1.0",int(acuse.get()))

def confAcuse():
    envio=f"acuse${chr(int(acuse.get()))}"
    envio1=envio.encode('utf-8')
    ESP32.write(envio1)


hilo=Thread(target=insertarInformacion)

customtkinter.set_appearance_mode("Dark")  # Modos: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Temas: "blue" (standard), "green", "dark-blue

ventana=customtkinter.CTk()
ventana.geometry(f"{1100}x{600}")
ventana.title("SPI Maestro")

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

esclavo=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=39,number_of_steps=98,command=insertarDireccion)
esclavo.place(x=450,y=50)

direccionEsclavo=customtkinter.CTkTextbox(ventana,width=60,height=40,font=('helvetica',20),fg_color='transparent')
direccionEsclavo.place(x=650,y=35)

texto1=customtkinter.CTkLabel(ventana,width=60,height=40,font=('helvetica',20),fg_color='transparent',text="Pin SS")
texto1.place(x=350,y=35)

acuse=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=33,to=125,number_of_steps=92,command=InsertarAcuse)
acuse.place(x=450,y=100)

texto1=customtkinter.CTkLabel(ventana,width=60,height=40,font=('helvetica',14),fg_color='transparent',text="Acuse recibido")
texto1.place(x=350,y=85)

carAcuse=customtkinter.CTkTextbox(ventana,width=60,height=40,font=('helvetica',20),fg_color='transparent')
carAcuse.place(x=650,y=85)

envioTexto=customtkinter.CTkTextbox(ventana,width=500,height=200,font=('Consolas',13),border_width=3)
envioTexto.place(x=350,y=150)
envioTexto.bind("<Return>", insertarEncabezado)

recibirTexto=customtkinter.CTkTextbox(ventana,width=500,height=200,font=('Consolas',13),border_width=3)
recibirTexto.place(x=350,y=375)

confSPI=customtkinter.CTkButton(ventana,width=100,height=50,text="Configurar SPI",font=('helvetica',14),command=confAcuse)
confSPI.place(x=900,y=50)

borrarRecibido=customtkinter.CTkButton(ventana,width=100,height=50,text="Borrar",font=('helvetica',18),command=lambda:borrarTB(recibirTexto))
borrarRecibido.place(x=900,y=400)

borrarEnvio=customtkinter.CTkButton(ventana,width=100,height=50,text="Borrar",font=('helvetica',18),command=lambda:borrarTB(envioTexto))
borrarEnvio.place(x=900,y=150)

salir=customtkinter.CTkButton(ventana,width=100,height=50,text="Salir",font=('helvetica',18),command=cerrar)
salir.place(x=900,y=500)

ventana.mainloop()