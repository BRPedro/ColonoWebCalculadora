from django.contrib import admin

# Register your models here.
from paginas.models import TC_PATRON, TC_COORDENADA

admin.site.register(TC_PATRON)
admin.site.register(TC_COORDENADA)