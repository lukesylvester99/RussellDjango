from django.urls import path
from . import views

urlpatterns = [
    path("<str:titer>/", views.display_graph, name="display_titer"),
]