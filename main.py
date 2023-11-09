import os
from uuid import uuid1
import cv2 as cv2
from modules import firebase as fb
from modules import gdrive as gd
from modules import helper as h
from modules import imagenes as im
from modules import textos as tx
from modules import valores as val
from dataclasses import dataclass, replace
import dataclasses
from collections import OrderedDict


os.system('cls')
task = False
fb.connect_to_fb()
source_img = 's_3.png'
global foto_carnet

@dataclass
class person:
    uuid: str = None
    thumbnail: str = None
    rut: str = None
    nombres: str = None
    apellidos: str = None
    n_documento: str = None
    f_nacimiento: str = None
    f_emision: str = None
    f_vencimiento: str = None
    f_scan: str = h.obtener_tiempo()
    pending: bool = True

while task is True:
    try:
        foto_carnet = im.load_image_grey(h.generar_ruta('input', source_img))
        foto_carnet = im.resize_image(foto_carnet, 3500)
        foto_carnet = im.rotate_image(foto_carnet, im.try_pattern_list(foto_carnet)[1])
        foto_carnet = im.crop_image(foto_carnet, im.try_pattern_list(foto_carnet)[0], val.DATOS_RAZONES[0]) 
        foto_carnet = im.resize_image(foto_carnet, 3000)
        foto_carnet = im.crop_image(foto_carnet, im.try_pattern_list(foto_carnet)[0], val.DATOS_RAZONES[1]) 
        foto_carnet = im.resize_image(foto_carnet, 1920)
        vista_previa = foto_carnet
    except:
        print('No se pudo procesar la imagen')
        break 
    
    uuid = str(uuid1())
    file_name = uuid+'.jpg'
    ruta_grabar = h.generar_ruta('temp', file_name)
    vista_previa = cv2.resize(vista_previa, (543, 340))
    im.save_image(vista_previa, ruta_grabar)
    thumbnail_id = gd.upload_to_gd(ruta_grabar, file_name)
    os.remove(ruta_grabar)
    data_for_fbase = [uuid, thumbnail_id]
    
    for i in range(len(val.DATOS_REGEX)):
        txt_in_img = im.crop_text(foto_carnet, i)
        txt_in_img = im.cv2image_to_pillow(txt_in_img)     
        txt_in_img = im.enhance_texts(txt_in_img)
        txt_in_img = im.apply_white_bg(txt_in_img)
        texto_capturado = tx.capturar_texto(txt_in_img)
        texto_formateado = tx.formatear_texto(texto_capturado, i)    
        data_for_fbase.append(texto_formateado)
    persona_1 = dataclasses.asdict(person(*data_for_fbase))
    fb.upoload_to_fb(uuid, persona_1)
    break


