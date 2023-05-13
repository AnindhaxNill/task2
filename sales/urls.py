from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from sales import views

urlpatterns = [
    path('sales_list/',views.SalesList.as_view(),),
    path('salesdetail/<int:id>/', views.SalesDetail.as_view()),
    path('salespdf/', views.SalesPdf.as_view()),
]
