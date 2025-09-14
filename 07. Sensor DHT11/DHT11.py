import customtkinter
import serial
import serial.tools.list_ports
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkSpinbox import *
from DHT11DB import *
from datetime import datetime

estadoPuerto=1
dato1=0
dato2=0
x1=[]
x2=[]

recepcionC=True
condicion1=True
condicion2=True
condicion3=True
condicion4=True

def iniciar():
    global x1,x2
    try:
        crearTabla("DHT11","Hora","Tipo","Dato")
    except:
        pass
    x1=crearArreglos(100)
    x2=crearArreglos(100)
    hilo.start()
    anim = animacion.FuncAnimation(figura, graficar,  fargs=(linea1,linea2,x1,x2),interval = 1, blit = False )
    grafica.draw()

def recepcion():
    condicion=True
    ESP32.reset_input_buffer()
    while condicion:
        try:
            datos=ESP32.readline().decode('utf-8').replace('\r\n', '')
            datos=datos.split(",")
            datos1=round(float(datos[0]),2)
            datos2=round(float(datos[1]),2)
            humedadV.configure(text=f"{datos1}%")
            temperaturaV.configure(text=f"{dato2}°C")
            condicion=False
        except ValueError or UnicodeDecodeError:
            pass

        except IndexError:
            pass
    return datos1,datos2

def obtenerDatos():
    global recepcionC
    while recepcionC:
        global dato1,dato2
        dato1,dato2=recepcion()
        verificar(1,dato1,setpoint1.get(),ESP32)
        verificar(2,dato2,setpoint2.get(),ESP32)

def crearArreglos(longitud):
    a1=[]
    for i in range(0,longitud):
        a1.append(0)
    return a1

def insertarDatosR(arreglo,valor):
    if len(arreglo)>=100:
        arreglo.pop(0)
    
    arreglo.append(valor)
    return arreglo

def graficar(self,linea1,linea2,arr1,arr2):
    arr1=insertarDatosR(arr1,dato1)
    arr2=insertarDatosR(arr2,dato2)
    linea1.set_data(range(100), arr1)
    linea2.set_data(range(100), arr2)


hilo=Thread(target=obtenerDatos)

def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

def conectar():
    setpoint1.set(50)
    setpoint2.set(50)
    condicion1=True
    global estadoPuerto
    global ESP32
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

    return ESP32

def actualizarPuertos():
    Puertos.configure(values=listadoPuertos())

        
figura, (eje1,eje2)=plt.subplots(2,1)
figura.set_size_inches(5,5)
figura.set_facecolor('#242424')
figura.tight_layout(pad=2)
eje1.tick_params(colors='#FFFFFF')
eje2.tick_params(colors='#FFFFFF')
eje1.set_facecolor('#000000')
eje2.set_facecolor('#000000')
eje1.set_xlim(0,100)
eje2.set_xlim(0,100)
eje1.set_ylim(0,100)
eje2.set_ylim(0,100)
eje1.set_ylabel('Humedad (%)',color='#FFFFFF')
eje2.set_ylabel('Temperatura °C',color='#FFFFFF')
eje1.grid()
eje2.grid()
linea1=eje1.plot([], [])[0]
linea1.set_color('#EA08DD')
linea2=eje2.plot([], [])[0]
linea2.set_color('#08EA2E')

def setpointHumedad(self):
    labelHumSetpoint.configure(text=f"{int(setpoint1.get())} %")

def setpointTemperatura(self):
    labelTemSetpoint.configure(text=f"{int(setpoint2.get())} °C")

def salir():
    ventana.destroy()
    ventana.quit()
    ESP32.close()

def verificar(tipo,dato,limite,dispositivo):
    global condicion1,condicion2,condicion3,condicion4
    if tipo==1:
        if condicion1==True:
            if dato>=limite:
                dispositivo.write(b'a')
                insertarDatos("DHT11","Hora","Tipo","Dato",str(datetime.now()),"Humedad",str(dato))
                condicion1=False
                condicion2=True
        
        if condicion2==True:
            if dato<limite:
                dispositivo.write(b'b')
                insertarDatos("DHT11","Hora","Tipo","Dato",str(datetime.now()),"Humedad",str(dato))
                condicion2=False
                condicion1=True
    
    if tipo==2:
        if condicion3==True:
            if dato>=limite:
                dispositivo.write(b'C')
                insertarDatos("DHT11","Hora","Tipo","Dato",str(datetime.now()),"Temperatura",str(dato))
                condicion3=False
                condicion4=True
        
        if condicion4==True:
            if dato<limite:
                dispositivo.write(b'd')
                insertarDatos("DHT11","Hora","Tipo","Dato",str(datetime.now()),"Temperatura",str(dato))
                condicion4=False
                condicion3=True

def genPDF():
    generarPDF("DHT11","Datos_DHT11")

def elimDatos():
    eliminarDatos("DHT11")


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue") 

ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Sensor DHT11")

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

botonIniciar=customtkinter.CTkButton(ventana,text="Iniciar",width=150,height=30,command=iniciar,corner_radius=6,fg_color="#8A3DF3",
                                     font=('Consolas',20))
botonIniciar.place(x=350,y=520)

humedadT=customtkinter.CTkLabel(ventana,width=100,height=50,fg_color='transparent',text="Humedad:",font=('Consolas',30))
humedadT.place(x=800,y=50)

humedadV=customtkinter.CTkLabel(ventana,width=100,height=50,fg_color='transparent',font=('Consolas',30),text="")
humedadV.place(x=950,y=50)

temperaturaT=customtkinter.CTkLabel(ventana,width=100,height=50,fg_color='transparent',text="Temperatura:",font=('Consolas',30))
temperaturaT.place(x=800,y=300)

temperaturaV=customtkinter.CTkLabel(ventana,width=100,height=50,fg_color='transparent',text="",font=('Consolas',30))
temperaturaV.place(x=1000,y=300)

setpoint1=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=100,number_of_steps=100,command=setpointHumedad)
setpoint1.place(x=800,y=150)

label1=customtkinter.CTkLabel(ventana,width=100,height=50,text="Setpoint",font=('Consolas',20))
label1.place(x=800,y=100)

labelHumSetpoint=customtkinter.CTkLabel(ventana,text="",fg_color="transparent",font=('Consolas',30))
labelHumSetpoint.place(x=1020,y=140)

##################################################################################################################################

setpoint2=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=100,number_of_steps=100,command=setpointTemperatura)
setpoint2.place(x=800,y=400)

label2=customtkinter.CTkLabel(ventana,width=100,height=50,text="Setpoint",font=('Consolas',20))
label2.place(x=800,y=350)

labelTemSetpoint=customtkinter.CTkLabel(ventana,text="",fg_color="transparent",font=('Consolas',30))
labelTemSetpoint.place(x=1020,y=390)

botonSalir=customtkinter.CTkButton(ventana,text="Salir",width=150,height=30,corner_radius=6,fg_color="#8A3DF3",command=salir,
                                     font=('Consolas',20))
botonSalir.place(x=600,y=520)

botonGenPDF=customtkinter.CTkButton(ventana,text="Generar PDF",width=150,height=30,corner_radius=6,fg_color="#8A3DF3",
                                     font=('Consolas',20),command=genPDF)
botonGenPDF.place(x=850,y=520)

botonElimDatos=customtkinter.CTkButton(ventana,text="Eliminar Datos",width=150,height=30,corner_radius=6,fg_color="#8A3DF3",
                                       font=('Consolas',20),command=elimDatos)

botonElimDatos.place(x=1050,y=520)


#Grafica

grafica=FigureCanvasTkAgg(figura,master=ventana)
grafica._tkcanvas.grid(row = 1,column = 2, padx=1,pady=1)
grafica.get_tk_widget().place(x=300, y=250, anchor='w')


ventana.mainloop()