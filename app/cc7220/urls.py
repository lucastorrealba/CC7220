from django.urls import path
from . import views

app_name = 'cc7220'

queries = [
    # Cantidad de Científicos por pais
    path(
        'q1/',
        views.q1,
        name='q1'
    ),
    # Mayores causas de muertes entre científicos
    path(
        'q2/',
        views.q2,
        name='q2'
    ),
    # Lista de ocupaciones científicas
    path(
        'q3/',
        views.q3,
        name='q3'
    ),
    # cantidad de cientificos por campo de estudio
    path(
        'q4/',
        views.q4,
        name='q4'
    )
]

requests = [
    path(
        '',
        views.Index.as_view(),
        name='index',
    ),
    # Cantidad de Científicos por pais
    path(
        'ccbc/',
        views.CCBC.as_view(),
        name='ccbc'
    ),
    # Mayores causas de muertes entre científicos
    path(
      'mcmc/',
      views.MCMC.as_view(),
      name='mcmc'
    ),
    # Lista de ocupaciones científicas
    path(
        'loc/',
        views.LOC.as_view(),
        name='loc'
    ),
    # cantidad de cientificos por campo de estudio
    path(
        'ccce/',
        views.CCCE.as_view(),
        name='ccce'
    ),
]

urlpatterns = queries + requests
