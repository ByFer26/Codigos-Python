import serial
import serial.tools.list_ports
import collections


def listadoPuertos():
    puertos=[]
    for i in serial.tools.list_ports.comports():
        puertos.append(i.name)
    return puertos

def obtenerPuerto(puerto,baudios):
    puerto=puerto.replace('(','')
    puerto=puerto.replace(')','')
    puerto=puerto.replace("'",'')
    puerto=puerto.replace(',','')
    return puerto,baudios,

def conectar(puerto,baudios):
    condicion1=True
    while (condicion1):
        try:
            ESP32=serial.Serial(puerto,baudios)
            condicion1=False
        except:
            pass
    return ESP32

def obtenerDatos(dispositivo):
    condicion2=True
    dispositivo.reset_input_buffer()
    while condicion2:
        try:
            datos=dispositivo.readline().decode('utf-8').replace('\r\n', '')
            datos=datos.split(",")
            datos1=float(datos[0])
            datos2=float(datos[1])
            datos1=round((datos1*3.3)/4096,2)
            datos2=round((datos2*3.3)/4096,2)
            condicion2=False
        except ValueError or UnicodeDecodeError:
            pass
        except IndexError:
            pass
    return datos1,datos2

def crearArreglos(longitud1):
    x1=[]
    for i in range(0,longitud1):
        x1.append(0)

    return x1



def insertarDatos(ar1,val1,longitud):
    if len(ar1)>=longitud:
        ar1.pop(0)
    ar1.append(val1)
    return ar1

    



