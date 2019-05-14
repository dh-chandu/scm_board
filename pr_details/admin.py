from django.contrib import admin

# Register your models here.
from .models import Branch, Tag, Pr
admin.site.register(Branch)
admin.site.register(Tag)
admin.site.register(Pr)

