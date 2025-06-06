# VisionAI/utils.py

import os
import tempfile
import re
from io import BytesIO

import cv2
import numpy as np
import pytesseract
import unidecode
import pandas as pd

from django.core.files.base import ContentFile

# -------------------------------------------------------------------
#  Configuraciones generales para OCR
# -------------------------------------------------------------------
# Lenguaje para Tesseract: 'spa' (español). Asegúrate de tener spa.traineddata en tessdata.
TESS_LANG = "spa"
# Parámetros de Tesseract: oem 3 (LSTM+Legacy), psm 3 (página completa)
TESS_CONFIG_FULLPAGE = r"--oem 3 --psm 3"


# -------------------------------------------------------------------
#  1) Función de preprocesamiento: redimensionar, filtrar, umbral adaptativo
# -------------------------------------------------------------------
def preprocesar_imagen(ruta_imagen, ancho_destino=1800):
    """
    1) Lee la imagen desde disco.
    2) Redimensiona a un ancho fijo (manteniendo relación de aspecto) para asegurar un DPI consistente.
    3) Convierte a escala de grises.
    4) Aplica filtro bilateral para preservar bordes y reducir ruido.
    5) Aplica umbral adaptativo para facturas con iluminación irregular.
    """
    img_color = cv2.imread(ruta_imagen)
    if img_color is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {ruta_imagen}")

    # 1. Redimensionar a ancho fijo
    h, w = img_color.shape[:2]
    escala = ancho_destino / float(w)
    nuevo_w = ancho_destino
    nuevo_h = int(h * escala)
    img_color = cv2.resize(img_color, (nuevo_w, nuevo_h), interpolation=cv2.INTER_CUBIC)

    # 2. Convertir a escala de grises
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # 3. Filtro bilateral (reduce ruido, preserva bordes)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # 4. Umbral adaptativo
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=21,
        C=5
    )
    return thresh


# -------------------------------------------------------------------
#  2) Función de OCR con Tesseract
# -------------------------------------------------------------------
def extraer_texto_ocr(imagen_binaria, config=TESS_CONFIG_FULLPAGE):
    """
    Realiza OCR usando Tesseract sobre la imagen binaria proporcionada.
    """
    texto = pytesseract.image_to_string(imagen_binaria, lang=TESS_LANG, config=config)
    return texto


# -------------------------------------------------------------------
#  3) Función de normalización “OCR‐friendly”
# -------------------------------------------------------------------
def normalizar_texto(raw_text):
    """
    - Quita tildes y acento con unidecode.
    - Aplica correcciones puntuales de OCR (MIT→NIT, S4,S→S.A.S., etc).
    - Reemplaza saltos de línea por marcador '<<NL>>'.
    - Elimina caracteres extraños, unifica espacios y pasa a mayúsculas.
    """
    # 1) Quitar tildes y caracteres especiales
    t = unidecode.unidecode(raw_text)

    # 2) Correcciones específicas de OCR
    t = re.sub(r"\bMIT\b", "NIT", t, flags=re.IGNORECASE)
    t = re.sub(r"CEN\s*CIODADNDA", "CEDULA DE CIUDADANIA", t, flags=re.IGNORECASE)
    t = re.sub(r"YE\s*TODAL", "TOTAL", t, flags=re.IGNORECASE)
    t = re.sub(r"TOT\s*AL", "TOTAL", t, flags=re.IGNORECASE)
    t = re.sub(r"S\.?4,?S\.?", "S.A.S.", t, flags=re.IGNORECASE)
    t = re.sub(r"S4,?S", "S.A.S.", t, flags=re.IGNORECASE)
    t = re.sub(r"VILLAYICENCIO", "VILLAVICENCIO", t, flags=re.IGNORECASE)

    # 3) Reemplazar saltos de línea por marcador especial <<NL>>
    t = t.replace("\r\n", "<<NL>>").replace("\n", "<<NL>>")

    # 4) Correcciones adicionales
    t = t.replace("|", "I")
    # Reemplazar 0 por O y 5 por S solo si están entre letras
    t = re.sub(r"(?<=\D)0(?=\D)", "O", t)
    t = re.sub(r"(?<=\D)5(?=\D)", "S", t)

    # 5) Eliminar caracteres extraños (dejamos: A-Z, a-z, 0-9, espacios, ., : / - $ < >)
    t = re.sub(r"[^A-Za-z0-9\s\.\,\:\-/\$\<\>]", "", t)

    # 6) Unificar espacios múltiples
    t = re.sub(r"\s{2,}", " ", t).strip()

    # 7) Pasar a mayúsculas
    return t.upper()


# -------------------------------------------------------------------
#  4) Funciones para extraer cada campo (regex + lógica línea a línea)
# -------------------------------------------------------------------
def extraer_nombre_empresa(texto_norm):
    """
    Estrategia:
      1) Divide texto en líneas (marcadas con '<<NL>>').
      2) Busca explícitamente 'PANAMERICANA' en las primeras 8 líneas.
      3) Si no, busca palabras clave típicas de razón social.
      4) Si detecta 'FACTURA DE VENTA' en la línea, la omite.
      5) Fallback: línea 0 si tiene al menos 4 palabras y no coincide con 'FACTURA DE VENTA'.
    """
    lineas = [l.strip() for l in texto_norm.split("<<NL>>") if l.strip()]

    # 1) Prioridad: PANAMERICANA
    for linea in lineas[:8]:
        if "PANAMERICANA" in linea:
            if "NIT" in linea:
                antes_nit = linea.split("NIT")[0].strip()
                return re.sub(r"[\-:/\s]+$", "", antes_nit)
            else:
                return re.sub(r"[\-:/\s]+$", "", linea)

    # 2) Otras palabras clave (omitimos 'FACTURA DE VENTA')
    palabras_clave = ["S.A.S", "LTDA", "S.A.", "COMERCIAL", "COLOMBIA",
                      "HOME-CENTER", "SODIMAC", "EXITŌ", "ALKOSTO"]
    for linea in lineas[:8]:
        if "FACTURA DE VENTA" in linea:
            continue
        for clave in palabras_clave:
            if clave in linea:
                if "NIT" in linea:
                    antes_nit = linea.split("NIT")[0].strip()
                    return re.sub(r"[\-:/\s]+$", "", antes_nit)
                else:
                    return re.sub(r"[\-:/\s]+$", "", linea)

    # 3) Fallback: línea 0 si tiene ≥4 palabras y no es 'FACTURA DE VENTA'
    if lineas:
        primera = lineas[0]
        if "FACTURA DE VENTA" not in primera and len(primera.split()) >= 4:
            if "NIT" in primera:
                return re.sub(r"[\-:/\s]+$", "", primera.split("NIT")[0].strip())
            return re.sub(r"[\-:/\s]+$", "", primera)

    return "No encontrado"


def extraer_nit(texto_norm):
    """
    Estrategia:
      1) Regex flexible para 'NIT' o 'MIT' y 6–20 caracteres siguientes.
      2) Limpiar '.', '-', espacios y convertir 'O'→'0'.
    """
    m = re.search(r"""
        \b[MN]\.?I\.?T\.?\b      # 'NIT' o 'MIT' con o sin puntos
        [\s:\-]*                 # espacios, ':' o '-'
        ([0-9O\.\- ]{6,20})      # 6–20 dígitos o caracteres OCR
        """, texto_norm, re.IGNORECASE | re.VERBOSE)
    if not m:
        return "No encontrado"
    raw = m.group(1)
    nit_limpio = raw.replace(".", "").replace("-", "").replace(" ", "")
    nit_limpio = nit_limpio.replace("O", "0")
    return nit_limpio


def extraer_fecha(texto_norm):
    """
    Estrategia:
      1) Buscar fechas dd/mm/yyyy o dd-mm-yyyy.
      2) También patrones textuales 'ENERO 15 2021', etc.
      3) Devolver en formato dd/mm/yyyy.
    """
    # 1) Regex estricto dd/mm/yyyy o dd-mm-yyyy
    m1 = re.search(r"\b([0-3]\d[\/\-][0-1]\d[\/\-]20\d{2})\b", texto_norm)
    if m1:
        return m1.group(1).replace("-", "/")

    # 2) Meses en texto
    meses = {
        "ENERO": "01", "FEBRERO": "02", "MARZO": "03", "ABRIL": "04",
        "MAYO": "05", "JUNIO": "06", "JULIO": "07", "AGOSTO": "08",
        "SEPTIEMBRE": "09", "OCTUBRE": "10", "NOVIEMBRE": "11", "DICIEMBRE": "12"
    }
    for mes_texto, mes_num in meses.items():
        patron = rf"\b([0-3]?\d)\s+{mes_texto}\s+(20\d{{2}})\b"
        m2 = re.search(patron, texto_norm)
        if m2:
            dia = m2.group(1).zfill(2)
            ano = m2.group(2)
            return f"{dia}/{mes_num}/{ano}"

    return "No encontrado"


def extraer_cedula(texto_norm):
    """
    Estrategia:
      1) Buscar 'C.C./N.I.T.: <números>'.
      2) Si no, 'CC: <números>'.
      3) Si no, 'CEDULA DE CIUDADANIA: <números>'.
      4) Limpiar '-' y convertir 'O'→'0'.
    """
    # 1) 'C.C./N.I.T.: 830.182.829-9'
    m1 = re.search(r"C\.?C\.?\/N\.?I\.?T\.?[:\s]*([0-9O\.\- ]{6,20})",
                   texto_norm, re.IGNORECASE)
    if m1:
        raw = m1.group(1)
        lim = raw.replace(".", "").replace("-", "").replace(" ", "")
        return lim.replace("O", "0")

    # 2) 'CC: 12345678'
    m2 = re.search(r"\bCC[:\s\-]*([0-9]{6,15})\b", texto_norm, re.IGNORECASE)
    if m2:
        return m2.group(1)

    # 3) 'CEDULA DE CIUDADANIA: 12345678-9'
    m3 = re.search(r"(?:CEDULA\s+DE\s+CIUDADANIA)[:\s]*([0-9]{6,15}-?[0-9]?)",
                   texto_norm, re.IGNORECASE)
    if m3:
        raw = m3.group(1).replace("-", "")
        return raw

    return "No encontrado"


def extraer_total(texto_norm):
    """
    Estrategia:
      1) Buscar línea con 'TOTAL' y '$', excluyendo 'SUBTOTAL' o 'IVA'.
      2) Si no aparece, buscar 'VALOR TOTAL' o 'TOTAL A PAGAR'.
      3) Si sigue sin hallarse, tomar la última ocurrencia de patrón monetario.
      4) Devolver cifra limpia (sin puntos ni comas).
    """
    lineas = [l.strip() for l in texto_norm.split("<<NL>>") if l.strip()]

    # 1) Buscar línea con 'TOTAL' + '$'
    for linea in reversed(lineas):
        if re.search(r"\bTOTAL\b", linea) and "$" in linea:
            if "SUBTOTAL" in linea or "IVA" in linea:
                continue
            m = re.search(r"[\$]\s*([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,]\d{2})?)", linea)
            if m:
                return m.group(1).replace(".", "").replace(",", "")

    # 2) Buscar 'VALOR TOTAL' o 'TOTAL A PAGAR'
    for linea in reversed(lineas):
        if "VALOR TOTAL" in linea or "TOTAL A PAGAR" in linea:
            m2 = re.search(r"([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,]\d{2})?)", linea)
            if m2:
                return m2.group(1).replace(".", "").replace(",", "")

    # 3) Última ocurrencia de patrón monetario en todo el texto
    m3s = re.findall(r"([0-9]{1,3}(?:[.,][0-9]{3})*(?:[.,]\d{2})?)", texto_norm)
    if m3s:
        ultimo = m3s[-1]
        return ultimo.replace(".", "").replace(",", "")

    return "No encontrado"


# -------------------------------------------------------------------
#  5) Función que agrupa todo: preprocesa, OCR, normaliza, extrae campos
# -------------------------------------------------------------------
def procesar_factura(ruta_imagen):
    """
    Procesa una sola imagen de factura en disco:
      1) Preprocesa con OpenCV (preprocesar_imagen).
      2) Realiza OCR (extraer_texto_ocr).
      3) Normaliza el texto (normalizar_texto).
      4) Extrae campos (empresa, nit, fecha, cedula, total).
      5) Devuelve un dict con esos valores.
    """
    try:
        imagen_proc = preprocesar_imagen(ruta_imagen)
    except FileNotFoundError as e:
        return {"error": str(e)}

    # 1) OCR completo (psm=3)
    texto_ocr = extraer_texto_ocr(imagen_proc, config=TESS_CONFIG_FULLPAGE)

    # 2) Normalizar el texto
    texto_norm = normalizar_texto(texto_ocr)

    # 3) Extraer cada campo
    datos = {
        "empresa": extraer_nombre_empresa(texto_norm),
        "nit":     extraer_nit(texto_norm),
        "fecha":   extraer_fecha(texto_norm),
        "cedula":  extraer_cedula(texto_norm),
        "total":   extraer_total(texto_norm)
    }
    return datos


# -------------------------------------------------------------------
#  6) Funciones auxiliares para integrar con Django (S3 o FileField)
# -------------------------------------------------------------------
def escribir_temporal_desde_filefield(filefield):
    """
    Dado un FileField (por ejemplo, DocumentoFactura.archivo), abre el archivo en
    modo binario y lo escribe en un archivo temporal en disco para que OpenCV lo lea.
    Retorna la ruta local del tempfile.
    """
    # Obtener extensión del archivo original
    nombre_original = filefield.name  # ej: 'facturas/mi-factura.jpg'
    ext = os.path.splitext(nombre_original)[1]  # ej: '.jpg' o '.pdf'

    # Crear un NamedTemporaryFile en disco con esa extensión
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    with filefield.open('rb') as f_src:
        temp.write(f_src.read())
    temp.flush()
    temp.close()

    return temp.name


def generar_excel_desde_listado(filas):
    """
    Recibe una lista de diccionarios (una fila por cada documento),
    donde cada dict contiene claves: 'empresa', 'nit', 'fecha', 'cedula', 'total'.
    Crea un DataFrame de pandas y genera un BytesIO con el .xlsx resultante.
    """
    df = pd.DataFrame(filas)
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer


def procesar_factura_ocr_y_generar_excel(factura):
    """
    1) Recorre todos los Documentos asociados a la factura.
    2) Para cada DocumentoFactura:
       a) Escribe su contenido en un archivo temporal.
       b) Llama a procesar_factura(ruta_temp) para extraer campos.
       c) Elimina el archivo temporal.
    3) Con la lista de dicts, genera un Excel en memoria (BytesIO).
    4) Guarda el Excel en factura.resumen_excel (sube a S3).
    5) Actualiza la factura.
    """
    filas = []

    for doc in factura.documentos.all():
        # 1) Crear archivo temporal desde el FileField
        ruta_temp = escribir_temporal_desde_filefield(doc.archivo)

        # 2) Extraer campos usando el pipeline OCR
        resultado = procesar_factura(ruta_temp)
        # Si hubo error, podrías registrar o marcar, pero aquí simplemente lo agregamos
        if "error" not in resultado:
            filas.append(resultado)
        else:
            filas.append({
                "empresa": "Error",
                "nit": "Error",
                "fecha": "Error",
                "cedula": "Error",
                "total": "Error"
            })

        # 3) Borrar el temporal
        os.remove(ruta_temp)

    # 4) Generar el Excel con todos los resultados
    buffer_excel = generar_excel_desde_listado(filas)

    # 5) Guardar en el campo resumen_excel (sube a S3)
    nombre_excel = f"factura_{factura.id}_resumen.xlsx"
    factura.resumen_excel.save(nombre_excel, ContentFile(buffer_excel.getvalue()))
    # 6) Actualizar solo el campo resumen_excel en la BD
    factura.save(update_fields=['resumen_excel'])
