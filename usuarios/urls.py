from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('login/', views.login_view, name='login_view'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('gerenciar/', views.listar_usuarios, name='listar_usuarios'),
    path('excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('desativar/<int:user_id>/', views.desativar_usuario, name='desativar_usuario'),
    path('reativar/<int:user_id>/', views.reativar_usuario, name='reativar_usuario'),

]