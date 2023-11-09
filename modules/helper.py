'''Modulo con funciones de uso general'''
import os
from datetime import datetime
from pytesseract import pytesseract

def ejecucion_en_colab():
    try:
        import google.colab
        return True
    except:
        return False

# Print de todos los resultados de Tesseract ya formateados
def print_al_terminal(listado_textos):
    i = listado_textos
    a ,b, c, d, e, f, g = i[0], i[1], i[2], i[3], i[4], i[5], i[6]  
    print('-------------DATOS-----------------------')
    print('RUT              : '+a)
    print('NOMBRES          : '+b)
    print('APELLIDOS        : '+c)
    print('N° DOCUMENTO     : '+d)
    print('F. NACIMIENTO    : '+e)
    print('F. EMISION       : '+f)
    print('F. VENCIMIENTO   : '+g)
    print('-----------------------------------------')

# Limpia archivos temporales
def limpiar_archivos_temporales():
    return None

# Genera rutas para archivos o carpetas dentro del directorio "Pattern-Matching\rsc"
def generar_ruta(nombre_carpeta,nombre_archivo):
    ruta=os.path.join(PLATAFORM_ROOT,'data',nombre_carpeta,nombre_archivo)
    return ruta

#Devuelve timestamp de tiempo
def obtener_tiempo():
    tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return tiempo

if ejecucion_en_colab() is True:  # Cambia el root dependiendo del entorno
    PLATAFORM_ROOT = r"/content/drive/MyDrive/Colab/Pattern-Matching"
else:
    PLATAFORM_ROOT = r"C:\Users\VvN\Desktop\Mega\Vicente\Python\Project_ID\ID_Check"
    PATH_TO_TESSERACRT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = PATH_TO_TESSERACRT 


