from django.urls import path
from .views import (AllEmployeeView,
                    DetailEmployeeView,
                    CreateLikeView,
                    AllLikeView,
                    ChangePasswordView,
                    )
from django.views.generic import TemplateView


urlpatterns = [
    path('', AllEmployeeView.as_view(), name='home'),
    path('change_confirmation/', TemplateView.as_view(
         template_name='change_confirmation.html'),
         name='confirm'),
    path('employee/<str:slug>/', DetailEmployeeView.as_view(), name='detail'),
    path('employee/<str:slug>/add_like/', CreateLikeView.as_view(),
         name='like'),
    path('employee/<str:slug>/all_likes/', AllLikeView.as_view(),
         name='like_all'),
    path('<str:department_slug>/', AllEmployeeView.as_view(),
         name='by_category'),
    path('<str:slug>/change_password/', ChangePasswordView.as_view(),
         name='change_password'),

    ]
