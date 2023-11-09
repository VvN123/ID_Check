''' Modulo de funciones para procesamiento de textos'''
import re
from pytesseract import pytesseract
from modules.valores import DATOS_FORMATEAR, DATOS_REGEX

# Realiza captura de texto en imagen por medio de Tesseract. Devuelve una cadena de texto.
def capturar_texto(ruta_imagen):
    txt_capturado = pytesseract.image_to_string(ruta_imagen, config='-l spa --psm 6')
    return txt_capturado

# Filtra texto de Tesseract con expresiones regulares. Retorna 'ERROR_LECTURA' en caso de incompatibilidad.
def formatear_texto(texto, index_regex):
    for char in DATOS_FORMATEAR[index_regex]:
        texto = texto.replace('\n', ' ').rstrip()
        texto = texto.replace(char, '')
    texto_regex = (re.search(DATOS_REGEX[index_regex],texto))
    if texto_regex is None:
        return 'ERROR'
    else:
        return texto_regex[0]  