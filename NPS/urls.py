from django.contrib import admin
from django.urls import path
import base.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.home),
	path('login/', views.loginpage),
	path('logout/', views.logoutview),
	path('news/', views.news),
    path('about/', views.about),
    path('contact/', views.contact),
    path('projects/', views.projects),
    path('students/', views.students),
   path('news/<str:pk>/', views.new),
   path('create-news', views.newscreate),
   path('profile/', views.profileredirect),
   path('profile/<str:pk>/', views.profilepage),
   path('project/<str:pk>', views.projectpage),
   path('project/edit/<str:pk>', views.projectedit),
   path('news/edit/<str:id>', views.newsedit),
   path('create-project', views.projectcreate),
   path('project/edit/<str:pk>/delete/<str:id>', views.deleteimg),
   path('project/edit/<str:pk>/deletefile/<str:id>', views.deletefile),
   path('project/edit/<str:pk>/deletemember/<str:id>', views.deletemember),
   path('project/delete/<str:pk>', views.deleteproject),
   path('profile/<str:pk>/skill-delete/<str:id>', views.deleteskill),
   path('news/delete/<str:id>', views.deletenews),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)