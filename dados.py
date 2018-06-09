import sys
import numpy as np
import cv2
import glob
import time

class Dados(object):

    def __init__(self):
        self.label_im="xx"
        self.caminho_im="xx"
        self.imagem=np.zeros((2,2))
        self.atributos=np.zeros(9)

    def read_info(self,linha):

        self.caminho_im = linha
        aux = linha.split('_')[0]
        aux = aux.split('/')[1]
        self.label_im = aux
        self.imagem = cv2.imread(self.caminho_im, 0)
        return self



