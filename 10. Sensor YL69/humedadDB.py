import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

conexion = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="netacad20",
    port="5432"
)

conexion.autocommit = True

def crearTabla(nombre, col1, col2):
    cursor = conexion.cursor()
    query = f'CREATE TABLE {nombre}({col1} varchar(30),{col2} varchar(30))'
    cursor.execute(query)
    cursor.close()

def insertarDatos(tabla, col1, col2,  nombre, apellido):
    cursor = conexion.cursor()
    query = f"INSERT INTO {tabla}({col1},{col2}) VALUES ('{nombre}','{apellido}')"
    cursor.execute(query)
    cursor.close()


def eliminarDatos(tabla):
    cursor=conexion.cursor()
    query=f"DELETE FROM {tabla}"
    cursor.execute(query)
    cursor.close

def eliminarTabla(tabla):
    cursor=conexion.cursor()
    query=f"DROP TABLE {tabla}"
    cursor.execute(query)
    cursor.close

def extraerDatos(tabla):
    cursor=conexion.cursor()
    query=f"SELECT * FROM {tabla}"
    cursor.execute(query)
    datos=cursor.fetchall()
    cursor.close
    return datos

def generarPDF(tabla,nombre):
    datos=extraerDatos(tabla)
    documento = canvas.Canvas(f"{nombre}.pdf", pagesize=letter)
    x = 100
    y = 700
    for fila in datos:
        for valor in fila:
            documento.drawString(x, y, str(valor))
            x += 200  
        y -= 20  
        x = 100   
    documento.save()