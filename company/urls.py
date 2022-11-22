from django.urls import path

from .views import (

    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,

    Company_list_view,
    Company_create_view,
    Company_detail_view,
    Company_update_view,

    icon_library,

)

app_name = "company"

urlpatterns = [

    # generic class based views
    path('', CompanyListView.as_view(), name='company-list'),
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<str:slug>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<str:slug>/update/', CompanyUpdateView.as_view(), name='company-update'),

    # function based views
    path('function/based-views/', Company_list_view, name='company-function-list'),
    path('function/based-views/create/', Company_create_view, name='company-function-create'),
    path('function/based-views/<str:slug>/', Company_detail_view, name='company-function-detail'),
    path('function/based-views/<str:slug>/update/', Company_update_view, name='company-function-update'),

    path('icon-library/icons/', icon_library, name='icon-library'),

]

