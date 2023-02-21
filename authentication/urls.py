from django.urls import path


from knox import views as knox_views
from authentication.views import  LoginView, RegisterView, ProfileView


app_name = 'authentication'

urlpatterns = [
  path('create/',RegisterView.as_view(), name="create"),
  path('profile/', ProfileView.as_view(), name='profile'),
  path('login/', LoginView.as_view(), name='knox_login'),
  path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
  path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall') ]
