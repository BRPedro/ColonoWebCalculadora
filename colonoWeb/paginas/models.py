from __future__ import unicode_literals

from django.db import models

class TC_PATRON(models.Model):
    idpatron =models.AutoField(primary_key=True)
    filap =   models.IntegerField(null=True)
    columnap = models.IntegerField(null=True)
    contadorp = models.IntegerField(default=0)

class TC_COORDENADA(models.Model):
    idcoordenada= models.AutoField(primary_key=True)
    filac=models.IntegerField()
    columnac=models.IntegerField()
    idtablapatron = models.ForeignKey(TC_PATRON,on_delete=models.CASCADE)

