from django.urls import path
from . import views

urlpatterns = [
    path('get_data/', views.get_data, name='get_data'),
    path('head_offices/', views.get_head_offices, name='get_head_offices'),
    path('branches/', views.get_branches, name="get_branches"),
    path('detail/<int:pk>/', views.detail, name="detail"),
    path('<str:headOfficeCode>/<str:branchOfficeCode>/<str:headOffice>/<str:branchOffice>.html', views.detail_view, name='detail_view'),
]