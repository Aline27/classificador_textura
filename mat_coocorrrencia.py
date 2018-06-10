import numpy as np
from math import log,sqrt
import cv2


class Mat_coocorrencia(object):

    def __init__(self,n1):
        self.mat_coocorrencia = np.zeros((n1,n1))
        self.mat_quantizada = np.zeros((256,256))
        self.descritores= np.zeros((7))

    def quantizacao(self, im,n1):
        vet_indices= np.array((range(n1)))
        vet_limites= np.linspace(0,256,n1+1)

        div= 256 / n1
        im_quantizada= (im /(256/div))*div

        # for i in range(0,256):
        #     for j in range(0,256):
        #         for cont in range(0,n1):
        #             if im_quantizada[i,j]==vet_limites[cont]:
        #                 im_quantizada[i,j]=vet_indices[cont]
        #                 break

        #   for i in range(0, 256):
        #     for j in range(0,256):
        #         for cont in range(1,n1+1):
        #             if im[i,j]<=vet_limites[cont]:
        #                 self.mat_quantizada[i,j]=vet_indices[cont-1]
        #                 break

        self.mat_quantizada=im_quantizada
        return self.mat_quantizada

    def calc_haralick(self,im,n1):

        #matrix de coocorrencia
        # 0-> 0
        # 45-> 1
        # 90 -> 2
        # 135 ->  3
        vet_aux=np.linspace(0,12,4)
        SMA=0
        energia=0
        variancia=0
        entropia=0
        homogeneidade=0
        contraste=0
        correlacao=0
        for cont in range(0,4):
            self.mat_coocorrencia[:,:]=0
            for i in range(0, 255):
                for j in range(0,255):
                    
                        if cont==0:
                            self.mat_coocorrencia[int(im[i,j]),int(im[i,j+1])]+=1
                        elif cont==1:
                            if i>0:
                                self.mat_coocorrencia[int(im[i,j]),int(im[i-1,j+1])]+=1
                        elif cont==2:
                            if i>0 and j>0 :
                                self.mat_coocorrencia[int(im[i,j]),int(im[i-1,j])]+=1
                        else:
                            self.mat_coocorrencia[int(im[i,j]),int(im[i-1,j-1])]+=1

            div= sum(sum(self.mat_coocorrencia))
            self.mat_coocorrencia=self.mat_coocorrencia/div
            mat=self.mat_coocorrencia

            #descritores de haralick
            aux=mat**2
            SMA+=sum(sum(aux))
            energia+=sqrt(SMA)

            mat_variancia=np.zeros((n1,n1))
            mat_entropia = np.zeros((n1, n1))
            mat_homogeneidade = np.zeros((n1, n1))
            mat_contraste = np.zeros((n1, n1))

            media_i=0
            media_j=0
            for i in range(0,n1):
                for j in range(0,n1):
                    mat_variancia[i,j]=mat[i,j]*(i-j)**2
                    mat_homogeneidade[i,j]=mat[i,j]/(1+abs(i-j))
                    mat_contraste[i,j]=mat[i,j]*(i-j)**2
                    media_i=i*mat[i,j]+media_i
                    media_j=j*mat[i,j]+media_j
                    if mat[i,j] > 0:
                        mat_entropia[i,j]= - mat[i,j]*log((mat[i,j]),2)
                    else:
                        mat_entropia[i,j]=0

            variancia_i=0
            variancia_j=0
            for i in range(0,n1):
                for j in range(0,n1):
                    variancia_i=mat[i, j] * (i - media_i) ** 2+variancia_i
                    variancia_j=mat[i, j] * (j - media_j) ** 2+variancia_j

            dvp_i = sqrt(variancia_i)
            dvp_j = sqrt(variancia_j)

            for i in range(0,n1):
                for j in range(0,n1):
                    aux_correl=mat[i, j] * ((i-media_i)*(j-media_j)/(dvp_i*dvp_j))

            correlacao+=aux_correl
            variancia += sum(sum(mat_variancia))
            entropia += sum(sum(mat_entropia))
            homogeneidade += sum(sum(mat_homogeneidade))
            contraste = sum(sum(mat_contraste)) + contraste


        self.descritores[0]= SMA/4
        self.descritores[1]= energia/4
        self.descritores[2]= variancia/4
        self.descritores[3]= entropia/4
        self.descritores[4]= homogeneidade/4
        self.descritores[5]= contraste/4
        self.descritores[6]= correlacao/4


        return self.descritores