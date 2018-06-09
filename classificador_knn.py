import sys
import numpy as np
from operator import itemgetter
from scipy import stats
import time

def read_carac (arq, N,qtd):
	cont=0
	matriz = np.zeros((N, qtd))
	for row in arq:
		values = row.split()
		matriz[cont,:]=values[0:qtd]
		cont += 1

	return matriz

def read_label(arq,N):

	label = np.zeros((N,1))
	cont=0
	for row in arq:
		if row == "Apuleia\n":
			label[cont]=0
		elif row == "Aspidosperma\n":
			label[cont] = 1
		elif row == "Astronium\n":
			label[cont] = 2
		elif row == "Byrsonima\n":
			label[cont] = 3
		elif row == "Calophyllum\n":
			label[cont] = 4
		elif row == "Cecropia\n":
			label[cont] = 5
		elif row == "Cedrelinga\n":
			label[cont] = 6
		elif row == "Cochlospermum\n":
			label[cont] = 7
		else:
			print("erro")

		cont+=1

	return label

def KNN_Classification(matriz_train,matriz_test,label_train,label_test,N_train,N_test,k,qtd):

	error_num=0
	label_result_array = np.zeros((N_test, 1))
	for i_test in range(0,N_test):
		flag=0
		aux=np.ones((k,2))
		l=0
		print("Teste "+str(i_test))
		matriz_distance=(matriz_train[:,:]-matriz_test[i_test,:])**2
		vet_distance=matriz_distance.sum(axis=1)
		vet_distance=np.sqrt(vet_distance)

		for i_train in range(0,N_train):
			if (i_train < k):
				#print vet_distance[i_train]
				aux[l, 0] = vet_distance[i_train]
				aux[l, 1] = label_train[i_train]
				l+=1
			if (i_train==k):
				aux = sorted(aux, key=itemgetter(0))
				aux = np.array(aux)
			if (i_train >=k):
				for q in range(0, k):
					if (vet_distance[i_train] < aux[q, 0]):
						for cont in range(k - 1, q):
							aux[cont, 0] = aux[cont - 1, 0]
							aux[cont, 1] = aux[cont - 1, 1]
						aux[q, 0] = vet_distance[i_train]
						aux[q, 1] = label_train[i_train]
						break

		#print (label_test[i_test])
		#print (aux)
		label_result=stats.mode(aux)
		label_result = label_result[0]
		#print (int(label_result[0,1]))
		label_result_array[i_test]=label_result[0,1]
		if(label_result[0,1]!=label_test[i_test]):
			#print("Errou")
			error_num+=1

	return label_result_array, error_num


def calc_rates(errors, N_test):

	hit_rate=(float(N_test-errors)/float(N_test))*100

	print("A taxa de acertos e de:"+str(hit_rate)+"%")
	print("A taxa de erros e de:"+str(100-hit_rate)+"%")


def Create_ConfusionMat(label1,label2,n):

	confusion_mat=np.zeros((8,8))
	for i in range(0,n):
		confusion_mat[int(label1[i]),int(label2[i])]+=1

	print confusion_mat
	return confusion_mat


text1=str(sys.argv[1])
text2=str(sys.argv[2])
k=int(str(sys.argv[3]))
archive = open("Caracteristicas/"+text1, 'r')
archive2 = open("Caracteristicas/"+text2, 'r')
archive3 = open("Caracteristicas/label_train.txt", 'r')
archive4 = open("Caracteristicas/label_test.txt", 'r')

N_train=1120
N_test=1120
qtd=int(str(sys.argv[4]))

matriz_train=read_carac(archive,N_train,qtd)
matriz_test=read_carac(archive2,N_test,qtd)
label_train=read_label(archive3,N_train)
label_test=read_label(archive4,N_test)

print("Calculando...")
start = time.time()
label_array,errors=KNN_Classification(matriz_train,matriz_test,label_train,label_test,N_train,N_test,k,qtd)
rates=calc_rates(errors, N_test)
confusion_mat=Create_ConfusionMat(label_test,label_array,N_test)
end = time.time()
print("Tempo de execucao: ", end - start)

archive.close()
archive2.close()









