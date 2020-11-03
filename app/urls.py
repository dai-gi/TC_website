from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('member/', views.MemberView.as_view(), name='member'),
    path('search/', views.SearchView.as_view(), name='search'), 
    path('post/list', views.PostListView.as_view(), name='post_list'),
    path('post/list/member', views.PostListMemberView.as_view(), name='post_list_member'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/member', views.PostDetailMemberView.as_view(), name='post_detail_member'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('category/<str:category>/member', views.CategoryMemberView.as_view(), name='category'),
    path('work/list', views.WorkListView.as_view(), name='work_list'),
    path('work/new/', views.CreateWorkView.as_view(), name='work_new'),
    path('work/<int:pk>/', views.WorkDetailView.as_view(), name='work_detail'),
    path('work/<int:pk>/edit/', views.WorkEditView.as_view(), name='work_edit'),
    path('work/<int:pk>/delete/', views.WorkDeleteView.as_view(), name='work_delete'),
    path('work_category/<str:work_category>/', views.WorkCategoryView.as_view(), name='work_category'),
]