import customtkinter
from tkinter import*
import serial
import serial.tools.list_ports
from threading import Thread
from baseDatosPines import*
from datetime import datetime

recepcionC=True
condE11=True
condE12=True
condE21=True
condE22=True
condE31=True
condE32=True
condE41=True
condE42=True
condE51=True
condE52=True
condE61=True
condE62=True
condE71=True
condE72=True
condE81=True
condE82=True

try:
    ESP32=serial.Serial("NADA",0)

except:
    pass

def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos


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

def obtenerDatos(dispositivo):
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

def recepcion():
    global recepcionC
    global condE11,condE12,condE21,condE22,condE31,condE32,condE41,condE42
    global condE51,condE52,condE61,condE62,condE71,condE72,condE81,condE82
    while recepcionC:
        datos=obtenerDatos(ESP32)
        try:
            if datos[7]=="1":
                estado1.configure(fg_color="#0FFF00")
                while condE11==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 1',str(datetime.now()),'Alto')
                    condE11=False
                    condE12=True
            if datos[7]=="0":
                estado1.configure(fg_color="#FF0000")
                while condE12==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 1',str(datetime.now()),'Bajo')
                    condE12=False
                    condE11=True
            if datos[6]=="1":
                estado2.configure(fg_color="#0FFF00")
                while condE21==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 2',str(datetime.now()),'Alto')
                    condE21=False
                    condE22=True
            if datos[6]=="0":
                estado2.configure(fg_color="#FF0000")
                while condE22==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 2',str(datetime.now()),'Bajo')
                    condE22=False
                    condE21=True
            if datos[5]=="1":
                estado3.configure(fg_color="#0FFF00")
                while condE31==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 3',str(datetime.now()),'Alto')
                    condE31=False
                    condE32=True
            if datos[5]=="0":
                estado3.configure(fg_color="#FF0000")
                while condE32==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 3',str(datetime.now()),'Bajo')
                    condE32=False
                    condE31=True
            if datos[4]=="1":
                estado4.configure(fg_color="#0FFF00")
                while condE41==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 4',str(datetime.now()),'Alto')
                    condE41=False
                    condE42=True
            if datos[4]=="0":
                estado4.configure(fg_color="#FF0000")
                while condE42==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 4',str(datetime.now()),'Bajo')
                    condE42=False
                    condE41=True
            if datos[3]=="1":
                estado5.configure(fg_color="#0FFF00")
                while condE51==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 5',str(datetime.now()),'Alto')
                    condE51=False
                    condE52=True
            if datos[3]=="0":
                estado5.configure(fg_color="#FF0000")
                while condE52==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 5',str(datetime.now()),'Bajo')
                    condE52=False
                    condE51=True
            if datos[2]=="1":
                estado6.configure(fg_color="#0FFF00")
                while condE61==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 6',str(datetime.now()),'Alto')
                    condE61=False
                    condE62=True
            if datos[2]=="0":
                estado6.configure(fg_color="#FF0000")
                while condE62==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 6',str(datetime.now()),'Bajo')
                    condE62=False
                    condE61=True
            if datos[1]=="1":
                estado7.configure(fg_color="#0FFF00")
                while condE71==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 7',str(datetime.now()),'Alto')
                    condE71=False
                    condE72=True
            if datos[1]=="0":
                estado7.configure(fg_color="#FF0000")
                while condE72==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 7',str(datetime.now()),'Bajo')
                    condE72=False
                    condE71=True
            if datos[0]=="1":
                estado8.configure(fg_color="#0FFF00")
                while condE81==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 8',str(datetime.now()),'Alto')
                    condE81=False
                    condE82=True
            if datos[0]=="0":
                estado8.configure(fg_color="#FF0000")
                while condE82==True:
                    insertarDatos("Entradas","Entrada","Hora","Estado",'Entrada 8',str(datetime.now()),'Bajo')
                    condE82=False
                    condE81=True
        except IndexError:
            pass
   
hilo=Thread(target=recepcion)

def envio(tipo):
        if tipo==1:
            if led1check.get()==1:
                ESP32.write(b'A')
                insertarDatos("Salidas","salida","Hora","Estado",'Led 1',str(datetime.now()),'Encendido')
            if led1check.get()==2:
                ESP32.write(b'a')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 1',str(datetime.now()),'Apagado')
        if tipo==2:
            if led2check.get()==1:
                ESP32.write(b'B')    
                insertarDatos("Salidas","salida","Hora","Estado",'Led 2',str(datetime.now()),'Encendido')
            if led2check.get()==2:
                ESP32.write(b'b')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 2',str(datetime.now()),'Apagado')
        if tipo==3:
            if led3check.get()==1:
                ESP32.write(b'C')
                insertarDatos("Salidas","salida","Hora","Estado",'Led 3',str(datetime.now()),'Encendido')
            if led3check.get()==2:
                ESP32.write(b'c')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 3',str(datetime.now()),'Apagado')
        if tipo==4:
            if led4check.get()==1:
                ESP32.write(b'D')    
                insertarDatos("Salidas","salida","Hora","Estado",'Led 4',str(datetime.now()),'Encendido')
            if led4check.get()==2:
                ESP32.write(b'd')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 4',str(datetime.now()),'Apagado')
        if tipo==5:
            if led5check.get()==1:
                ESP32.write(b'E')
                insertarDatos("Salidas","salida","Hora","Estado",'Led 5',str(datetime.now()),'Encendido')
            if led5check.get()==2:
                ESP32.write(b'e')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 5',str(datetime.now()),'Apagado')
        if tipo==6:
            if led6check.get()==1:
                ESP32.write(b'F')    
                insertarDatos("Salidas","salida","Hora","Estado",'Led 6',str(datetime.now()),'Encendido')
            if led6check.get()==2:
                ESP32.write(b'f')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 6',str(datetime.now()),'Apagado')
        if tipo==7:
            if led7check.get()==1:
                ESP32.write(b'G')
                insertarDatos("Salidas","salida","Hora","Estado",'Led 7',str(datetime.now()),'Encendido')
            if led7check.get()==2:
                ESP32.write(b'g')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 7',str(datetime.now()),'Apagado')
        if tipo==8:
            if led8check.get()==1:
                ESP32.write(b'H')    
                insertarDatos("Salidas","salida","Hora","Estado",'Led 8',str(datetime.now()),'Encendido')
            if led8check.get()==2:
                ESP32.write(b'h')
                insertarDatos("Salidas","Salida","Hora","Estado",'Led 8',str(datetime.now()),'Apagado')
                


try:
    crearTabla("Salidas","Salida","Hora","Estado")
except:
    pass
try:
    crearTabla("Entradas","Entrada","Hora","Estado")
except:
    pass

def eliminarDatosI(tabla1,tabla2):
    eliminarDatos(tabla1)
    eliminarDatos(tabla2)

def generarReporte():
    generarPDF("Entradas","Entradas")
    generarPDF("Salidas","Salidas")

def salir():
    ventana.destroy()
    ventana.quit()

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("colores.json")  # Themes: "blue" (standard), "green", "dark-blue

ventana=customtkinter.CTk()
ventana.geometry(f"{1100}x{580}")
ventana.title("Control de puertos")

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

botonConectar=customtkinter.CTkButton(ventana,width=150,height=50,text="Conectar",command=conectar,font=('helvetica',18))
botonConectar.place(x=75,y=450)

led1check=customtkinter.IntVar()
led1=customtkinter.CTkCheckBox(ventana,text="Led 1",variable=led1check,onvalue=1,offvalue=2,command=lambda:envio(1),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led1.place(x=400,y=14)

led2check=customtkinter.IntVar()
led2=customtkinter.CTkCheckBox(ventana,text="Led 2",variable=led2check,onvalue=1,offvalue=2,command=lambda:envio(2),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led2.place(x=400,y=82)

led3check=customtkinter.IntVar()
led3=customtkinter.CTkCheckBox(ventana,text="Led 3",variable=led3check,onvalue=1,offvalue=2,command=lambda:envio(3),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led3.place(x=400,y=150)

led4check=customtkinter.IntVar()
led4=customtkinter.CTkCheckBox(ventana,text="Led 4",variable=led4check,onvalue=1,offvalue=2,command=lambda:envio(4),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led4.place(x=400,y=218)

led5check=customtkinter.IntVar()
led5=customtkinter.CTkCheckBox(ventana,text="Led 5",variable=led5check,onvalue=1,offvalue=2,command=lambda:envio(5),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led5.place(x=400,y=286)

led6check=customtkinter.IntVar()
led6=customtkinter.CTkCheckBox(ventana,text="Led 6",variable=led6check,onvalue=1,offvalue=2,command=lambda:envio(6),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led6.place(x=400,y=354)

led7check=customtkinter.IntVar()
led7=customtkinter.CTkCheckBox(ventana,text="Led 7",variable=led7check,onvalue=1,offvalue=2,command=lambda:envio(7),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led7.place(x=400,y=422)

led8check=customtkinter.IntVar()
led8=customtkinter.CTkCheckBox(ventana,text="Led 8",variable=led8check,onvalue=1,offvalue=2,command=lambda:envio(8),
                              checkbox_height=40,checkbox_width=40,font=('helvetica',18))
led8.place(x=400,y=490)

##########################################################################################################

estado1=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado1.place(x=900,y=14)

estado2=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado2.place(x=900,y=82)

estado3=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado3.place(x=900,y=150)

estado4=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado4.place(x=900,y=218)

estado5=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado5.place(x=900,y=286)

estado6=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado6.place(x=900,y=354)

estado7=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado7.place(x=900,y=422)

estado8=customtkinter.CTkLabel(ventana,text=" ",width=40,height=40,fg_color="#FF0000")
estado8.place(x=900,y=490)

entrada1=customtkinter.CTkLabel(ventana,text="Entrada 1",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada1.place(x=950,y=14)

entrada2=customtkinter.CTkLabel(ventana,text="Entrada 2",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada2.place(x=950,y=82)

entrada3=customtkinter.CTkLabel(ventana,text="Entrada 3",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada3.place(x=950,y=150)

entrada4=customtkinter.CTkLabel(ventana,text="Entrada 4",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada4.place(x=950,y=218)

entrada5=customtkinter.CTkLabel(ventana,text="Entrada 5",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada5.place(x=950,y=286)

entrada6=customtkinter.CTkLabel(ventana,text="Entrada 6",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada6.place(x=950,y=354)

entrada7=customtkinter.CTkLabel(ventana,text="Entrada 7",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada7.place(x=950,y=422)

entrada8=customtkinter.CTkLabel(ventana,text="Entrada 8",font=('helvetica',18),fg_color="transparent",width=40,height=40)
entrada8.place(x=950,y=490)

############################################################################################################################

borrarDB=customtkinter.CTkButton(ventana,width=150,height=50,text="Borrar datos",command=lambda:eliminarDatosI("Entradas","Salidas"),
                                 font=('helvetica',18))
borrarDB.place(x=600,y=500)

salirB=customtkinter.CTkButton(ventana,width=150,height=50,text="Salir",command=salir,font=('helvetica',18))
salirB.place(x=600,y=300)

verDatos=customtkinter.CTkButton(ventana,width=150,height=50,text="Generar reporte",command=generarReporte,
                                 font=('helvetica',18))
verDatos.place(x=600,y=400)

ventana.mainloop()