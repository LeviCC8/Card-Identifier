import pytesseract as ocr
from PIL import Image
import numpy as np
import cv2


# path do tesseract
ocr.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def operateImage(img):
	# Redimensionar  proporcionalmente a imagem por volta de 300 DPI
	length, width = img.shape
	imgScale = width/length
	resize = cv2.resize(img, (int(300*imgScale), 300), interpolation = cv2.INTER_CUBIC)

	# Embaçar a imagem para diminuição de ruídos
	blur = cv2.GaussianBlur(resize, (3,3), 0)

	# Limiarização da imagem 
	(T, thresh) = cv2.threshold(blur, 150, 255, cv2.THRESH_OTSU)

	return thresh


cartas = ['carta1.jpg', 'carta2.jpg', 'carta3.jpg', 'carta4.jpg', 'carta5.jpg']
for carta in cartas:
	numero = cartas.index(carta) + 1

	#Ler e operar cada imagem
	img = cv2.imread('cartas/{}'.format(carta))
	cv2.imshow('original', img)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	newimg = operateImage(img)
	cv2.imshow('img_modified', newimg)
	cv2.imwrite('cartas_modificadas/carta{}_modified.jpg'.format(numero), newimg)

	# Utilizar a OCR para identificação de texto, limitado aos valores 0-9, A, Q, K, J
	text = ocr.image_to_string(Image.open('cartas_modificadas/carta{}_modified.jpg'.format(numero)), config="-c tessedit_char_whitelist=0123456789AQKJ")
	characteres = list(text.replace(' ', '').replace('\n', ''))
	print('Cartas{}: '.format(numero) +' '.join(characteres))
	cv2.waitKey(0)