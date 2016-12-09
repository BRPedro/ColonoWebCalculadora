from __future__ import unicode_literals

from django.db import models

class TC_PATRON(models.Model):
    ID_PARONT =models.AutoField(primary_key=True)
    FILA_P =   models.IntegerField(null=True)
    COLUMNA_P = models.IntegerField(null=True)

class TC_COORDENADA(models.Model):
    ID_COORDENADAN= models.AutoField(primary_key=True)
    FILA_C=models.IntegerField()
    COLUMNA_C=models.IntegerField()
    ID_TC_PATRON = models.ForeignKey(TC_PATRON,null=True)

