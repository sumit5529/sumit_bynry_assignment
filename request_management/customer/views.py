from django.views import View
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
# from requests.models import ServiceRequest
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from requests.models import ServiceRequest


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'customer/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email_domain = user.email.split('@')[-1]
            csr_email_domain = 'company.com'

            if email_domain == csr_email_domain:
                csr_group, created = Group.objects.get_or_create(name='CSR')
                user.groups.add(csr_group)
            else:
                customer_group, created = Group.objects.get_or_create(name='Customer')
                user.groups.add(customer_group)

            login(request, user)
            return redirect('customer:dashboard_redirect')
        return render(request, 'customer/register.html', {'form': form})
    

def dashboard_redirect(request):
    if request.user.groups.filter(name='CSR').exists():
        return redirect('csr:csr_dashboard')
    else:
        return redirect('customer:dashboard')

def career_page(request):
        return render(request, 'customer/career.html')
class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/dashboard.html'

    def get(self, request, *args, **kwargs):
        # Ensure the user is part of the 'Customer' group
        if not request.user.groups.filter(name='Customer').exists():
            return redirect('login')  # Redirect to login if not in Customer group
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add customer-specific data to the context
        # customer_service_requests = ServiceRequest.objects.filter(user=self.request.user)
        customer_service_requests = f"checking list of your request {self.request.user}"
        context['service_requests'] = customer_service_requests
        return context


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'customer/login.html'