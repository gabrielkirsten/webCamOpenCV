# WebCam OpenCV

This project is a software that performs real-time filtering image obtained by webcam, using python and openCV.

      Ps. Description in PT-BR

Atividade - Visão Computacional (Filtragem em tempo real)
------------------------------------------------------------------------
# Descrição

Desenvolvido em Python v2.7.12 utilizando como base a biblioteca OpenCV v3.0.0 
Sistema Operacional: Ubuntu 16.04 LTS 

Software desenvolvido para disciplina de Visão Computacional, foram dedicadas em um intervalo de duas semana, cerca de 8 horas de desenvolvimento.

A implementação, em geral, foi realizada sem muitas dificuldades.

A parte relacionada aos canais de cores, como RGB ou HSV foi obtida atraves da documentação do openCV (http://docs.opencv.org/) e também foi necessário alguns conhecimentos de tratamento de matrizes em python. 

O detector de bordas Canny foi tomado como base a documentação do openCV (http://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html?highlight=canny#cv2.Canny), aplicando os limites maximos e minimos fixos como 100 e 200 (a documentação recomenda a utilização na proporção entre 2:1 and 3:1,  http://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html#gsc.tab=0), o detector não funcionou corretamente quando a imagem era apresentada com variações de luminosidade. Então optou-se por calcular uma média. Como se tratava de uma imagem em tempo real onde o calculo foi obtido através do artigo http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/

Como base para o reconhecimento facial, foi utilizado como base o material contido no link  http://www.galirows.com.br/meublog/opencv-python/opencv2-python27/capitulo2-deteccao/reconhecimento-face/ o arquivo de padrões para o reconhecimento que foi sugerido pelo blog é disponibilizado pelo GitHub no link https://github.com/Itseez/opencv/tree/master/data/haarcascades no formato .XML com o nome de "haarcascade_frontalface_default.xml" com esse arquivo,foi utilizado o classificador do openCV CascadeClassifier() que carrega o arquivo de padrões e o detectMultiScale() que procura os padrões dentrodo frame. A especificação dos metodos para seu funcionamento foram detalhadas a partir da documentação do openCV (http://docs.opencv.org/) porém a maioria dos parâmetros passados para a função foram mantidos, considerando que eram as melhores escolhas.

Na parte de subtração de fundo, inicialmente foi lido o material da PUC-Rio (https://webserver2.tecgraf.puc-rio.br/~mgattass/ra/trb09/Guilherme/VisaoComputacional%20-%20Trabalho%202.htm) e implementado um método simples, onde percorria a matriz, e comparava a diferença da imagem atual com a imagem do fundo, considerando as duas em escala de cinza, como mostra o trecho de código abaixo:

  for i in range(len(img)):
  	for j in range(len(gray[0])):
  		if (gray[i][j] - frameFundo[i][j]) >= 50:
  			img[i][j] = gray[i][j]
  		else:
  			img[i][j] = 0

O metodo se mostrou muito lento, e com ruido. (posterior a esse exercicio, foi descoberto a origem da lentidão, as operações com matrizes podem ser eealizadas utilizando a biblioteca numpy, que utiliza as funções de item() e itemset() para obter e definir valores em matrizes de magens, essa função será utilizada na atividade de convolução). Para solucionar esse problema foi pesquisado sobre "Background substraction openCV" e então foi encontrado o método createBackgroundSubtractorMOG2() na biblioteca openCV que se mostrou mais eficaz, o método conta também com a opção de aprendizagemautomatica que aceita valores de 0 a 1 e o valor escolhido foi 0.0003 http://docs.opencv.org/2.4/modules/video/doc/motion_analysis_and_object_tracking.html?highlight=background#cv2.BackgroundSubtractorMOG para deixar a imagem ainda mais precisa, foi utilizadas operações morfologicas de abertura e fechamento de imagens binárias como já foram vistas anteriormenteutilizando imageJ, então nesse artigo foi encontrada os métodos para implementação das funções em openCV  http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html após obter a mascara que subtrai o fundo foi utilizado a operação de AND lógico, para exibir a imagem em colorido, como demonstrado a seguir:
img = cv2.merge((fgmask&frame[:,:,0], fgmask&frame[:,:,1], fgmask&frame[:,:,2]))
foi feito o AND entre cada canal do BGR do frame com a mascara fgmask e emseguida foi realizado a mesclagem de todas as cores compondo uma nova imagem que foi exibida.

(IMPORTANTE: O código foi gerado utilizando openCV v3.0.0 e não houve a possibilidade de rodar e testar no openCV v3.1.0)

#Etapas de desenvolvimento:
	- Estudo da abertura da utilização da webcam com openCV.
	- Implementação da apresentação da imagem.
	- Estudo de operações com matrizes em Python.
	- Implementação da parte relacionada com tratamento de cores.
	- Implementação do detector de bordas Canny.
	- Implementação do reconhecimento facial.
	- Implementação da subtração de fundo.

------------------------------------------------------------------------
#Utilização

	- Altere o diretorio no terminal linux com o comando 'cd' até a pasta
	onde se encontra o arquivo atividadeWebCam.py;
			(importante: o código não irá funcionar se o diretorio for
			 diferente, pois depende de importações de arquivos que estão
			  em caminhos relativos)
 	- Execute o código atividadeWebCam.py com o comando 
 	"python atividadeWebCam.py";
	- Utilize os comandos relacionados abaixo para navegação.

------------------------------------------------------------------------		
#ESTRUTURA DE DIRETORIOS	
    .
    |-- atividadeWebCam
    |	|-- atividadeWebCam.py (codigo em python)
    |	|-- README.txt (arquivo contendo informações do software)
    |	|-- haarcascade_frontalface_default.xml 
    |	|	(arquivo de padrões para o reconhecimento facial)


------------------------------------------------------------------------
#Comandos

	Comando			Descrição
	a				Zera os canais R e G deixando apenas o canal azul 
	g				Zera os canais R e B deixando apenas o canal verde 
	c				Aplica detecção de bordas de canny
	s				Realiza segmentação por subtração de fundo 
	f				Desenha um retângulo ou uma elipse ao redor das faces
					que aparecem na imagem 
	h				Transforma a imagem para o espaço HSV e zera os canais
				 	S e V, deixando apenas a matiz (Hue)
-------------------------------------------------------------------------
