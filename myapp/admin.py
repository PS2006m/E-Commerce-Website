from django.contrib import admin
from .models import User,Courses,Cart,ChatMessage
# Register your models here.
admin.site.register(User)
admin.site.register(Courses)
admin.site.register(Cart)
admin.site.register(ChatMessage)