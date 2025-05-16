from django.urls import path
from . import views

urlpatterns = [
    path('', views.agendamento_criar, name='agendamento_criar'),
    path('painel-gerente/', views.painel_gerente, name='painel_gerente'),
    path('cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('confirmar/<int:agendamento_id>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('finalizar/<int:agendamento_id>/', views.finalizar_agendamento, name='finalizar_agendamento'),
    path('exportar-csv/', views.exportar_agendamentos_csv, name='exportar_agendamentos_csv'),
    path('agendamentos/', views.painel_users_list, name='painel_user'),  
    path('agendamentos/editar/<int:id>/', views.agendamento_editar, name='agendamento_editar'),
#   path('agendamento/<int:agendamento_id>/pdf/', views.baixar_agendamento_pdf, name='baixar_agendamento_pdf'),
    path('criar-admin/', views.criar_superusuario_temporario, name='criar_admin'),
]
