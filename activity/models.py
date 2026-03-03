from django.db import models
from django.utils import timezone


class Employee(models.Model):
    ROLE_CHOICES = (
        ('Employee','Employee'),
        ('Group Head','Group Head'),
        ('HR','HR'),
    )
    staff_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')

  #  group_head = models.CharField(max_length=10, blank=True, null=True)
   # hr = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.staff_no} - {self.name}"

class WeeklyReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    current_week_activity = models.TextField()
    next_week_activity = models.TextField()
    leave_taken = models.CharField(max_length=100)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    gh_status = models.CharField(max_length=20, default="Pending")
    hr_status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(default=timezone.now)
