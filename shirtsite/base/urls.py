from django.urls import path
from . import views
from .views import SizeCreateView,UserLoginView,UserRegistration,ImageRequestView,UpdateOrderInfo,UpdateImageRequest,DesignList
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path("", views.home_test , name="home"),
    path('design/',views.design , name='design'),
    path('size/',SizeCreateView.as_view(), name='size'),
    path('order-summary/' , views.OrderDetails , name="order_summary"),
    path('payment/',views.PaymentGateway,name="payment"),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',UserRegistration.as_view(),name='register'),
    path('aidesign-create/',views.Aidesign,name='aides'),
    path('ai-request/',ImageRequestView.as_view(),name='aires'),
    path('size-edit/<str:pk>/',UpdateOrderInfo.as_view(),name='size_edit'),
    path('ai-request/<str:pk>/',UpdateImageRequest.as_view(),name='aires_edit'),
    path('design_list/', DesignList.as_view(),name='design_list')

    #path('design_edit/<str:pk>/',views.DesignDetailView,name='design_edit')
]