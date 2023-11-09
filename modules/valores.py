''' Modulo con parametros y constantes para ejecución de otros modulos'''

# Diccionario de nombres
DATOS_TEXTOS = ['rut', 'nom', 'ape', 'ndoc', 'fnac', 'femi', 'fvenc']

# Factores de intensidad para filtros de imagen
DATOS_RESALTAR = [0,3,1,4,0]  

# Proporciones para verificacion de patrones
DATOS_RAZONES = (
    [8.294985250737463, -0.8901551123773346,
     6.2439024390243905, -0.877141458639256,],
    [32.12, -0.9745145631067961, 
     46.088235294117645, -1.0038436899423446]
)

# Coordenadas para recorte textos
DATOS_RECORTES = (  
    [20,1020,630,1130],
    [600,400,1600,480],
    [600,210,1200,345],
    [1100,625,1500,700],
    [600,625,1100,695],
    [600,745,1100,820],
    [1100,745,1520,820]
)

# Limpieza de textos
DATOS_FORMATEAR = (
    [',', '', 'RUN', '.', ' '],
    [',', '', '.'],
    [',', '', '.'],
    [',', '', '.', ' '],
    [',', '', '.'],
    [',', '', '.'],
    [',', '', '.']
)

# Combinaciones de patrones 
DATOS_PATRON = ( 
    ['pattern_A_1.png','pattern_B_1.png','pattern_C_1.png'],
    ['pattern_A_2.png','pattern_B_2.png','pattern_C_2.png'],
    ['pattern_A_3.png','pattern_B_3.png','pattern_C_3.png'],
    ['pattern_A_4.png','pattern_B_4.png','pattern_C_4.png'],
    ['pattern_A_5.png','pattern_B_5.png','pattern_C_5.png'],
    ['pattern_A_6.png','pattern_B_6.png','pattern_C_6.png'],
    ['pattern_A_7.png','pattern_B_7.png','pattern_C_7.png'],
    ['pattern_A_8.png','pattern_B_8.png','pattern_C_8.png'],
    ['pattern_A_9.png','pattern_B_9.png','pattern_C_9.png']
)

# Expresiones REGEX para aprobar textos
DATOS_REGEX = [
    '^([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9][0-9][0-9][0-9])-([0-9]|K)$',
    '^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$',
    '^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$',
    '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]',
    '^[0-9][0-9] [A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*|^[0-9][0-9] [A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*',
    '^[0-9][0-9] [A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*|^[0-9][0-9] [A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*',
    '^[0-9][0-9] [A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*|^[0-9][0-9] [A-Z][A-Z][A-Z][A-Z] [0-9][0-9][0-9][A-Z0-9]*'
]


