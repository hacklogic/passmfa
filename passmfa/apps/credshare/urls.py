from django.urls import path
from .views import LoginView,IndexView,get_otp,userlogout,NewView,EditView,testView
from .views import credentials_list, add_credentials, edit_credentials, delete_credentials,qrcode,addshare_credentials,SharetomeView,getshare_credentials,delshare_credentials



urlpatterns = [
    # Other URL patterns...

    #path("test1/",Test_View.as_view(template_name="index4.html"),),

    #path("otp/",IndexView.as_view(template_name="otp.html"),name='otp'),

    #用户首页
    path("index/",IndexView.as_view(template_name="index.html"),name='index'),

    #path("index3/",IndexView.as_view(template_name="index3.html"),name='index3'),
    #path("index2/",IndexView.as_view(template_name="ui_modals.html"),name='index2'),
    #登录 登出
    path("login/",LoginView.as_view(template_name="login.html"),name='login'),
    path("logout/",userlogout,name='userlogout'),

    #读取qrcode图片
    path('qrcode/', qrcode, name='qrcode'),
    #获取otp
    path('otp/<int:credential_id>/', get_otp, name='get_otp'),

    #添加页
    path("new/",NewView.as_view(template_name="new.html"),name='new'),
    #修改页
    path("edit/<int:id>/",EditView.as_view(template_name="edit.html"),name='edit'),

    #共享给我的
    path('share/', SharetomeView.as_view(template_name="sharetome.html"), name='sharetome'),

    #path('list/', credentials_list, name='credentials_list'),
    #path('add/', add_credentials, name='add_credentials'),

    #path('edit/<int:id>/', edit_credentials, name='edit_credentials'),

    #删除我的
    path('delete/<int:id>/', delete_credentials, name='delete_credentials'),

    #add new share
    #path('addshare/<int:id>/', addshare_credentials, name='addshare_credentials'),

    #删除共享，不能刪除共享组
    #delete share
    path('delshare/<int:id>/', delshare_credentials, name='delshare_credentials'),

    #path('getshare/<int:id>/', getshare_credentials, name='getshare_credentials'),
    #get shared credentials
    #path("register/",ProfileView.as_view(template_name="profile.html"),),

    #404 页面
    path('404/', testView.as_view(template_name="404.html"),name='404'),

    #my profile
    #edit profile




]