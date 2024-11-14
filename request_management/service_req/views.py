from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import ServiceRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
# ServiceRequest Create View
class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    fields = ['request_type', 'details']  # Exclude 'customer'
    template_name = 'service_req/service_request_form.html'
    success_url = reverse_lazy('customer:dashboard')

    def form_valid(self, form):
        # Automatically set the customer to the logged-in user
        if not self.request.user.groups.filter(name='Customer').exists():
            raise PermissionDenied
        form.instance.customers = self.request.user
        return super().form_valid(form)

# ServiceRequest List View
class ServiceRequestListView(ListView):
    model = ServiceRequest
    template_name = 'service_req/service_request_list.html'
    context_object_name = 'service_requests'
    def get_queryset(self):
        # Filter service requests by the logged-in user
        return ServiceRequest.objects.filter(customers=self.request.user)

# ServiceRequest Detail View
class ServiceRequestDetailView(DetailView):
    model = ServiceRequest
    template_name = 'service_req/service_request_detail.html'
    context_object_name = 'service_request'

# ServiceRequest Update View
class ServiceRequestUpdateView(UpdateView):
    model = ServiceRequest
    fields = ['request_type', 'details', 'status'] 
    template_name = 'service_req/service_request_form.html'

    # def get_fields(self):
    #     # Get the user from the request
    #     user = self.request.user

    #     # Check if the user belongs to the 'CSR' group
    #     if user.groups.filter(name='CSR').exists():
    #         # Allow CSR group members to only modify 'status' and 'details'
    #         return ['status', 'details']
    #     else:
    #         # Non-CSR users can modify all fields
    #         return ['name', 'description', 'status', 'details']

    def get_object(self, queryset=None):
        # Get the object to be updated
        obj = super().get_object(queryset)

        # Check if the status is 'Pending' only for non-CSR users
        if self.request.user.groups.filter(name='CSR').exists() or obj.status == 'Pending':
            return obj
        else:
            raise PermissionDenied("Only pending service requests can be updated.")
        
    def form_valid(self, form):
        # Before saving, check if the status is 'Resolved' and resolved_date is null
        if form.cleaned_data['status'] == 'Resolved' and not form.instance.resolved_date:
            # Set the resolved_date to the current date
            form.instance.resolved_date = timezone.now()

        # Save the form data (this will save the changes)
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.groups.filter(name='Customer').exists():
            return reverse_lazy('customer:dashboard')

# ServiceRequest Delete View
class ServiceRequestDeleteView(DeleteView):
    model = ServiceRequest
    template_name = 'service_req/service_request_confirm_delete.html'
    context_object_name = 'service_request'
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"ok {obj.pending}")
        print(obj.status)
        if obj.status!='Pending':
            raise PermissionDenied("Only pending services requests can be deleted.")
        if not self.request.user.groups.filter(name='Customer').exists():
            raise PermissionDenied("Only customer can delete request")
            

        return obj

    def get_success_url(self):
        if self.request.user.groups.filter(name='Customer').exists():
            return reverse_lazy('customer:dashboard')

