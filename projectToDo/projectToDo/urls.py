"""projectToDo URL Configuration

The `urlpatterns` list routes URLs to viewses. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function viewses
    1. Add an import:  from my_app import viewses
    2. Add a URL to urlpatterns:  path('', viewses.home, name='home')
Class-based viewses
    1. Add an import:  from other_app.viewses import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('tasks/', include("listWorkers.urls")),
    path('rest/', include("restToDoApp.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
