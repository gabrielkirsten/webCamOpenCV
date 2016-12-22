##############################################################################################
##############################################################################################
#
#                 		VISAO COMPUTACIONAL - 19/08/2016
#
# Criar um software em python para aplicar uma serie de filtros, escolhidos pelo usuario, na imagem capturada pela webcam do laptop (ou de uma webcam ligada a um desktop).  Leia as orientacoes disponivel na Secao "Procedimento e Criterios de Avaliacao" para saber como submeter uma atividade envolvendo geracao de codigo (programacao).  O software precisa atender aos seguintes requisitos:
#
# - O software deve ler e mostrar na tela a imagem que esta sendo capturada pela webcam (em tempo real)
# - Ao pressionar as seguintes teclas as operacoes correspondentes devem ser aplicadas (e o resultado mostrado em tempo real na tela do computador)
# - 'a' = Zera os canais R e G deixando apenas o canal azul (a imagem devera ficar toda azulada)  
# - 'g' = Zera os canais R e B deixando apenas o canal verde (a imagem devera ficar toda esverdeada)  
# - 'c' = Aplica deteccao de bordas de canny
# - 's' = Realiza segmentacdo por subtracao de fundo (o quadro que estiver sendo capturado no momento em que a tecla 's' for pressionada deve ser considerado como fundo)
# - 'f' = Desenha um retangulo ou uma elipse ao redor das faces que aparecem na imagem (existem varias solucoes para isso disponiveis na internet, pode usar alguma pronta ou desenvolver seu proprio detector de faces)
# - 'h' = Transforma a imagem para o espaco HSV e zera os canais S e V, deixando apenas a matiz (Hue)
#
#   Academico: Gabriel Kirsten Menezes RA: 148298
#
##############################################################################################
##############################################################################################

import numpy as np
import cv2

#arquivo .xml contedo os padroes para o reconhecimento facial
arqCasc = './haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(arqCasc)

#inicia a captura do video
cap = cv2.VideoCapture(0)
opc = 0 #opcoes que simbolizam as teclas digitadas pelo usuario
while(True):
	# faz a captura de cada frame obtido pela webcam
	ret, frame = cap.read()
	
	#carrega o frame em escala de cinza
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 

	if opc == 1: 
		frame[:,:,1] = 0 				#zera o canal G
		frame[:,:,2] = 0 				#zera o canal R
		img = frame 					#a imagem de saida e somente o canal B
			
	elif opc == 2:
		frame[:,:,0] = 0 				#zera o canal B
		frame[:,:,2] = 0 				#zera o canal R
		img = frame 					#a imagem de saida e somente o canal G
		
	elif opc == 3:
		sigma=0.33
		v = np.median(gray) 						#calcula do valor medio da matriz em tons de cinza
		# aplica a deteccao de bordas por Canny utilizando a media
		minimo = int(max(0, (1.0 - sigma) * v)) 	#calcula o valor minimo
		maximo = int(min(255, (1.0 + sigma) * v)) 	#calcula o valor maximo
		borda = cv2.Canny(gray, minimo, maximo) 	#realiza a operacao de deteccao de bordas
		img = borda 								#a imagem de saida e a borda
		
	elif opc == 4:
		fgmask = fgbg.apply(frame, frameBlur, 0.0003) 										#realiza a subtacao de fundo entre o fundo e o frame atual
		ret, fgmask = cv2.threshold(fgmask, 127,255,cv2.THRESH_BINARY)						#aplica uma binarização para eliminar valores intermediarios
		kernel = np.ones((5, 5),np.uint8) 													#cria um kernel para realizar abertura/fechamento (elemento estruturante, nucleo)
		fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)			 				# realiza a abertura
		fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=2) 			#realiza a fechamento
		img = cv2.merge((fgmask&frame[:,:,0], fgmask&frame[:,:,1], fgmask&frame[:,:,2])) 	#a imagem de saida e um and entre todos os canais e a mascara

	elif opc == 5:
		img = frame 																		#a imagem de saida e a mesma da entrada
		# realiza a deteccao dos padroes
		faces = faceCascade.detectMultiScale(img, minNeighbors=5, minSize=(30, 30), maxSize=(200,200))
		for (x, y, w, h) in faces:															#para cada face detectada, resenha um retangulo
			cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
			
	elif opc == 6:
		hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) 										#converte a imagem para HSV
		hsv[:,:,1] = 0 																		#zera o canal S
		hsv[:,:,2] = 0 																		#zera o canal V
		img = hsv 																			#a imagem de saida e somente o canal H
		
	else:
		img = frame 																		#se nenhuma opcao foi selecionada, exibe a imagem de entrada

	# exibe a imagem 
	cv2.imshow('Visao Computacional - Gabriel Kirsten',img)
	
	#armazena a tecla pressionada de acordo com sua opcao
	k = cv2.waitKey(1)
	if k & 0xFF == ord('q'):
		break
	elif k & 0xFF == ord('a'):
		opc = 1
	elif k & 0xFF == ord('g'):
		opc = 2
	elif k & 0xFF == ord('c'):
		opc = 3
	elif k & 0xFF == ord('s'):
		frameFundo = frame 										#guarda o frame de fundo no momento que 's' foi pressionado
		frameBlur = cv2.GaussianBlur(frameFundo, (5,5), 0) 		#aplica um desfoque gaussiano para suavizar a imagem 
		fgbg = cv2.createBackgroundSubtractorMOG2() 			#cria o subtrator de fundo
		opc = 4
	elif k & 0xFF == ord('f'):
		opc = 5
	elif k & 0xFF == ord('h'):
		opc = 6
	else:
		continue

cap.release() 					#encerra a comunicacao com a webcam
cv2.destroyAllWindows() 		#fecha todas as janelas
