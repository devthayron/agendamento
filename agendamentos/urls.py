from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_agendamento, name='pagina_agendamento'),
    path('painel-gerente/', views.painel_gerente, name='painel_gerente'),
    path('cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('dashboard/', views.dashboard_gerente, name='dashboard_gerente'),
    path('confirmar/<int:agendamento_id>/', views.confirmar_agendamento, name='confirmar_agendamento'),
    path('finalizar/<int:agendamento_id>/', views.finalizar_agendamento, name='finalizar_agendamento'),
    path('exportar-csv/', views.exportar_agendamentos_csv, name='exportar_agendamentos_csv'),
    path('agendamentos', views.user_agendamentos_list,name='meus_agendamentos'),
    path('agendamentos/editar/<int:id>/', views.agendamento_edit, name='editar_agendamento'),
    path('agendamento/<int:agendamento_id>/pdf/', views.baixar_agendamento_pdf, name='baixar_agendamento_pdf'),

]