from django.urls import path
from .views import LoginView,IndexView,get_otp
from .views import credentials_list, add_credentials, edit_credentials, delete_credentials,read_qrcode,confirmshare_credentials,SharetomeView,getshare_credentials



urlpatterns = [
    # Other URL patterns...

    #path("test1/",Test_View.as_view(template_name="index4.html"),),
    path('api/get_otp/<int:credential_id>/', get_otp, name='get_2fa_code'),
    #path("otp/",IndexView.as_view(template_name="otp.html"),name='otp'),
    path("index/",IndexView.as_view(template_name="index.html"),name='index'),

    #path("index3/",IndexView.as_view(template_name="index3.html"),name='index3'),
    #path("index2/",IndexView.as_view(template_name="ui_modals.html"),name='index2'),
    path("login/",LoginView.as_view(template_name="login.html"),name='login'),
    path('read-qrcode/', read_qrcode, name='read_qrcode'),

    path('list/', credentials_list, name='credentials_list'),
    path('add/', add_credentials, name='add_credentials'),
    path('edit/<int:id>/', edit_credentials, name='edit_credentials'),
    path('delete/<int:id>/', delete_credentials, name='delete_credentials'),

    path('confirmshare/<int:id>/', confirmshare_credentials, name='confirmshare_credentials'),

    path('getshare/<int:id>/', getshare_credentials, name='getshare_credentials'),
    path('share/', SharetomeView.as_view(template_name="sharetome.html"),name='sharetome'),
    #path("register/",ProfileView.as_view(template_name="profile.html"),),

]