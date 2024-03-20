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

def crearArreglos(longitud1,longitud2):
    x1=collections.deque([0]*longitud1, maxlen=longitud1)
    x2=collections.deque([0]*longitud2, maxlen=longitud2)
    return x1,x2



def insertarDatos(ar1,ar2,val1,val2):
    ar1.append(val1)
    ar2.append(val2)
    return ar1,ar2