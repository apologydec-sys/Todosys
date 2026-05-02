from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('todos/', views.index, name='todo-index'),
    path('update/<int:pk>/', views.update, name='todo-update'),
    path('delete/<int:pk>/', views.delete, name='todo-delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/reminders/', views.reminders_api, name='reminders-api'),
    # PWA
    path('manifest.json', views.manifest, name='pwa-manifest'),
    path('sw.js', views.service_worker, name='pwa-sw'),
    path('offline/', views.offline, name='pwa-offline'),
]

