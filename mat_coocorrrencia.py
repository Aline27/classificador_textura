import numpy as np
from math import log10



class Mat_coocorrencia(object):

    def __init__(self,n1,n2):
        self.mat_coocorrencia = np.zeros((n1,n1))
        self.mat_quantizada = np.zeros((256,256))
        self.descritores= np.zeros((16))

    def quantizacao(self, im,n1):
        vet_indices= np.array((range(n1)))
        vet_limites= np.linspace(0,100,n1+1)

        for i in range(0, 256):
            for j in range(0,256):
                for cont in range(1,n1+1):
                    if im[i,j]<=vet_limites[cont]:
                        self.mat_quantizada[i,j]=vet_indices[cont-1]
                        break

        return self.mat_quantizada

    def calc_haralick(self,im,n1):

        #matrix de coocorrencia
        # 0-> 0
        # 45-> 1
        # 90 -> 2
        # 135 ->  3
        vet_aux=np.linspace(0,12,4)
        for cont in range(0,4):
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
            energia=sum(sum(aux))

            mat_variancia=np.zeros((n1,n1))
            mat_entropia = np.zeros((n1, n1))
            mat_homogeneidade = np.zeros((n1, n1))

            for i in range(0,n1):
                for j in range(0,n1):
                    mat_variancia[i,j]=mat[i,j]*(i-j)**2
                    mat_homogeneidade[i,j]=mat[i,j]/(1+abs(i-j))
                    if mat[i,j] > 0:
                        mat_entropia[i,j]= mat[i,j]*log10((mat[i,j]))
                    else:
                        mat_entropia[i,j]=0


            variancia=sum(sum(mat_variancia))
            entropia= sum(sum(mat_entropia))
            homogeneidade=sum(sum(mat_homogeneidade))

            self.descritores[int(0+vet_aux[cont])]= energia
            self.descritores[int(1+vet_aux[cont])]= variancia
            self.descritores[int(2+vet_aux[cont])]= entropia
            self.descritores[int(3+vet_aux[cont])]= homogeneidade


        return self.descritores