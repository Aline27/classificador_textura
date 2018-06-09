import sys
import numpy as np
from operator import itemgetter
from scipy import stats
import time
from dados import Dados
import glob
from mat_coocorrrencia import Mat_coocorrencia


N_train=1120
N_test=1120
im_train=[Dados() for i in range(N_train)]
im_test=[Dados() for i in range(N_test)]
cont_train=0
cont_test=0

name_images=glob.glob('Carvao/*.tif')
name_images.sort()

niveis = 5
caracteristicas=16
matTrain_coocorrencia=np.zeros((N_train,caracteristicas))
matTest_coocorrencia=np.zeros((N_test,caracteristicas))
labelTrain= []
labelTest= []
#metodo=int(str(sys.argv[1]))
metodo=0
         # metodo 0-> 
         # metodo 1-> 
         # metodo 2 -> 
         # metodo 3 ->

if (metodo==0):
 #   mat_hisTrain = np.zeros((N_train, 2 * n + 1))
 #   mat_hisTest = np.zeros((N_test, 2 * n + 1))

    for linha in range(0,2240,280):
        print linha
        for i1 in range(0,140):
            print ('treino'+str(i1))
            im_train[cont_train].read_info(name_images[linha+i1])
            image = im_train[cont_train].imagem
            coocorrencia = Mat_coocorrencia(niveis,caracteristicas)
            mat_quantizada=coocorrencia.quantizacao(image, niveis)
            descritores= coocorrencia.calc_haralick(mat_quantizada,niveis)
            im_train[cont_train].atributos= descritores
            matTrain_coocorrencia[cont_train, :] = im_train[cont_train].atributos
            labelTrain.append(im_train[cont_train].label_im)
            cont_train+=1
        for i2 in range(140,280):
            print ('teste'+str(i2))
            im_test[cont_test].read_info(name_images[linha+i2])
            image=im_test[cont_test].imagem
            coocorrencia = Mat_coocorrencia(niveis, caracteristicas)
            mat_quantizada = coocorrencia.quantizacao(image, niveis)
            descritores = coocorrencia.calc_haralick(mat_quantizada, niveis)
            im_test[cont_test].atributos = descritores
            matTest_coocorrencia[cont_test, :] = im_test[cont_test].atributos
            labelTest.append(im_test[cont_test].label_im)
            cont_test += 1

        np.savetxt('Caracteristicas/haralick_train.txt', matTrain_coocorrencia, delimiter=' ')
        np.savetxt('Caracteristicas/haralick_test.txt', matTest_coocorrencia, delimiter=' ')
        np.savetxt('Caracteristicas/label_train.txt', labelTrain, delimiter=' ',fmt="%s")
        np.savetxt('Caracteristicas/label_test.txt', labelTest, delimiter=' ',fmt="%s")




else:
    print("Metodo invalido")





