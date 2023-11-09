''' Modulo de funciones para procesamiento de imagenes'''
import cv2 
import numpy as np
from PIL import Image,ImageEnhance
from modules.valores import DATOS_RECORTES, DATOS_RESALTAR, DATOS_PATRON, DATOS_RAZONES
from math import atan2,degrees
from modules.helper import generar_ruta

# Carga el archivo a objecto imagen OpenCV
def load_image(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    return img

# Carga el archivo a objecto imagen OpenCV en escala de grises
def load_image_grey(ruta_imagen):
    img = cv2.imread(ruta_imagen, 0)
    return img

# Guarda objeto imagen OpenCV en destino
def save_image(imagen, ruta_salida):
    cv2.imwrite(ruta_salida, imagen)

# Carga el archivo a objecto imagen Pillow
def load_image_pillow(ruta_imagen):
    img = Image.open(ruta_imagen)
    return img

# Rota la imagen n grados. Retorna obj imagen
def rotate_image(imagen, grados_rotacion):
    grados_rotacion = grados_rotacion + 33
    image_center = tuple(np.array(imagen.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, grados_rotacion, 1.0)
    img = cv2.warpAffine(imagen, rot_mat, imagen.shape[1::-1], flags=cv2.INTER_LINEAR)
    return img

# Recorta la imagen. Devuelve obj imagen OpenCV
def crop_image(imagen, coordenadas, razones):
    (p1x, p1y, p3x, p3y) = coordenadas
    razon_1, razon_2, razon_3, razon_4 = razones 
    limite_izquierdo = int(p1x - ((p3x-p1x)/razon_1))
    limite_derecho = int(p1x - ((p3x-p1x)/razon_2))
    limite_superior = int(p3y - ((p1y-p3y)/razon_3))
    limite_inferior = int(p3y - ((p1y-p3y)/razon_4)) 
    recorte = imagen[limite_superior:limite_inferior, limite_izquierdo:limite_derecho]
    return recorte

# Redimensiona imagen cambiando solo el ancho y manteniendo su aspecto original. Devuelve Obj imagen OpenCV
def resize_image(imagen, nuevo_ancho):
    (alto, ancho) = imagen.shape[:2]
    aspect_ratio = ancho / alto
    nueva_altura = int(nuevo_ancho / aspect_ratio)
    imagen_redimensionada = cv2.resize(imagen, (nuevo_ancho, nueva_altura))
    return imagen_redimensionada

# Aplica filtro. Devuelve Obj imagen Pillow
def image_filters(imagen, tipo_filtro, factor):
    if tipo_filtro == 'sharpness':
        enhance_type = ImageEnhance.Sharpness(imagen)
    if tipo_filtro == 'contrast':
        enhance_type = ImageEnhance.Contrast(imagen)
    if tipo_filtro == 'color':
        enhance_type = ImageEnhance.Color(imagen)
    if tipo_filtro == 'brightness':
        enhance_type = ImageEnhance.Brightness(imagen)
    return enhance_type.enhance(factor)

# Traspasar obj imagen OpenCV a Pillow
def cv2image_to_pillow(imagen):
    cv_image_array = np.array(imagen)
    return Image.fromarray(cv_image_array)

# Aplica un fondo blanco para lectura de Tesseract. Devuelve Obj imagen Pillow
def apply_white_bg(imagen):
    fondo_blanco = load_image_pillow(generar_ruta('resources\\background', 'white_bg.png'))
    imagen = fondo_blanco.copy()
    imagen.paste(imagen, (50, 50))
    return imagen

# Concatena una serie de filtros de imagen para resaltar los textos. Devuelve Obj imagen pillow
def enhance_texts(imagen):
    factor_1, factor_2, factor_3, factor_4, factor_5 = DATOS_RESALTAR
    imagen_resaltada_1 = image_filters(imagen, 'sharpness', factor_1)
    imagen_resaltada_2 = image_filters(imagen_resaltada_1, 'contrast', factor_2)
    imagen_resaltada_3 = image_filters(imagen_resaltada_2, 'color', factor_3)
    imagen_resaltada_4 = image_filters(imagen_resaltada_3, 'brightness', factor_4)
    imagen_resaltada = image_filters(imagen_resaltada_4, 'sharpness', factor_5)
    return imagen_resaltada

# Compara imagen con un patron. Ambos input deben ser en escala de grises. Retorna coordenadas
def locate_pattern(imagen_grey, imagen_patron_grey):
    try:
        w, h = imagen_patron_grey.shape[::-1]
        method = eval('cv2.TM_CCOEFF_NORMED')
        res = cv2.matchTemplate(imagen_grey, imagen_patron_grey, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        x = (top_left[0] + bottom_right[0]) / 2
        y = (top_left[1] + bottom_right[1]) / 2
        return x, y
    except:
        return None

#Comprueba coherencia de datos obtenidos en ubicar_patron(). En caso de ser correctos, devuelve coordenadas.
def try_pattern_list(imagen):
    i, datos = 0, 0
    while i < len(DATOS_PATRON):
        patron = DATOS_PATRON[i]
        p1x, p1y = locate_pattern(imagen, load_image_grey(generar_ruta('resources\pattern',patron[0])))
        p2x, p2y = locate_pattern(imagen, load_image_grey(generar_ruta('resources\pattern',patron[1])))
        p3x, p3y = locate_pattern(imagen, load_image_grey(generar_ruta('resources\pattern',patron[2])))
        datos = (p1x, p1y, p2x, p2y, p3x, p3y)
        if check_data(datos) is True:
            angulo = get_angle(p1x, p1y, p3x, p3y)
            datos = (p1x, p1y, p3x, p3y), angulo
            break
        else:
            i += 1
        datos = None
    return datos

def check_data(datos: tuple):
    p1x, p1y, p2x, p2y, p3x, p3y = datos
    razon = (p1y-p2y) / (p3x-p2x)
    angulo = get_angle(p1x, p1y, p3x, p3y)
    if razon < 0.8 or razon > 0.87 or angulo < -36 or angulo > -28:
        return False
    return True

# Obtiene el angulo entre dos rectas. Calcula en radianes y retorna en grados
def get_angle(p1x, p1y, p2x, p2y):
    delta_x = p2x - p1x
    delta_y = p2y - p1y
    return degrees(atan2(delta_y,delta_x))

# Recorta los textos ubicados en la imagen. Devuelve Obj imagen OpenCV    
def crop_text(imagen,index_datos):
    datos = DATOS_RECORTES[index_datos]
    return imagen[int(datos[1]):int(datos[3]), int(datos[0]):int(datos[2])]

def loop(foto_carnet,datos):
    for i in range(3):
        if datos is not None:
            if i == 0:
                foto_carnet = rotate_image(foto_carnet, datos[1])
                print(f'flag '+str(i))
            if i == 1:
                foto_carnet = crop_image(foto_carnet, datos[0], DATOS_RAZONES[0]) 
                foto_carnet = resize_image(foto_carnet, 3000)
                print(f'flag '+str(i))
            if i == 2:
                foto_carnet = crop_image(foto_carnet, datos[0], DATOS_RAZONES[1]) 
                foto_carnet = resize_image(foto_carnet, 1920)
                print(f'flag '+str(i))
    
#### FUNCIONES DESACTIVADAS TEMPORALMENTE ####

# Redimensiona una imagen cambiando solo el ancho con Pillow. SIN USO
def redimensionar_imagen_pil(imagen, ancho):
    wpercent = (ancho/float(imagen.size[0]))
    hsize = int((float(imagen.size[1])*float(wpercent)))
    redimension = imagen.resize((ancho,hsize), Image.Resampling.LANCZOS)
    return redimension

# Recorta los textos ubicados en la imagen con Pillow. SIN USO
def recortar_textos_pil(imagen, index_datos):
    coordenada = DATOS_RECORTES[index_datos]
    recorte = imagen.crop((coordenada[0], coordenada[1], coordenada[2], coordenada[3]))
    return recorte

# Guarda un objecto de imagen Pillow como archivo en el directorio indicado con Pillow. SIN USO
def grabar_imagen_pil(imagen, ruta_salida):
    imagen.save(ruta_salida)
