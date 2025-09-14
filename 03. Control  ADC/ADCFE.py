from ADCBE import *
import matplotlib.pyplot as plt
import matplotlib.animation as animacion
from threading import Thread
import threading
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


dato1=0
dato2=0
recepcionC=True
graficaC=True
x1=[]
x2=[]


pararHilo=threading.Event()

def Iniciar():
    global anim
    global graficaC
    global x1,x2
    x1=crearArreglos(muestreo1.get())
    x2=crearArreglos(muestreo2.get())
    while graficaC:
        try:
            hilo.start()
            graficaC=False
        except:
            pass
    
    anim = animacion.FuncAnimation(figura, graficar,  fargs=(linea1,linea2,muestreo1.get(),muestreo2.get(),
                                                             x1,x2),interval = 1, blit = False )
    grafica.draw()


def recepcion():
    global recepcionC
    while recepcionC:
        global dato1,dato2
        dato1,dato2=obtenerDatos(conectar(puertoSerial.get(),baudios.get()))
        vol1.set(str(dato1)+"VDC")
        vol2.set(str(dato2)+"VDC")
        if pararHilo.is_set():
            recepcionC=False
            
            
hilo=Thread(target=recepcion)

def graficar(self,linea1,linea2,longitud1,longitud2,arr1,arr2):
    arr1=insertarDatos(arr1,dato1,longitud1)
    arr2=insertarDatos(arr2,dato2,longitud2)
    linea1.set_data(range(longitud1), arr1)
    linea2.set_data(range(longitud2), arr2)

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

def Salir():
    recepcionC=False
    hilo.join()
    ventana.destroy()
    ventana.quit()

def actualizar1(self):
    parar()
    eje1.set_xlim(0,muestreo1.get())
    x1=crearArreglos(muestreo1.get())
    x1.clear()
    reanudar()


def actualizar2(self):
    parar()
    eje2.set_xlim(0,muestreo2.get())
    x2=crearArreglos(muestreo2.get())
    x2.clear()
    reanudar()

figura, (eje1,eje2)=plt.subplots(2,1)
figura.set_size_inches(8,5)
figura.set_facecolor('#4F406A')
figura.tight_layout(pad=2)
eje1.set_facecolor('000000')
eje2.set_facecolor('000000')
eje1.set_xlim(0,10)
eje2.set_xlim(0,10)
eje1.set_ylim(-1,4)
eje2.set_ylim(-1,4)
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


#Creación de la interfaz en tkinter
ventana=Tk()
ventana.geometry("1550x650")
ventana.configure(bg='#4F406A')
ventana.title("Control de ADC")

#Opciones de puerto
puertoSerial=StringVar(ventana)
puertoSerial.set("Puertos")
listaPuertos=listadoPuertos()
opcionesPuertos=OptionMenu(ventana,puertoSerial,*listaPuertos)
opcionesPuertos.configure(font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
opcionesPuertos.place(x=50,y=50,width=150,height=60)

#Opciones de baudios
baudios=IntVar(ventana)
baudios.set("Baudios")
listaBaudios=[4800,9600,31250,38400,57600,196200,230400]
opcionesBaudios=OptionMenu(ventana,baudios,*listaBaudios)
opcionesBaudios.configure(font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
opcionesBaudios.place(x=50,y=200,width=150,height=60)

#Escala 1
muestreo1=Scale(ventana,from_=10,to=200,orient='horizontal',length=200,command=actualizar1,
                font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
muestreo1.place(x=1100,y=150)

#Escala 2
muestreo2=Scale(ventana,from_=10,to=200,orient='horizontal',length=200,command=actualizar2,
                font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
muestreo2.place(x=1100,y=350)

#Salir
botonSalir=Button(ventana,text="Salir",command=Salir,
                  font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
botonSalir.place(x=940,y=550,width=150,height=60)

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

#Iniciar
botonIniciar=Button(ventana,text="Iniciar",command=Iniciar,
                    font=('Qanelas Heavy',16),bg='#53107E',fg='#FFFFFF')
botonIniciar.place(x=140,y=550,width=100,height=60)

#Grafica

grafica=FigureCanvasTkAgg(figura,master=ventana)
grafica._tkcanvas.grid(row = 1,column = 2, padx=1,pady=1)
grafica.get_tk_widget().place(x=250, y=250, anchor='w')

ventana.mainloop()