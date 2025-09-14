import customtkinter
from tkinter import*
import serial
import serial.tools.list_ports
import datetime
from threading import Thread
from CTkSpinbox import *

bitsResolucion=2
valoresResolucion=(2**2)-1

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
        except:
            pass
            print("Error de conexión")
    return ESP32

def confCiclo(canal):
    if canal==1:
        envio=f"canal1$ciclo${int(ciclo1.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==2:
        envio=f"canal2$ciclo${int(ciclo2.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==3:
        envio=f"canal3$ciclo${int(ciclo3.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==4:
        envio=f"canal4$ciclo${int(ciclo4.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

def confPWM(canal):
    if canal==1:
        ciclo1.configure(to=((2**int(resolucion1.get()))-1),number_of_steps=((2**int(resolucion1.get()))-1))
        envio=f"canal1${int(frecuencia1.get())},{int(pin1.get())},{int(resolucion1.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==2:
        ciclo2.configure(to=((2**int(resolucion2.get()))-1),number_of_steps=((2**int(resolucion2.get()))-1))
        envio=f"canal2${int(frecuencia2.get())},{int(pin2.get())},{int(resolucion2.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==3:
        ciclo3.configure(to=((2**int(resolucion3.get()))-1),number_of_steps=((2**int(resolucion3.get()))-1))
        envio=f"canal3${int(frecuencia3.get())},{int(pin3.get())},{int(resolucion3.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)

    if canal==4:
        ciclo4.configure(to=((2**int(resolucion4.get()))-1),number_of_steps=((2**int(resolucion4.get()))-1))
        envio=f"canal4${int(frecuencia4.get())},{int(pin4.get())},{int(resolucion4.get())}"
        envio1=envio.encode('utf-8')
        print(envio1)
        ESP32.write(envio1)
            

def confLabel1(self):
    label3C1.delete("1.0","end-1c")
    label3C1.insert(f"1.0",f"{round(((int(ciclo1.get())*100))/((2**resolucion1.get())-1),2)}%")

def confLabel2(self):
    label3C2.delete("1.0","end-1c")
    label3C2.insert(f"1.0",f"{round(((int(ciclo2.get())*100))/((2**resolucion2.get())-1),2)}%")
       
def confLabel3(self):
    label3C3.delete("1.0","end-1c")
    label3C3.insert(f"1.0",f"{round(((int(ciclo3.get())*100))/((2**resolucion3.get())-1),2)}%")

def confLabel4(self):
    label3C4.delete("1.0","end-1c")
    label3C4.insert(f"1.0",f"{round(((int(ciclo4.get())*100))/((2**resolucion4.get())-1),2)}%")

def salir():
    ventana.destroy()
    ventana.quit()
       

customtkinter.set_appearance_mode("system")  # Modos: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Temas: "blue" (standard), "green", "dark-blue

ventana=customtkinter.CTk()
ventana.geometry(f"{1300}x{585}")
ventana.title("Control PWM")

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
#####################################################################################################################################
ciclo1=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=valoresResolucion,number_of_steps=valoresResolucion,
                               command=confLabel1)
ciclo1.place(x=350,y=100)

resolucion1=CTkSpinbox(ventana,width=100,height=50,min_value=2,start_value=2,max_value=16,step_value=2,font=('consolas',20))
resolucion1.place(x=600,y=75)

frecuencia1=CTkSpinbox(ventana,width=180,height=50,min_value=500,start_value=500,max_value=20000,step_value=500,font=('consolas',20))
frecuencia1.place(x=750,y=75)

pin1=CTkSpinbox(ventana,height=50,width=100,start_value=1,min_value=1,max_value=36,step_value=1,font=('consolas',20))
pin1.place(x=980,y=75)

canal1b1=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar PWM 1",command=lambda:confPWM(1))
canal1b1.place(x=1130,y=60)

canal1b2=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar ciclo PWM 1",command=lambda:confCiclo(1))
canal1b2.place(x=1130,y=100)

label1C1=customtkinter.CTkLabel(ventana,text="Canal 1",font=('Consolas',20))
label1C1.place(x=350,y=25)

label2C1=customtkinter.CTkLabel(ventana,text="Ciclo:",font=('Consolas',20))
label2C1.place(x=350,y=50)

label3C1=customtkinter.CTkTextbox(ventana,width=100,height=25,font=('consolas',20),fg_color='transparent')
label3C1.place(x=420,y=45)

label4C1=customtkinter.CTkLabel(ventana,text="Bits resolución",font=('Consolas',15))
label4C1.place(x=600,y=40)

label5C1=customtkinter.CTkLabel(ventana,text="Frecuencia (Hz)",font=('Consolas',15))
label5C1.place(x=750,y=40)

label6C1=customtkinter.CTkLabel(ventana,text="Pin salida",font=('Consolas',15))
label6C1.place(x=980,y=40)
#####################################################################################################################
ciclo2=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=valoresResolucion,number_of_steps=valoresResolucion,
                               command=confLabel2)
ciclo2.place(x=350,y=200)

resolucion2=CTkSpinbox(ventana,width=100,height=50,min_value=2,start_value=2,max_value=16,step_value=2,font=('consolas',20))
resolucion2.place(x=600,y=175)

frecuencia2=CTkSpinbox(ventana,width=180,height=50,min_value=500,start_value=500,max_value=20000,step_value=500,font=('consolas',20))
frecuencia2.place(x=750,y=175)

pin2=CTkSpinbox(ventana,height=50,width=100,start_value=1,min_value=1,max_value=36,step_value=1,font=('consolas',20))
pin2.place(x=980,y=175)

canal2b1=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar PWM 2",command=lambda:confPWM(2))
canal2b1.place(x=1130,y=160)

canal2b2=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar ciclo PWM 2",command=lambda:confCiclo(2))
canal2b2.place(x=1130,y=200)

label1C2=customtkinter.CTkLabel(ventana,text="Canal 2",font=('Consolas',20))
label1C2.place(x=350,y=125)

label2C2=customtkinter.CTkLabel(ventana,text="Ciclo:",font=('Consolas',20))
label2C2.place(x=350,y=150)

label3C2=customtkinter.CTkTextbox(ventana,width=100,height=25,font=('consolas',20),fg_color='transparent')
label3C2.place(x=420,y=145)

label4C2=customtkinter.CTkLabel(ventana,text="Bits resolución",font=('Consolas',15))
label4C2.place(x=600,y=140)

label5C2=customtkinter.CTkLabel(ventana,text="Frecuencia (Hz)",font=('Consolas',15))
label5C2.place(x=750,y=140)

label6C2=customtkinter.CTkLabel(ventana,text="Pin salida",font=('Consolas',15))
label6C2.place(x=980,y=140)
########################################################################################################################
ciclo3=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=valoresResolucion,number_of_steps=valoresResolucion,
                               command=confLabel3)
ciclo3.place(x=350,y=300)

resolucion3=CTkSpinbox(ventana,width=100,height=50,min_value=2,start_value=2,max_value=16,step_value=2,font=('consolas',20))
resolucion3.place(x=600,y=275)

frecuencia3=CTkSpinbox(ventana,width=180,height=50,min_value=500,start_value=500,max_value=20000,step_value=500,font=('consolas',20))
frecuencia3.place(x=750,y=275)

pin3=CTkSpinbox(ventana,height=50,width=100,start_value=1,min_value=1,max_value=36,step_value=1,font=('consolas',20))
pin3.place(x=980,y=275)

canal3b1=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar PWM 3",command=lambda:confPWM(3))
canal3b1.place(x=1130,y=260)

canal3b2=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar ciclo PWM 3",command=lambda:confCiclo(3))
canal3b2.place(x=1130,y=300)

label1C3=customtkinter.CTkLabel(ventana,text="Canal 3",font=('Consolas',20))
label1C3.place(x=350,y=225)

label2C3=customtkinter.CTkLabel(ventana,text="Ciclo:",font=('Consolas',20))
label2C3.place(x=350,y=250)

label3C3=customtkinter.CTkTextbox(ventana,width=100,height=25,font=('consolas',20),fg_color='transparent')
label3C3.place(x=420,y=245)

label4C3=customtkinter.CTkLabel(ventana,text="Bits resolución",font=('Consolas',15))
label4C3.place(x=600,y=240)

label5C3=customtkinter.CTkLabel(ventana,text="Frecuencia (Hz)",font=('Consolas',15))
label5C3.place(x=750,y=240)

label6C3=customtkinter.CTkLabel(ventana,text="Pin salida",font=('Consolas',15))
label6C3.place(x=980,y=240)
########################################################################################################################
ciclo4=customtkinter.CTkSlider(ventana,orientation="horizontal",from_=0,to=valoresResolucion,number_of_steps=valoresResolucion,
                               command=confLabel4)
ciclo4.place(x=350,y=400)

resolucion4=CTkSpinbox(ventana,width=100,height=50,min_value=2,start_value=2,max_value=16,step_value=2,font=('consolas',20))
resolucion4.place(x=600,y=375)

frecuencia4=CTkSpinbox(ventana,width=180,height=50,min_value=500,start_value=500,max_value=20000,step_value=500,font=('consolas',20))
frecuencia4.place(x=750,y=375)

pin4=CTkSpinbox(ventana,height=50,width=100,start_value=1,min_value=1,max_value=36,step_value=1,font=('consolas',20))
pin4.place(x=980,y=375)

canal4b1=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar PWM 4",command=lambda:confPWM(4))
canal4b1.place(x=1130,y=360)

canal4b2=customtkinter.CTkButton(ventana,width=100,height=25,text="Configurar ciclo PWM 4",command=lambda:confCiclo(4))
canal4b2.place(x=1130,y=400)

label1C4=customtkinter.CTkLabel(ventana,text="Canal 4",font=('Consolas',20))
label1C4.place(x=350,y=325)

label2C4=customtkinter.CTkLabel(ventana,text="Ciclo:",font=('Consolas',20))
label2C4.place(x=350,y=350)

label3C4=customtkinter.CTkTextbox(ventana,width=100,height=25,font=('consolas',20),fg_color='transparent')
label3C4.place(x=420,y=345)

label4C4=customtkinter.CTkLabel(ventana,text="Bits resolución",font=('Consolas',15))
label4C4.place(x=600,y=340)

label5C4=customtkinter.CTkLabel(ventana,text="Frecuencia (Hz)",font=('Consolas',15))
label5C4.place(x=750,y=340)

label6C4=customtkinter.CTkLabel(ventana,text="Pin salida",font=('Consolas',15))
label6C4.place(x=980,y=340)
##################################################################################################################################

botonSalir=customtkinter.CTkButton(ventana,text="Salir",width=150,height=50,font=('helvetica',18),command=salir)
botonSalir.place(x=700,y=500)
ventana.mainloop()