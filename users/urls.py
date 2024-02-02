from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
#url patterns has list of all urls corresponding to the views and the webpages
urlpatterns = [
    path('', views.login, name = 'login'),
    path('login/', views.login_page, name = 'login_page'),
    path('logout/', views.logout_page, name= 'logout'),
    path('register/', views.register, name = 'register'),
    path('profile/<str:username>', views.profile, name = 'profile'),
    #path('editprofile/<str:username>', views.edit_profile, name = 'edit_profile'),
    path('userprofiles/', views.user_profiles, name = 'user_profiles'),
]
