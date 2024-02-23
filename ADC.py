import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from threading import Thread
from tkinter import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial.tools.list_ports

condDatos = True 
condGrafica=True
condSerial=True
condArreglos=True
condCrearGrafica=True
datos= 0.0
datos1= 0.0
datos2= 0.0
puerto=""
baud=0
mues1=200
mues2=200

#Figura en matplotlib y sus configuraciones
figura, (eje1,eje2)=plt.subplots(2,1)
figura.set_size_inches(8,5)
figura.set_facecolor('#4F406A')
figura.tight_layout(pad=2)
eje1.set_facecolor('000000')
eje2.set_facecolor('000000')
eje1.set_ylim(-1,4)
eje2.set_ylim(-1,4)
eje1.set_xlim(0,mues1)
eje2.set_xlim(0,mues2)
eje1.set_xlabel('Tiempo (ms)')
eje2.set_xlabel('Tiempo (ms)')
eje1.set_ylabel('Voltaje (V)')
eje2.set_ylabel('Voltaje (V)')
eje1.grid()
eje2.grid()
linea1=eje1.plot([], [])[0]
linea1.set_color('#45D115')
linea2=eje2.plot([], [])[0]
linea2.set_color('#45D115')

try:
    ESP32=serial.Serial(puerto,baud,timeout=1)
except:
    pass

def detectarPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

def Salir():
    global condGrafica
    global condArreglos
    global condCrearGrafica
    global condSerial
    condGrafica=False
    condSerial=False
    ventana.destroy()
    ventana.quit()
    
    
def parar():
    try:
        anim.event_source.stop()
    except NameError:
        pass

def reanudar():
    try:
        anim.event_source.start()
    except NameError:
        pass


def Actualizar1(self):
    global data1
    try:
        data1.clear()
        for i in range(0,round(muestreo1.get()+1,0)):
            data1.append(0)
        eje1.set_xlim(0,muestreo1.get())
    except NameError:
        pass

def Actualizar2(self):
    global data2
    try:
        data2.clear()
        for i in range(0,muestreo2.get()+1):
            data2.append(0)
        eje2.set_xlim(0,muestreo2.get())
    except NameError:
        pass


def obtenerDatos():
    time.sleep(1)
    global condSerial
    puerto=puertoSerial.get()
    puerto=puerto.replace('(','')
    puerto=puerto.replace(')','')
    puerto=puerto.replace("'",'')
    puerto=puerto.replace(',','')
    baud=baudios.get()
    while(condSerial):
        try:
            ESP32=serial.Serial(puerto,baud,timeout=1)
            condSerial=False
        except:
            pass
    ESP32.reset_input_buffer()
    while (condGrafica):
        global datos
        global datos1
        global datos2
        try:
            datos=ESP32.readline().decode('utf-8').replace('\r\n', '')
            datos=datos.split(",")
            datos1=float(datos[0])
            datos2=float(datos[1])
            datos1=round((datos1*3.3)/4096,2)
            datos2=round((datos2*3.3)/4096,2)
            vol1.set(str(datos1)+"VDC")
            vol2.set(str(datos2)+"VDC")
        except ValueError or UnicodeDecodeError:
            pass
        except IndexError:
            pass



def graficarDatos(self,lines1,lines2):
    global condArreglos
    global data1
    global data2
    while(condArreglos):
        try:
            data1 = []
            data2 = []
            for i in range(0,muestreo1.get()):
                data1.append(0)
            for j in range(0,muestreo2.get()):
                data2.append(0)
            condArreglos=False
        except:
            pass
    if len(data1)>muestreo1.get():
        data1.pop(0)
    
    if len(data2)>muestreo2.get():
        data2.pop(0)
    data1.append(datos1)
    data2.append(datos2)
    print(data1)
    print(data2)
    try:
        lines1.set_data(range(len(data1)), data1)
        lines2.set_data(range(len(data2)), data2)
    except ValueError:
        pass

hiloSecundario=Thread(target=obtenerDatos) #Creación del hilo secundario para obtener datos


def Iniciar():
    global condCrearGrafica
    global data1
    global data2
    global anim
    while(condCrearGrafica):
        try:
            time.sleep(1)
            eje1.set_xlim(0,muestreo1.get())
            eje2.set_xlim(0,muestreo1.get())
            condCrearGrafica=False
        except:
            pass

    hiloSecundario.start()
    anim=animacion.FuncAnimation(figura,graficarDatos,fargs=(linea1,linea2),
                                    interval = 100, blit = False)
    grafica.draw()

#Creación de la interfaz en tkinter
ventana=Tk()
ventana.geometry("1500x650")
ventana.configure(bg='#4F406A')
ventana.title("Control de ADC")

#Opciones de puerto
puertoSerial=StringVar(ventana)
puertoSerial.set("Puertos")
listaPuertos=detectarPuertos()
opcionesPuertos=OptionMenu(ventana,puertoSerial,*listaPuertos)
opcionesPuertos.configure(font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
opcionesPuertos.place(x=50,y=50,width=150,height=60)


#Opciones de baudios
baudios=IntVar(ventana)
baudios.set("Baudios")
listaBaudios=[4800,9600,196200,31250,38400,57600]
opcionesBaudios=OptionMenu(ventana,baudios,*listaBaudios)
opcionesBaudios.configure(font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
opcionesBaudios.place(x=50,y=200,width=150,height=60)

#Iniciar
botonIniciar=Button(ventana,text="Iniciar",command=Iniciar,
                    font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
botonIniciar.place(x=140,y=550,width=100,height=60)

#Escala 1
muestreo1=Scale(ventana,from_=10,to=200,orient='horizontal',length=200,command=Actualizar1,
                font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
muestreo1.place(x=1100,y=150)

#Escala 2
muestreo2=Scale(ventana,from_=10,to=200,orient='horizontal',length=200,command=Actualizar2,
                font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
muestreo2.place(x=1100,y=350)

#Salir
botonSalir=Button(ventana,text="Salir",command=Salir,
                  font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
botonSalir.place(x=940,y=550,width=150,height=60)

#Grafica

grafica=FigureCanvasTkAgg(figura,master=ventana)
grafica._tkcanvas.grid(row = 1,column = 2, padx=1,pady=1)
grafica.get_tk_widget().place(x=250, y=250, anchor='w')


#Etiqueta Voltaje 1
nombre1=Label(ventana,text="Canal 1",
              font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
nombre1.place(x=1100,y=100)
vol1=StringVar(ventana)
voltaje1=Label(ventana,textvariable=vol1,
               font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
voltaje1.place(x=1200,y=100)

#Etiqueta Voltaje 2
nombre2=Label(ventana,text="Canal 2",
              font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
nombre2.place(x=1100,y=300)
vol2=StringVar(ventana)
voltaje2=Label(ventana,textvariable=vol2,
               font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
voltaje2.place(x=1200,y=300)

#Boton pausar
pausar=Button(ventana,text="Pausar",command=parar,
              font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
pausar.place(x=406,y=550,width=150,height=60)

#Boton reanudar
regresar=Button(ventana,text="Reanudar",command=reanudar,
                font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
regresar.place(x=663,y=550,width=150,height=60)

ventana.mainloop()