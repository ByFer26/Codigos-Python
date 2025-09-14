import customtkinter
import serial
import serial.tools.list_ports
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkSpinbox import *
from datetime import datetime
import time
from CTkSpinbox import *
from YL69DB import *

estadoPuerto=1
recepcionC=True
estadoHilo=1
x1=[]
dato1=0
ppm=0
alarmaP=0
toleranciaP=0

def alarma(valor,tolerancia):
    if valor<tolerancia:
        valorH.configure(bg_color="Red")
        v1=velocidadB.get()/100
        v1=255*v1
        v1=round(v1,0)
        envio=f'Encendido${v1}'
        envio=envio=bytes(envio,'utf-8')
        ESP32.write(envio)
        insertarDatos("YL69", "Humedad", "Hora",str(dato1),str(datetime.now()))
    else:
        valorH.configure(bg_color="Green")
        envio=f'Apagado'
        envio=bytes(envio,'utf-8')
        ESP32.write(envio)


def confUmbral(self):
    umbral=tolHum.get()
    umbral=int(umbral)
    Bomba.configure(text=f'Umbral={int(tolHum.get())}%')

def confVelB(self):
    velBom=velocidadB.get()
    velBom=int(velBom)
    Bombav.configure(text=f'Velocidad={velBom}%')
        
def eliminarT():
    eliminarDatos("YL69")	    

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

def graficar(self,linea1,arr1):
    try:
        arr1=insertarDatosR(arr1,float(dato1))
        linea1.set_data(range(100), arr1)
    except ValueError:
        pass
    






def iniciar():
    global estadoHilo
    global x1
    #envio=f'a${str(round(velocidadT.get(),0))}${str(round(pinESP.get(),0))}\n'
    x1=crearArreglos(100)
    #envio=bytes(envio,'utf-8')
    for i in range(0,3):
        #ESP32.write(envio)
        time.sleep(0.5)
    if estadoHilo==1:
        hilo.start()
        estadoHilo=2
    else:
        pass

    anim = animacion.FuncAnimation(figura, graficar,  fargs=(linea1,x1),interval = 1, blit = False )
    grafica.draw()

def parar():
    #envio=f'b${str(round(velocidadT.get(),0))}${str(round(pinESP.get(),0))}\n'
    envio=bytes(envio,'utf-8')
    for i in range(0,3):
        ESP32.write(envio)
        time.sleep(0.5)

def recepcion():
    condicion=True
    ESP32.reset_input_buffer()
    while condicion:
        try:
            datos=ESP32.readline().decode('utf-8').replace('\r\n', '')
            condicion=False
        except ValueError or UnicodeDecodeError:
            pass

        except IndexError or AttributeError:
            pass
    return datos

def loop():
    while True:
        global dato1
        global ppm
        dato1=recepcion()
        try:
            dato1=float(dato1)
            dato1=(dato1/4095)*100
            dato1=float(dato1)
            dato1=round(dato1,2)
            particulas.configure(text=f'Humedad={dato1}%')
            alarma(dato1,tolHum.get())

        except ValueError:
            pass
            
        

hilo=Thread(target=loop)

def salir():
    ventana.destroy()
    ventana.quit()
    ESP32.close()


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

    try:
        crearTabla("YL69","Humedad","Hora")
        print("Hola")
    except:
       pass

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

def genPDF():
    generarPDF("YL69","sensor humedad")

def elimDatos():
    eliminarDatos("YL69")

figura, (eje1)=plt.subplots(1,1)
figura.set_size_inches(4,4)
figura.set_facecolor("#84B4FD")
figura.tight_layout(pad=2)
eje1.tick_params(colors='#000000')
eje1.set_facecolor("#84B4FD")
eje1.set_xlim(0,100)
eje1.set_ylim(0,110)
eje1.set_ylabel('Humedad (%)',color='#000000')
eje1.grid()
linea1=eje1.plot([], [])[0]
linea1.set_color('#0000FF')




ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Sensor YL69")

ventana.configure(fg_color="#84B4FD")

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

botonIniciar=customtkinter.CTkButton(ventana,text="Iniciar",width=150,height=30,corner_radius=6,fg_color="#00FF66",command=iniciar,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonIniciar.place(x=300,y=550)

botonSalir=customtkinter.CTkButton(ventana,text="Salir",width=150,height=30,corner_radius=6,fg_color="#00FF66",command=salir,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonSalir.place(x=500,y=550)

botonParar=customtkinter.CTkButton(ventana,text="Parar",width=150,height=30,corner_radius=6,fg_color="#00FF66",command=parar,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonParar.place(x=700,y=550)

botonGenPDF=customtkinter.CTkButton(ventana,text="Generar PDF",width=150,height=30,corner_radius=6,fg_color="#00FF66",
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000",command=genPDF)
botonGenPDF.place(x=900,y=550)

botonElimDatos=customtkinter.CTkButton(ventana,text="Eliminar Datos",width=150,height=30,corner_radius=6,fg_color="#00FF66",command=elimDatos,
                                       font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")

botonElimDatos.place(x=1100,y=550)

particulas=customtkinter.CTkLabel(ventana,width=150,height=50,text="Humedad (%)",font=('Consolas',40))
particulas.place(x=700,y=50)

particulas1=customtkinter.CTkLabel(ventana,width=150,height=50,text=" ",font=('Consolas',40))
particulas1.place(x=700,y=250)

velocidadB=customtkinter.CTkSlider(ventana,orientation="vertical",from_=0,to=100,number_of_steps=100,command=confVelB)
velocidadB.place(x=1100,y=75)

tolHum=customtkinter.CTkSlider(ventana,orientation="vertical",from_=0,to=100,number_of_steps=100,command=confUmbral)
tolHum.place(x=1250,y=75)

Bomba=customtkinter.CTkLabel(ventana,width=100,height=50,text=f'Umbral={int(tolHum.get())}%',font=('Consolas',30))
Bomba.place(x=300,y=450)

Bombav=customtkinter.CTkLabel(ventana,width=100,height=50,text=f'Velociadad={int(velocidadB.get())}%',font=('Consolas',30))
Bombav.place(x=550,y=450)

valorH=customtkinter.CTkLabel(ventana,width=350,height=50,text=" ",bg_color="Green")
valorH.place(x=700,y=100)


#Grafica

grafica=FigureCanvasTkAgg(figura,master=ventana)
grafica._tkcanvas.grid(row = 1,column = 2, padx=1,pady=1)
grafica.get_tk_widget().place(x=300, y=200, anchor='w')

ventana.mainloop()