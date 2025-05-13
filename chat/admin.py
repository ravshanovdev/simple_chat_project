from django.contrib import admin
from .models import Message, Sticker


admin.site.register([Message, Sticker])

