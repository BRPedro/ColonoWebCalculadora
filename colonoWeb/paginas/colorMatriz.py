
class ColorMatriz:
    def __init__(self,color,banda):
        self.color=color
        self.matriz=banda.ReadAsArray()

    def numeroFilas(self):
        return len(self.matriz)

    def numeroColumnas(self):
        return len(self.matriz[0])

    def getValorPixelPosicion(self,fila,columna):
        return self.matriz[fila][columna]

    def setValorPixelPosicion(self,fila,columna,valor):
        self.matriz[fila][columna]=valor

    def imprimir(self):
        for i in self.matriz:
            print i