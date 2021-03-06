from django.urls import include, path
from django.contrib.auth.views import logout
from rest_framework.authtoken.views import obtain_auth_token



from .views import *


urlpatterns = [
  
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('decide/login/', LoginUserView.as_view(), name='auth_login'),
    path('decide/logout/', logout, name="auth_logout"),
    path('decide/register/', RegisterUserView.as_view(), name="auth_register"),
    path('decide/register/complete/', CompleteVotingUserDetails.as_view(), name='auth_register_complete'),
    path('decide/getVotingUser/', GetVotingUser.as_view(), name='auth_get_voting_user'),
    path('decide/getGenresByIds/', GetGenresByIds.as_view(), name='auth_get_voting_user_genre'),
   
    path('user/<int:id>/', GetUserDetailsView.as_view()),
   

    path('register/', RegisterView.as_view()),
    path('sign-in/', SigninView.as_view()),
    
    path('form-login/', LoginView.as_view()),
    path('login-bot/', CustomAuthToken.as_view()),
]
