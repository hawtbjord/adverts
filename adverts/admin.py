from django.contrib import admin
from .models import *

from .models import Category, Advert


admin.site.register(Advert)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Image)
admin.site.register(ModNote)


