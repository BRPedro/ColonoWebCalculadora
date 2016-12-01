import os
from io import BytesIO

from django.http import HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

from django.shortcuts import render, HttpResponse

from paginas.conteoNivelColor import ConteoCombinado
from paginas.reporte import Reporte
import paginas.reporte as rep
from .forms import UploadFileForm, Parametros
import paginas.configuracion as conf
import paginas.formatoImagen as formatosI
import cv2
from .forms import Parametros

"""
Lanza la pagina principal
"""
def index(request):
    return render(request,'paginas/home.html')

"""
Lanza la pagina con la imagen cargada
"""
def cargado(request):
    return render(request,'paginas/imagCarga.html')

def cargadoConImagenO(request):
    return render(request,'paginas/imagCarga2.html')

def imagenO(request):
    logo={'c':'paginaP/img/imagTempW.tif'}
    return render(request,'paginas/imagSeleccion.html',logo)

"""
Lanza pagina con el formulario de cargado de imagen
"""
def formularioImagen(request):
    if request.method == 'POST':
        if 'b1' in request.POST:
            form = UploadFileForm(request.POST, request.FILES)
            copiaImagenServidor(request.FILES['archivo'])
            temI=cv2.imread('paginas\static\paginaP\img\imagTempW.tif')
            formatosI.cambio(temI,"imagTempW.jpg")
            return render(request,'paginas/imagCarga2.html')
    else:
        form = UploadFileForm()

    return render(request, 'paginas/cargarImg.html', {'form': form})

"""
Lanza procesamiento de la imagen, para luego presentar resultados.
"""
def prosesamiento(request):
    conteo=ConteoCombinado('paginas\static\paginaP\img\imagTempW.tif')

    datos=conf.cargar()
    print datos.ruido,datos.proximidad,datos.circulo
    resultado=conteo.inicioConteo(int(datos.ruido),float(datos.proximidad),int(datos.circulo),int(datos.verde))
    reporte=Reporte(datos.altura,datos.escala,datos.ruido,datos.proximidad,datos.circulo,resultado[1],0)
    resultado={'res': resultado[1],'tie':resultado[2]
               }

    datos.imp()
    rep.guardarReporte(reporte)
    return render(request,'paginas/imagProc2.html',resultado)

"""
Copia imagen cargada al servidor.
"""
def copiaImagenServidor(f):
    with open('paginas\static\paginaP\img\imagTempW.tif', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
"""
Lanza pagina con el formulario de ajuste de parametros.
"""
def ajusteParametros(request):
    if request.method == 'POST':
        form = Parametros(request.POST)
        if form.is_valid():
            print "Error"
            if 'b2' in request.POST:
                return HttpResponseRedirect('/')
        else:
            print "bien"
        if 'b1' in request.POST:
            conf.guardar(request.POST['altura'],request.POST['escala'],request.POST['ruido'],request.POST['proximidad'],request.POST['circulo'],request.POST['verde'])
            return HttpResponseRedirect('/')
        elif 'b2' in request.POST:
            return HttpResponseRedirect('/')
        elif 'b3' in request.POST:
            carga=conf.predeterminado()
            form = Parametros(initial={'escala': carga.escala,'altura':carga.altura,'ruido':carga.ruido,'proximidad':carga.proximidad,'circulo':carga.circulo,'verde':carga.verde})
            return render(request, 'paginas/ajustes.html', {'form': form})
        form = Parametros(request.POST, request.FILES)
        return render(request,'paginas/imagCarga2.html')
    else:
        carga=conf.cargar()
        form = Parametros(initial={'escala': carga.escala,'altura':carga.altura,'ruido':carga.ruido,'proximidad':carga.proximidad,'circulo':carga.circulo,'verde':carga.verde})
    return render(request, 'paginas/ajustes.html', {'form': form})

"""Funcion que crea un PDF con los resultados y parametros con que se analizo la imagen """
def crearPDF(request):

    fecha=datetime.now()
    fechaStr=str(fecha.day)+"/"+str(fecha.month)+"/"+str(fecha.year)

    reporte=rep.cargarReporte()
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition']='attachment; filename=reporte.pdf'
    buffer=BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)

    c.setLineWidth(.3)
    c.setFont('Helvetica',22)
    c.drawString(30,750,'Reporte de resutados')

    c.setFont('Helvetica-Bold',22)
    c.drawString(460,750,fechaStr)

    c.setFont('Helvetica',12)
    c.drawString(30,710,"Altura de vuelo:")
    c.drawString(150,710,str(reporte.altura))
    c.drawString(30,695,"Escala pixel x metro:")
    c.drawString(150,695,str(reporte.escala))
    c.drawString(30,680,"Filtro de ruido:")
    c.drawString(150,680,str(reporte.ruido))
    c.drawString(30,665,"Proximidad:")
    c.drawString(150,665,str(reporte.proximidad))
    c.drawString(30,650,"Escala circulo:")
    c.drawString(150,650,str(reporte.circulo))
    c.drawString(30,615,"Conteo de plantas:")
    c.drawString(150,615,str(reporte.conteo))

    c.save()
    pdf = buffer.getvalue()
    response.write(pdf)
    return response

def animacio(request):
    return render(request,'paginas/animacion.html')