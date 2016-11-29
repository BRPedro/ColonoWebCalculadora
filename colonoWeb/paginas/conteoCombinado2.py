import threading
from time import time

__author__ = "Pedro Barrantes R"
__date__ = "$11/10/2016 09:44:07 AM$"

import cv2
import numpy as np
"""
Clase encargada de realizar el conteo de pinnas en una plantacion
Su constructor recibe un string con la direccion de la imagen.
"""
class ConteoCombinado:
    def __init__(self, direccion):
        self.paso=0
        self.dir = direccion
        self.imagen = cv2.imread(direccion)
        self.matrizOrig = np.array(self.imagen)
        self.fila, self.columna, self.tipo = self.imagen.shape
        self.newData = np.zeros(shape=(self.fila, self.columna))
        self.centroides = []
        self.listaEstado=[False,False,False,False]
        self.listaEstado2=[False,False]
        self.listacortes=[[],[],[],[]]


    def inicioConteo(self, limitePatron, limiteCercania, circulo):
        return self.contadorAgrupadoMejorado(limitePatron, limiteCercania, circulo)


    def filtroVerdes(self):
        listapuntos = []
        for f in range(self.fila):
            for c in range(self.columna):
                rojo, verde, azul = self.matrizOrig[f][c]
                if (rojo < verde) and (azul < verde):
                    listapuntos.append([[f, c]])
                    self.newData[f][c] = 1
                else:
                    self.newData[f][c] = 0
        return listapuntos

    def dibujarCirculos(self,circulo):
        tem = cv2.imread(self.dir)
        for i in self.centroides:
            cv2.circle(tem, (i[0], i[1]), circulo, (0, 0, 255), 0)
        cv2.imwrite('paginas\\static\\paginaP\\img\\imgContada.tif', tem)

    def contadorAgrupadoMejorado(self, limitePatron, limiteCercania, circulo):
        tiempo_inicial = time()
        try:
            print "Paso 1 de 5"
            listapuntos=self.filtroVerdes()

            print "Paso 2 de 5",1234
            listapuntos = self.agrupamientoXvecinos(listapuntos)

            print "Paso 3 de 5"
            self.centroidesBuscarSecundario2(listapuntos,limitePatron)

            print "Paso 4 de 5"
            self.centroides = self.agrupamientoXproximidadMejorado(self.centroides, limiteCercania)
            tem = cv2.imread(self.dir)

            print "Paso 5 de 5"
            self.dibujarCirculos(circulo)

            tiempo_final = time()
            tiempo_total = tiempo_final - tiempo_inicial
            tiempo_total /= 60

            return [tem, len(self.centroides), int(tiempo_total)]
        except:
            return []

    """
      Metodo que verifica los vecinos de los patrones y si existen patrones mas cercanos al limite minimo borra el patron con menor cantidad de coordenadas
      Parametros:
          listaGrupos: lista [][][]
          limite: int, limite de cercania
        Retorna:
          Int[][][]
      """

    def agrupamientoXproximidadMejorado(self, listaGrupos,
                                        limiteD):  # Este metodo se puede mejorar si se realiza un manejo mejor de los ciclos de busqueda en la lista.
        listaGrupos = sorted(listaGrupos, key=lambda x: x[2], reverse=True)
        largo = len(listaGrupos) - 1
        indice = 0
        while indice < largo:
            indice2 = indice + 1
            while indice2 < largo + 1:
                resultado = self.distaciaEntrePuntos(listaGrupos[indice], listaGrupos[indice2])
                if resultado <= float(limiteD):
                    listaGrupos.pop(indice2)
                    largo -= 1
                else:
                    indice2 += 1
            indice += 1
        return listaGrupos

    def agrupamientoXvecinos(self, listapuntos):
        while True:
            inicio, siguiente = 0, 1
            bandera = True
            while siguiente < len(listapuntos):
                bandera2 = True
                for lis in listapuntos[inicio]:
                    if self.busqueda(lis[0], lis[1], listapuntos[siguiente]):
                        bandera2 = False
                        bandera = False
                        listapuntos[inicio] = listapuntos[inicio] + listapuntos[siguiente]
                        listapuntos.pop(siguiente)
                        break
                if bandera2:
                    inicio += 1
                    siguiente += 1
            if bandera:
                break
        return listapuntos


    def centroidesBuscarSecundario2(self,listapuntos,limite):
        for i in listapuntos:
            if len(i)>limite:
                minF, minC = self.fila-1, self.columna-1
                maxF, maxC = 0, 0
                for ii in i:
                    if ii[0] < minF:
                        minF = ii[0]
                    if ii[0] > maxF:
                        maxF = ii[0]
                    if ii[1] < minC:
                        minC = ii[1]
                    if ii[1] > maxC:
                        maxC = ii[1]
                self.centroides.append([((maxC-minC) / 2) + minC,((maxF-minF) / 2) + minF,len(i),len(i)])
        return


def centroidesBuscarPrimario2(self, listapuntos, limite):
    self.centroidesBuscarSecundario(listapuntos, limite)
    return