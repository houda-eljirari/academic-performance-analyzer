"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentViewSet, ModuleViewSet
from students.import_views import ImportStudentsView

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'modules',  ModuleViewSet,  basename='module')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/import/students/', ImportStudentsView.as_view(), name='import-students'),
    path('api/analytics/', include('analytics.urls')), 
     path('api/ml/', include('ml_models.urls')),
]