from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('samples/', views.samples_by_experiment, name='samples_by_experiment'),
    path('/filtered-samples', views.filter_samples, name='filter_samples'),
    path('export-csv-query/', views.export_csv_query, name='export_csv_query'),
    path('export-csv/<int:experiment_id>/', views.export_csv_by_exp, name='export_csv_by_exp'),
    #path('titer/', views.titer, name='titer')
]