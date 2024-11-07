

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
    path('predict_response/', views.predict_response, name='predict_response'),
    path('predict_language/', views.predict_language, name='predict_language'),
    path('login/',views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("signup/",views.signup,name="signup"),
    path('create_mel_spectrogram/', views.create_mel_spectrogram, name='create_mel_spectrogram'),



    # Other URL patterns specific to your app...
]
