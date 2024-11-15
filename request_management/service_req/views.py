from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import ServiceRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ServiceRequestForm
from django.utils import timezone
class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    fields = ['request_type', 'details']  # Exclude 'customer'
    template_name = 'service_req/service_request_form.html'
    success_url = reverse_lazy('customer:dashboard')

    def form_valid(self, form):
        if not self.request.user.groups.filter(name='Customer').exists():
            raise PermissionDenied
        form.instance.customers = self.request.user
        return super().form_valid(form)

class ServiceRequestListView(ListView):
    model = ServiceRequest
    template_name = 'service_req/service_request_list.html'
    context_object_name = 'service_requests'
    def get_queryset(self):
        # Filter service requests by the logged-in user
        return ServiceRequest.objects.filter(customers=self.request.user)

class ServiceRequestDetailView(DetailView):
    model = ServiceRequest
    template_name = 'service_req/service_request_detail.html'
    context_object_name = 'service_request'

class ServiceRequestUpdateView(UpdateView):
    model = ServiceRequest
    template_name = 'service_req/service_request_form.html'
    form_class = ServiceRequestForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        print("Available form fields:", form.fields.keys()) 
        if user.groups.filter(name='CSR').exists():
            allowed_fields = ['status', 'support']
        else:
            allowed_fields = ['request_type', 'details']
        form.fields = {key: form.fields[key] for key in allowed_fields if key in form.fields}

        return form


    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.groups.filter(name='CSR').exists() or obj.status == 'Pending':
            return obj
        else:
            raise PermissionDenied("Only pending service requests can be updated.")
        
    def form_valid(self, form):
        if hasattr(form.instance, 'status') and form.cleaned_data.get('status') == 'Resolved':
            if not form.instance.date_resolved:  # Ensure resolved_date is set only once
                form.instance.date_resolved = timezone.now()
                
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy ('customer:dashboard_redirect')

class ServiceRequestDeleteView(DeleteView):
    model = ServiceRequest
    template_name = 'service_req/service_request_confirm_delete.html'
    context_object_name = 'service_request'
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
      
        if obj.status!='Pending':
            raise PermissionDenied("Only pending services requests can be deleted.")
        if not self.request.user.groups.filter(name='Customer').exists():
            raise PermissionDenied("Only customer can delete request")
            

        return obj

    def get_success_url(self):
        if self.request.user.groups.filter(name='Customer').exists():
            return reverse_lazy('customer:dashboard')

