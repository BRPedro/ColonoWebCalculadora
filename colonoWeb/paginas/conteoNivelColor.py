#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from time import time

__author__ = "Pedro Barrantes R"
__date__ = "$11/10/2016 09:44:07 AM$"

import cv2
import numpy as np
import paginas.configuracion as conf


class ConteoCombinado:
    def __init__(self, direccion):
        self.dir = direccion  # direccion de la fisica de la imagen.
        self.imagen = cv2.imread(direccion)  # se carga la imagen que se encuentra en la direccion dir.
        self.matrizOrig = np.array(self.imagen)  # matriz int de la imagen.
        self.fila, self.columna, self.tipo = self.imagen.shape  # dimensiones de la imagen.
        self.centroides = []  # lista de coordenadas de los centros de los patrones.
        self.listaEstado = [False, False, False, False]  # lista para el manejo de los hilos.
        self.listacortes = [[], [], [], []]

    # ***************************************************************************************************

    """
    Metodo que busca los 8 vecinos mas cercanos de una coordenada (f,c)
    Recibe de parametros:
        f =  fila (int)
        c = columna (int)
        lista = lista de coordenadas ejemplo: [[2,3],[1,2], ...,[2,4]]
    Retorna True si tiene un vecino en la lista o Falso si no tiene vecino. 
    """

    def busqueda(self, f, c, lista):
        if lista.count([f - 1, c - 1]) > 0:
            return True
        if lista.count([f - 1, c]) > 0:
            return True
        if lista.count([f - 1, c + 1]) > 0:
            return True
        if lista.count([f, c + 1]) > 0:
            return True
        if lista.count([f + 1, c + 1]) > 0:
            return True
        if lista.count([f + 1, c]) > 0:
            return True
        if lista.count([f + 1, c - 1]) > 0:
            return True
        if lista.count([f, c - 1]) > 0:
            return True
        return False

    # ****************************************************************************************************************************************************************************

    """
    Metodo para calcular la distancia de dos puntos (F, C)
    Parametros:
            coordenada1: lista de int ejemplo: [0, 0]
            coordenada2: lista de int ejemplo: [0, 1]
    Retorna: 
            Resultado: float
    """

    def distaciaEntrePuntos(self, coordenada1, coordenada2):
        resultado = (((coordenada2[0] - coordenada1[0]) ** 2) + ((coordenada2[1] - coordenada1[01]) ** 2)) ** 0.5
        if (resultado < 0):  # si el valor se resultado es negativo se debe multiplicar por -1
            resultado *= -1
        return resultado

    # ****************************************************************************************************************************************************************************

    """
    Metodo que verifica los vecinos de los patrones y si existen patrones mas cercanos al limite minimo borra el patron con menor cantidad de coordenadas
    Parametros:
        listaGrupos: lista [][][]
        limite: int, limite de cercania
      Retorna: 
        Int[][][]
    """

    def agrupamientoXproximidad(self, listaGrupos,
                                limite):  # Este metodo se puede mejorar si se realiza un manejo mejor de los ciclos de busqueda en la lista.
        while True:  # Ciclo infinito el cual se detiene solo si ya se terminar de procesar listaGrupos  en su totalidad. Para ello se puede realizar varios recorridos a la lista.
            bandera = True
            i1 = 0
            while i1 < len(listaGrupos) - 1:  # Ciclo para recorrer cada sublistas de listaGrupos
                i2 = i1 + 1
                bandera2 = True
                while i2 < len(listaGrupos):
                    if (self.distaciaEntrePatrones(listaGrupos[i1], listaGrupos[i2], limite)):
                        if len(listaGrupos[i1]) > len(listaGrupos[i2]):
                            listaGrupos.pop(i2)
                        else:
                            listaGrupos.pop(i1)
                        bandera2 = False
                        break

                    i2 += 1
                if bandera2 == False:
                    bandera = False
                    break
                i1 += 1
            if bandera:
                break
        return listaGrupos

    # ****************************************************************************************************************************************************************************

    """
    Método encargado de agrupar los pixeles verdes de una imagen en listas de patrones este metodo esta diseñado para ejecutarse en hilos.
    Parametros:
        listapuntos: [[],[],..] lista con listas de las coordenadas de un pixel verde
        estado: int para controlar los hilos
    """

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

    # ****************************************************************************************************************************************************************************

    """
    Método encargado de agrupar los pixeles verdes de una imagen en listas de patrones.
    Parametros:
        listapuntos: [[],[],..] lista con listas de las coordenadas de un pixel verde
        estado: int para controlar los hilos
    """

    def agrupamientoXvecinosFinal(self, listapuntos):
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

    # ****************************************************************************************************************************************************************************

    """
    Método principal con hilos que calcula las coordenadas centrales de un patrón.
    Parametros:
        Listapuntos: [[[], []], [[]], ..] lista que contiene listas con las coordenadas de los parámetros.
        Limite: int limite mínimo aceptable de cantidad de pixeles de un patrón.
    """

    def centroidesBuscarPrimario(self, listapuntos, limite):
        self.centroidesBuscarSecundario(listapuntos, 0, limite)
        return

    # ****************************************************************************************************************************************************************************

    """
    Metodo secundario sin hilos que calcula las coordenadas centrales de un patrón.
    Parametros:
        listapuntos: [[[], []], [[]], ..] lista que contiene listas con las coordenadas de los parámetros.
        estado: int que cambia el estado de de la lista listaEstado, para identificar en que estado esta el hilo.
        limite: int límite mínimo aceptable de cantidad de pixeles de un patrón.
    """

    def centroidesBuscarSecundario(self, listapuntos, estado, limite):
        self.listaEstado[estado] = False
        for i in listapuntos:
            if len(i) > limite:
                minF, minC = self.fila - 1, self.columna - 1
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
                self.centroides.append([((maxC - minC) / 2) + minC, ((maxF - minF) / 2) + minF, len(i), len(i)])
        self.listaEstado[estado] = True
        return

    # ****************************************************************************************************************************************************************************

    """
    Método que inicia el conteo sobre la imagen.
    Parámetros:
        limitePatron: int valor mínimo que se acepta en cantidad de pixeles de un patrón.
        limiteCercania: float valor mínimo que se acepta de cercanía entre los parones.
        circulo: int tamaño de las marcas circulares.
    Retorno:
        [(int resultado conteo),(float tiempo de análisis)]
    """

    def inicioConteo(self, limitePatron, limiteCercania, circulo, verde):
        return self.contadorAgrupado(limitePatron, limiteCercania, circulo, verde)

    # ****************************************************************************************************************************************************************************

    """
    Método que inicia el conteo sobre la imagen el cual se realiza ejecutando varios hilos.
    Parámetros:
        limitePatron: int valor mínimo que se acepta en cantidad de pixeles de un patrón.
        limiteCercania: float valor mínimo que se acepta de cercanía entre los parones.
        circulo: int tamaño de las marcas circulares.
    Retorno:
        [(int resultado conteo),(float tiempo de análisis)]
    """

    def contadorAgrupado(self, limitePatron, limiteCercania, circulo, verde):
        tiempo_inicial = time()
        try:
            print "Paso 1 de 5"
            listapuntos = self.filtroVerde(verde)

            print "Paso 2 de 5"
            listapuntos = self.agrupamientoXvecinosInicial(listapuntos)

            print "Paso 3 de 5"
            self.centroidesBuscarPrimario(listapuntos, limitePatron)

            print "Paso 4 de 5"
            self.centroides = self.agrupamientoXproximidadMejorado(self.centroides, limiteCercania)

            print "Paso 5 de 5"
            tem = self.dibujarCirculos(circulo)

            print "FIN..."
            tiempo_final = time()
            tiempo_total = tiempo_final - tiempo_inicial
            tiempo_total /= 60.0

            return [tem, len(self.centroides), "{0:.2f}".format(tiempo_total)]
        except:
            return []

    # ****************************************************************************************************************************************************************************

    """
    Metodo que verifica los vecinos de los patrones y si existen patrones mas cercanos al limite minimo borra el patron con menor cantidad de coordenadas
    Parametros:
        listaGrupos: lista [][][]
        limite: int, limite de cercania
      Retorna:
        Int[][][]
    """

    def agrupamientoXproximidadMejorado(self, listaGrupos, limiteD):  # Este metodo se puede mejorar si se realiza un manejo mejor de los ciclos de busqueda en la lista.
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

    # ****************************************************************************************************************************************************************************

    """
    Método que calcula que el porcentaje de intensidad de verde que se permite con respecto al de los colores verde y rojo.
    Parámetros:
        rojo: int que representa el valor del rojo
        verde: int que representa el valor del verde
        azul: int que representa el valor del azul
        limite
    Retorna:
        True: si es la intensidad del verde es aceptable
        False: si el intensidad del verde no es aceptable
    """


    # ****************************************************************************************************************************************************************************

    """"
    Método que filtra la imagen y crea una lista con todas las coordenadas que corresponde a una intensidad de verde mayor.
    Retorna:
        Lista con sublistas que contienen las coordenadas de los pixeles verdes.

    """

    def filtroVerde(self,verdeP):
        listapuntos = []
        for f in range(self.fila):
            for c in range(self.columna):
                rojo, verde, azul = self.matrizOrig[f][c]
                if (rojo < verde) and (azul < verde):
                    if (rojo+azul)//2<verdeP:
                        listapuntos.append([[f, c]])
        return listapuntos


    # ****************************************************************************************************************************************************************************

    """
        Método encargado de agrupar los pixeles verdes de una imagen en listas de patrones este método está diseñado para ejecutar hilos dividiendo la lista en cuatro partes.
        Parámetros:
            listapuntos: [[], [],..] lista con listas de las coordenadas de un pixel verde
        Retorna:
            lista con lista de coordenadas que corresponde a los patrones
    """

    def agrupamientoXvecinosInicial(self, listapuntos):
        return self.agrupamientoXvecinos(listapuntos)

    # ****************************************************************************************************************************************************************************

    """
    Método que dibuja círculos sobre la imagen procesada.
    Parámetros:
        circulo: int con el tamaño del circulo a dibujar.
    Retorna:
        La imagen con los círculos dibujados.
    """

    def dibujarCirculos(self, circulo):
        tem = cv2.imread(self.dir)
        for i in self.centroides:
            cv2.circle(tem, (i[0], i[1]), circulo, (0, 0, 255), 0)
        cv2.imwrite('paginas\\static\\paginaP\\img\\imgContada.jpg', tem)
        return tem
        # ****************************************************************************************************************************************************************************

# __________________________________________________________________________________________________________________________________________________________________________________
