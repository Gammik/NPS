from django.contrib import admin
from .models import News, profile, Skills, project, projectfile, projectimage, projectmember
# Register your models here.
admin.site.register(News)
admin.site.register(profile)
admin.site.register(Skills)
admin.site.register(project)
admin.site.register(projectfile)
admin.site.register(projectimage)
admin.site.register(projectmember)