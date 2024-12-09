import cv2
import easyocr
from matplotlib import pyplot as plt
# Cargar la imagen

def ocr_core(img):
    reader = easyocr.Reader(['es'])
    results = reader.readtext('temp/processed_imagen.png')
    documento = ''
# Mostrar resultados
    for (bbox, text, prob) in results:
        print(f"Texto detectado: {text} (confianza: {prob})")
        documento += ' ' +text
    return documento


if __name__ == '__main__':
    image = cv2.imread('temp/DNI_Enrique_Delgado.png',cv2.IMREAD_UNCHANGED)
    img_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
    opening_image = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel,iterations=1)
    invert_image = 255 - opening_image
    cv2.imwrite('temp/processed_imagen.png', invert_image)
    print(f"Imagen procesada guardada en: {'temp/processed_imagen.png'}")
    transcription = ocr_core('temp/processed_imagen.png')

