from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(Category)