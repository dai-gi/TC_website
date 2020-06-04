from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('work', views.WorkListView.as_view(), name='work_list'),
    path('work-detail/<int:pk>/', views.WorkDetailView.as_view(), name='work_detail'),
]