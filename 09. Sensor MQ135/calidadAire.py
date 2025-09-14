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
from MQ135DB import *

estadoPuerto=1
recepcionC=True
estadoHilo=1
x1=[]
dato1=0
ppm=0
alarmaP=0
toleranciaP=0

def confAlarmas(self):
    global alarmaP,toleranciaP
    labelAlarmas.configure(text=f'{int(alarmasppm.get())}±{int(tolerancia.get())}')
    alarmaP=int(alarmasppm.get())
    toleranciaP=int(tolerancia.get())

def comparacion(valor,alarma,tolerancia1):
    limiteInferior=alarma-tolerancia1
    limiteSuperior=alarma+tolerancia1
    if limiteInferior<valor<limiteSuperior:
        print("Alarma")
        indicador.configure(bg_color="red")
        insertarDatos("MQ135", "PPM", "Hora",str(ppm),str(datetime.now()))
    else:
        indicador.configure(bg_color="green")   
        
def eliminarT():
    eliminarDatos("MQ135")	    

def genPD():
    generarPDF("MQ135","Sensor particulas")

def imprimir(self):
    print(int(alarmasppm.get()))
    print(int(tolerancia.get()))

def calcular_ppm(vout):
    rs = 10000 * (5.0 - vout) / vout
    ratio = rs / 10000
    A = 116.6020682
    B = 2.769034857
    ppm = A * (ratio ** -B)
    return ppm

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
    arr1=insertarDatosR(arr1,float(ppm/1000))
    linea1.set_data(range(100), arr1)


def confVel(self):
    labelVelocidad.configure(text=f"{int(velocidadT.get())}")

def confPin(self):
    labelPin.configure(text=f"{int(pinESP.get())}")

def iniciar():
    global estadoHilo
    global x1
    envio=f'a${str(round(velocidadT.get(),0))}${str(round(pinESP.get(),0))}\n'
    x1=crearArreglos(100)
    envio=bytes(envio,'utf-8')
    for i in range(0,3):
        ESP32.write(envio)
        time.sleep(0.5)
    if estadoHilo==1:
        hilo.start()
        estadoHilo=2
    else:
        pass

    anim = animacion.FuncAnimation(figura, graficar,  fargs=(linea1,x1),interval = 1, blit = False )
    grafica.draw()

def parar():
    envio=f'b${str(round(velocidadT.get(),0))}${str(round(pinESP.get(),0))}\n'
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
            dato1=(dato1/4095)*5
            if float(dato1)==0.0:
                dato1=0.1
            ppm=(10000*(5.0-dato1))/(dato1)
            ppm=ppm/10000
            if ppm==0.0:
                ppm=0.1
            ppm=116.6020682*(ppm**-2.769034857)
            particulas1.configure(text=f'{round(float(ppm),3)}')
            comparacion(ppm,alarmaP,toleranciaP)
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
        crearTabla("MQ135","PPM","Hora")
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
    generarPDF("MQ135","Gases detectados")

def elimDatos():
    eliminarDatos("MQ135")

figura, (eje1)=plt.subplots(1,1)
figura.set_size_inches(4,4)
figura.set_facecolor("#F9FD84")
figura.tight_layout(pad=2)
eje1.tick_params(colors='#000000')
eje1.set_facecolor("#F9FD84")
eje1.set_xlim(0,100)
eje1.set_ylim(0,80)
eje1.set_ylabel('PPM (x1000)',color='#000000')
eje1.grid()
linea1=eje1.plot([], [])[0]
linea1.set_color('#0000FF')




ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Sensor MQ135")

ventana.configure(fg_color="#F9FD84")

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

botonIniciar=customtkinter.CTkButton(ventana,text="Iniciar",width=150,height=30,corner_radius=6,fg_color="#FFF200",command=iniciar,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonIniciar.place(x=1125,y=50)

botonSalir=customtkinter.CTkButton(ventana,text="Salir",width=150,height=30,corner_radius=6,fg_color="#FFF200",command=salir,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonSalir.place(x=1125,y=150)

botonParar=customtkinter.CTkButton(ventana,text="Parar",width=150,height=30,corner_radius=6,fg_color="#FFF200",command=parar,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonParar.place(x=1125,y=250)

velocidadT=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=1,to=1000,number_of_steps=999,command=confVel)
velocidadT.place(x=300,y=75)

label1=customtkinter.CTkLabel(ventana,width=100,height=50,text="Velocidad (ms)",font=('Consolas',20))
label1.place(x=320,y=25)

labelVelocidad=customtkinter.CTkLabel(ventana,text="",fg_color="transparent",font=('Consolas',20))
labelVelocidad.place(x=500,y=37)

pinESP=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=1,to=39,number_of_steps=38,command=confPin)
pinESP.place(x=600,y=75)

label2=customtkinter.CTkLabel(ventana,width=100,height=50,text="Pin Lectura",font=('Consolas',20))
label2.place(x=620,y=25)

labelPin=customtkinter.CTkLabel(ventana,text="",fg_color="transparent",font=('Consolas',20))
labelPin.place(x=800,y=37)

botonGenPDF=customtkinter.CTkButton(ventana,text="Generar PDF",width=150,height=30,corner_radius=6,fg_color="#FFF200",command=genPD,
                                     font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")
botonGenPDF.place(x=1125,y=350)

botonElimDatos=customtkinter.CTkButton(ventana,text="Eliminar Datos",width=150,height=30,corner_radius=6,fg_color="#FFF200",command=eliminarT,
                                       font=('Consolas',20),text_color="#000000",border_width=2,border_color="#000000")

botonElimDatos.place(x=1125,y=450)

particulas=customtkinter.CTkLabel(ventana,width=150,height=50,text="PPM (CO2)",font=('Consolas',40))
particulas.place(x=700,y=150)

particulas1=customtkinter.CTkLabel(ventana,width=150,height=50,text=" ",font=('Consolas',40))
particulas1.place(x=700,y=250)

tolerancia=CTkSpinbox(ventana,width=180,height=50,min_value=1,start_value=100,max_value=10000,step_value=100,font=('consolas',20),command=confAlarmas)
tolerancia.place(x=300,y=500)

alarmasppm=CTkSpinbox(ventana,width=180,height=50,min_value=500,start_value=500,max_value=70000,step_value=500,font=('consolas',20),command=confAlarmas)
alarmasppm.place(x=550,y=500)

labelAlarmas=customtkinter.CTkLabel(ventana,width=150,height=50,text="500±500",font=('Consolas',30))
labelAlarmas.place(x=800,y=500)

indicador=customtkinter.CTkLabel(ventana,width=100,height=50,text=" ",bg_color="green")
indicador.place(x=700,y=300)

#Grafica

grafica=FigureCanvasTkAgg(figura,master=ventana)
grafica._tkcanvas.grid(row = 1,column = 2, padx=1,pady=1)
grafica.get_tk_widget().place(x=300, y=300, anchor='w')

ventana.mainloop()
