"""drinks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from bartender import settings
from drinks import views as drinks
from barkeep import views as barkeep
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.auth_login, name='login'),
    path('logout/', auth_views.auth_login, name='logout'),
    path('ingredients/new/', drinks.ingredients),
    path('ingredients/', drinks.ingredients),
    path('ingredient_types/new/', drinks.ingredient_types),
    path('ingredient_Types/<int:ingredient_type_id>', drinks.ingredient_types),
    path('ingredient_types/', drinks.ingredient_types),
    path('', drinks.index, name='index'),
    path('drinks/new', drinks.drink_new),
    path('drinks/<int:drink_id>', drinks.drinks),
    path('drinks/', drinks.drinks),
    path('pour/', drinks.pour),
    path('restock/', barkeep.index)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
