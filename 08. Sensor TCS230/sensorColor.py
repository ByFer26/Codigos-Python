import customtkinter
import serial
import serial.tools.list_ports
from CTkSpinbox import *
from datetime import datetime
import numpy as np
from TCS230DB import *

estadoPuerto=1

valor1="0,0,0"
valor2="0,0,0"
valor3="0,0,0"
valor4="0,0,0"
valor5="0,0,0"
valor6="0,0,0"
estadoComp=0
estadoHilo=0
num1=[]
num2=[]
num3=[]
num4=[]
num5=[]
num6=[]
numA=[]
valorActual="0,0,0"

def comparar():
    global valor1,valor2,valor3,valor4,valor5,valor6
    experimental=recepcionDatos()

    def seleccionObjeto(datoEntrada,tolerancia):
        objeto=6
        matriz=np.zeros((6,3))
        datosE=np.zeros((1,3))
        for i in range(1,7):
            variable=f'valor{i}'
            variable=eval(variable)
            datos=variable.split(',')
            datoEntrada1=datoEntrada.split(',')
            for j in range(0,3):
                matriz[i-1,j]=float(datos[j])
                datosE[0,j]=float(datoEntrada1[j])

        for k in range(0,6):
            resta=matriz[k,0]-datosE[0,0]
            if abs(resta)<=tolerancia:
                if abs(matriz[k,1]-datosE[0,1])<=tolerancia:
                    if abs(matriz[k,2]-datosE[0,2])<=tolerancia:
                        objeto=k
                        continue
            

        return (objeto+1)
    
    objeto=seleccionObjeto(experimental,int(tolerancia.get()))

    for z in range(1,7):
        cuadro1=f'alerta{z}'
        cuadro1=eval(cuadro1)
        botonS=f'botonObjeto{z}'
        botonS=eval(botonS)
        if z==objeto:
            cuadro1.configure(bg_color="#00FF00")
            insertarDatos("TCS230","Objeto","Estado","Hora",str(botonS.cget("text")),"Detectado",str(datetime.now()))
        else:
            cuadro1.configure(bg_color="#FF0000")

    if objeto==7:
        for m in range(1,7):
            cuadro=f'alerta{m}'
            cuadro=eval(cuadro)
            cuadro.configure(bg_color="#FF0000")



def salir():
    ventana.destroy()
    ventana.quit()
    ESP32.close()

def asignarValores(parametro,valor):
    global valor1,valor2,valor3,valor4,valor5,valor6
    valnum=f'num{parametro}'
    valNum=eval(valnum)
    elementos=valor.split(',')
    valNum.append(elementos[0])
    valNum.append(elementos[1])
    valNum.append(elementos[2])
    if parametro==1:
        valor1=valor
    if parametro==2:
        valor2=valor
    if parametro==3:
        valor3=valor
    if parametro==4:
        valor4=valor
    if parametro==5:
        valor5=valor
    if parametro==6:
        valor6=valor

def recepcion():
    condicion=True
    ESP32.reset_input_buffer()
    while condicion:
        try:
            datos=ESP32.readline().decode('utf-8').replace('\r\n', '')
            condicion=False
        except ValueError or UnicodeDecodeError:
            pass

        except IndexError:
            pass

    return datos

def recepcionDatos():
    condicion=True
    global valorActual
    envio="a"
    envio=bytes(envio,'utf-8')
    ESP32.write(envio)
    valorActual=recepcion()
    return valorActual
 

def configurarObjeto(parametro):
    global num1,num2,num3,num4,num5,num6

    def recuperarInfo(parametro1):
        etiqueta=f'valor{parametro1}'
        etiq=eval(etiqueta)
        if etiq=="0,0,0":
         pass
        if etiq!="0,0,0":
            elementos1=etiq.split(',')
            R1=elementos1[0]
            G1=elementos1[1]
            B1=elementos1[2]
            valorC.configure(text=f'R={R1} G={G1} B={B1}',font=('Consolas',20))


    def configurar():
        boton=f'botonObjeto{str(parametro)}'
        objeto=eval(boton)
        objeto.configure(text=f'Objeto {parametro}: {nombre1.get("1.0", "end")}')

    def insertarTexto():
       # ESP32.write(b'c')
        ESP32.write(b'a')
        valor=recepcion()
        elementos=valor.split(',')
        R=elementos[0]
        G=elementos[1]
        B=elementos[2]
        valorC.configure(text=f'R={R} G={G} B={B}',font=('Consolas',20))
        asignarValores(parametro,valor)


    nuevaVentana=customtkinter.CTkToplevel(ventana)
    nuevaVentana.geometry("400x300")
    nuevaVentana.title(f'Configuración objeto {str(parametro)}')
    botonConf1=customtkinter.CTkButton(nuevaVentana,text="Configurar objeto",command=configurar)
    botonConf1.place(x=10,y=250)
    botonObtenerDatos=customtkinter.CTkButton(nuevaVentana,text="Obtener datos",command=insertarTexto)
    botonObtenerDatos.place(x=250,y=250)
    nombre1=customtkinter.CTkTextbox(nuevaVentana,font=('Consolas',20),height=30,width=200)
    nombre1.place(x=100,y=150)
    etiqueta1=customtkinter.CTkLabel(nuevaVentana,text="Nombre del objeto")
    etiqueta1.place(x=150,y=120)
    etiqueta2=customtkinter.CTkLabel(nuevaVentana,text="Valor sensor color")
    etiqueta2.place(x=150,y=10)
    valorC=customtkinter.CTkLabel(nuevaVentana,text="")
    valorC.place(x=65,y=50)
    recuperarInfo(parametro)

        
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
        crearTabla("TCS230","Objeto","Estado","Hora")
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


def confTol(self):
    tol1.configure(text=f'{tolerancia.get()}')

def genPDF():
    generarPDF("TCS230","Objetos_detectados")

def elimDatos():
    eliminarDatos("TCS230")


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue") 

ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Sensor TCS230")

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

botonObjeto1=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 1",command=lambda:configurarObjeto(1))
botonObjeto1.place(x=350,y=50)

botonObjeto2=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 2",command=lambda:configurarObjeto(2))
botonObjeto2.place(x=350,y=140)

botonObjeto3=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 3",command=lambda:configurarObjeto(3))
botonObjeto3.place(x=350,y=240)

botonObjeto4=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 4",command=lambda:configurarObjeto(4))
botonObjeto4.place(x=350,y=340)

botonObjeto5=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 5",command=lambda:configurarObjeto(5))
botonObjeto5.place(x=350,y=440)

botonObjeto6=customtkinter.CTkButton(ventana,width=150,height=30,text="Configurar objeto 6",command=lambda:configurarObjeto(6))
botonObjeto6.place(x=350,y=540)

alerta1=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta1.place(x=700,y=50)

alerta2=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta2.place(x=700,y=140)

alerta3=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta3.place(x=700,y=240)

alerta4=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta4.place(x=700,y=340)

alerta5=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta5.place(x=700,y=440)

alerta6=customtkinter.CTkLabel(ventana,bg_color="#FF0000",text="",width=100,height=40)
alerta6.place(x=700,y=540)

botonComparar=customtkinter.CTkButton(ventana,width=150,height=30,text="Comparar",font=('helvetica',20),corner_radius=6,fg_color="#226103",
                                      command=comparar)
botonComparar.place(x=1100,y=50)

botonGenPDF=customtkinter.CTkButton(ventana,width=150,height=30,text="Generar PDF",font=('helvetica',20),corner_radius=6,fg_color="#226103",command=genPDF)
botonGenPDF.place(x=1100,y=140)

botonBorrar=customtkinter.CTkButton(ventana,width=150,height=30,text="Borrar datos",font=('helvetica',20),corner_radius=6,fg_color="#226103",command=elimDatos)
botonBorrar.place(x=1100,y=240)

botonSalir=customtkinter.CTkButton(ventana,width=150,height=30,text="Salir",font=('helvetica',20),corner_radius=6,fg_color="#226103",
                                   command=salir)
botonSalir.place(x=1100,y=340)

tol=customtkinter.CTkLabel(ventana,text="Tolerancia: ",font=('Consolas',20))
tol.place(x=1080,y=450)

tol1=customtkinter.CTkLabel(ventana,text="",font=('Consolas',20))
tol1.place(x=1220,y=450)

tolerancia=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=10,number_of_steps=10,command=confTol)
tolerancia.place(x=1080,y=500)


ventana.mainloop()