from django.contrib import admin
from .models import Movieinfo, Movielink, User, Useraction, Usercomment

# Register your models here.
admin.site.register(Movieinfo)
admin.site.register(Movielink)
admin.site.register(User)
admin.site.register(Useraction)
admin.site.register(Usercomment)

