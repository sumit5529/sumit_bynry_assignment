from django.db import models
from customer.models import CustomUser

class ServiceRequest(models.Model):
    REQUEST_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    REQUEST_TYPE_CHOICES = [
        ('Leak', 'Gas Leak'),
        ('Installation', 'New Installation'),
        ('Maintenance', 'Maintenance'),
        ('Billing', 'Billing Inquiry'),
        ('Other', 'Other'),
    ]

    customers = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    # file = models.FileField(upload_to='service_requests/', blank=True, null=True) 
    details = models.TextField()
    support = models.TextField()
    status = models.CharField(choices=REQUEST_STATUS, max_length=20, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.request_type} - {self.customers.username}"
    @property
    def pending(self):
        return self.status == 'Pending'
