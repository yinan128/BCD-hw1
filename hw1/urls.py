"""hw1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from iw import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('systems/heating/', views.heating, name='heating'),
    path('systems/ventilation/', views.ventilation, name='ventilation'),
    path('systems/ac/', views.ac, name='ac'),
    path('systems/lighting/', views.lighting, name='lighting'),
    path('planImage/<int:id>', views.getPlanImage, name='planImage'),
]
