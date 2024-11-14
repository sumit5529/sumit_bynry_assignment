from django.urls import path
from .views import RegisterView, dashboard_redirect,CustomerDashboardView ,CustomLoginView ,career_page# Import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

app_name = 'customer'  

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('dashboard-redirect/', dashboard_redirect, name='dashboard_redirect'),
    path('', career_page, name='career'), 
    path('dashboard/', CustomerDashboardView.as_view(), name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('customer:career')), name='logout')

]

