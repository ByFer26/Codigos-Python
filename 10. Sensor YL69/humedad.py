import customtkinter
import serial
import serial.tools.list_ports
from CTkSpinbox import *
from datetime import datetime
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from humedadDB import *
estadoDB=0
estadoPuerto = 1
dato1 = 0
x1 = []

recepcionC = True

def crearArreglos(longitud):
    return [0] * longitud

def insertarDatosR(arreglo, valor):
    if len(arreglo) >= 100:
        arreglo.pop(0)
    arreglo.append(valor)
    return arreglo

def listadoPuertos():
    return [i.name for i in serial.tools.list_ports.comports()]

def actualizarPuertos():
    Puertos.configure(values=listadoPuertos())

def conectar():
    global estadoPuerto, ESP32
    if estadoPuerto == 1:
        try:
            ESP32 = serial.Serial(Puerto.get(), int(Velocidad.get()))
            botonConectar.configure(text="Desconectar")
            print("Conexión exitosa")
        except:
            print("Error de conexión")
    elif estadoPuerto == 2:
        print("Desconectando...")
        botonConectar.configure(text="Conectar")
        ESP32.close()
    estadoPuerto += 1
    if estadoPuerto >= 3:
        estadoPuerto = 1

def recepcion():
    ESP32.reset_input_buffer()
    while True:
        try:
            datos = ESP32.readline().decode('utf-8').replace('\r\n', '')
            return datos
        except (ValueError, UnicodeDecodeError, IndexError):
            continue

def obtenerDatos():
    global recepcionC, dato1
    while recepcionC:
        try:
            dato1 = float(recepcion())
            dato1=(-1*dato1)+4095
            dato1 = round((dato1 / 4096) * 100, 2)
            humedadT.configure(text=f'Humedad: {dato1} %')
            comparacion(dato1,humHum1.get())
        except:
            pass

def graficar(frame, linea1, arr1):
    arr1 = insertarDatosR(arr1, dato1)
    linea1.set_data(range(len(arr1)), arr1)
    return linea1,

def iniciar():
    global x1, hilo, anim
    try:
        crearTabla("YL69","Hora","Tipo")
    except:
        pass

    x1 = crearArreglos(100)
    humLval.configure(text=f'{round(((humHum.get()/4096)*100),2)} %')
    humLval1.configure(text=f'{((round(float(humHum1.get()),2))/100)*100} %')
    if not hilo.is_alive():
        hilo = Thread(target=obtenerDatos)
        hilo.start()
    anim = animation.FuncAnimation(figura, graficar, fargs=(linea1, x1), interval=100, blit=False)
    grafica.draw()

def salir():
    global recepcionC
    recepcionC = False
    try:
        ESP32.close()
    except:
        pass
    ventana.destroy()

def humbralHumS(value):
    datoHumbraHum = float(value)
    datoHumbraHum=(datoHumbraHum/255)*100
    datoHumbraHum=round(datoHumbraHum,2)
    humLval.configure(text=f'{datoHumbraHum} %')
    envio=f'Encendido${round(humHum.get(),0)}'
    print(envio)

def humbralHumS1(value):

    datoL = float(value)
    datoL = round(datoL, 2)
    humLval1.configure(text=f'{datoL} %')

def comparacion(entrada,umbral):
    global estadoDB
    if entrada<umbral:
        salida=1
        indicador.configure(bg_color='Red')
        envio=f'Encendido${round(humHum.get(),0)}'
        envio=bytes(envio,'utf-8')
        ESP32.write(envio)
        if estadoDB==0:
            insertarDatos("YL69","Hora","Tipo",str(datetime.now()),str(entrada))
            estadoDB=1
    else:
        salida=0
        indicador.configure(bg_color='Green')
        envio=f'Apagado'
        envio=bytes(envio,'utf-8')
        ESP32.write(envio)   
        if estadoDB==1:
            insertarDatos("YL69","Hora","Tipo",str(datetime.now()),str(entrada))
            estadoDB=0  
    print(salida)
    return salida

def genPDF():
    generarPDF("YL69","Datos_YL69")

def elimDatos():
    eliminarDatos("YL69")
# Configurar ventana principal
ventana = customtkinter.CTk()
ventana.geometry("1300x585")
ventana.title("Sensor YL69")
ventana.configure(fg_color="#242424")

# Crear hilo
hilo = Thread(target=obtenerDatos)

# Configurar gráfica
figura, eje1 = plt.subplots()
figura.set_size_inches(4, 3)
figura.set_facecolor("#242424")
figura.tight_layout(pad=2)
eje1.set_facecolor("#242424")
eje1.tick_params(colors="white")
eje1.set_xlim(0, 100)
eje1.set_ylim(0, 120)
eje1.set_ylabel("Humedad (%)", color="white")
eje1.grid()
linea1, = eje1.plot([], [], color="#EA08DD")

# Widgets
barraLateral = customtkinter.CTkFrame(ventana, width=300, height=580)
barraLateral.grid(row=0, column=0, rowspan=4)

Puerto = customtkinter.StringVar(ventana)
Puertos = customtkinter.CTkComboBox(ventana, values=listadoPuertos(), width=150, height=30, variable=Puerto, font=('helvetica', 18))
Puertos.set("Puerto")
Puertos.place(x=75, y=100)

Velocidad = customtkinter.StringVar(ventana)
Velocidades = customtkinter.CTkComboBox(ventana, values=["4800", "9600", "31250", "38400", "57600", "196200", "230400"], width=150, height=30,
                                        variable=Velocidad, font=('helvetica', 18))
Velocidades.set("Velocidad")
Velocidades.place(x=75, y=200)

botonConectar = customtkinter.CTkButton(ventana, width=150, height=30, text="Conectar", font=('helvetica', 20), command=conectar,
                                        corner_radius=6, fg_color="#D52585")
botonConectar.place(x=75, y=350)

botonRefrescarPuertos = customtkinter.CTkButton(ventana, width=150, height=30, text="Actualizar", font=('helvetica', 20),
                                                command=actualizarPuertos, corner_radius=6, fg_color="#611D6A")
botonRefrescarPuertos.place(x=75, y=400)

botonIniciar = customtkinter.CTkButton(ventana, text="Iniciar", width=150, height=30, command=iniciar, corner_radius=6, fg_color="#8A3DF3",
                                       font=('Consolas', 20))
botonIniciar.place(x=350, y=520)

botonSalir = customtkinter.CTkButton(ventana, text="Salir", width=150, height=30, corner_radius=6, fg_color="#8A3DF3", command=salir,
                                     font=('Consolas', 20))
botonSalir.place(x=600, y=520)

botonGenPDF = customtkinter.CTkButton(ventana, text="Generar PDF", width=150, height=30, corner_radius=6, fg_color="#8A3DF3",command=genPDF,
                                      font=('Consolas', 20))
botonGenPDF.place(x=850, y=520)

botonElimDatos = customtkinter.CTkButton(ventana, text="Eliminar Datos", width=150, height=30, corner_radius=6, fg_color="#8A3DF3",command=elimDatos,
                                         font=('Consolas', 20))
botonElimDatos.place(x=1050, y=520)

humedadT = customtkinter.CTkLabel(ventana, width=100, height=50, fg_color='transparent', text='Humedad: -- %',
                                  font=('Consolas', 30), text_color="#FFFFFF")
humedadT.place(x=350, y=50)

indicador = customtkinter.CTkLabel(ventana, width=150, height=50, fg_color='transparent', text="")
indicador.place(x=350, y=420)

humLabel=customtkinter.CTkLabel(ventana,width=200,height=25,text=f'Potencia bomba',font=('helvetica', 20),fg_color='transparent',text_color="#FFFFFF")
humLabel.place(x=700,y=140)
humHum=customtkinter.CTkSlider(ventana,width=300,height=25,from_=0,to=255,number_of_steps=255,command=humbralHumS)
humHum.place(x=700,y=175)
humLval=customtkinter.CTkLabel(ventana,width=200,height=25,text=f'',font=('Consolas', 20),fg_color='transparent',text_color="#FFFFFF")
humLval.place(x=1000,y=175)

humLabel1=customtkinter.CTkLabel(ventana,width=200,height=25,text=f'Umbra humedad',font=('helvetica', 20),fg_color='transparent',text_color="#FFFFFF")
humLabel1.place(x=700,y=235)
humHum1=customtkinter.CTkSlider(ventana,width=300,height=25,from_=0,to=99,number_of_steps=99,command=humbralHumS1)
humHum1.place(x=700,y=270)
humLval1=customtkinter.CTkLabel(ventana,width=200,height=25,text=f'',font=('Consolas', 20),fg_color='transparent',text_color="#FFFFFF")
humLval1.place(x=1000,y=270)

grafica = FigureCanvasTkAgg(figura, master=ventana)
grafica.get_tk_widget().place(x=400, y=300, anchor='w')



ventana.mainloop()

