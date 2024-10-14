from django.contrib import admin
from django.urls import path, include
from api.views import api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls") ),
    path('members/', include("members.urls") ),
    path('members/', include("django.contrib.auth.urls") ),
    path('api/', api.urls)
]
