# models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=255, default='')

    def save(self, *args, **kwargs):
        # Populate the username and email fields from the associated User model
        self.username = self.user.username
        self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.city}'


class Worker(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    is_worker = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('works', 'Works'),
        ('sick', 'Sick'),
        ('not_working_today', 'Not Working Today'),
        ('on_holiday', 'On Holiday'),
        ('pending', 'Pending'),  # Add 'pending' status
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    worker_name = models.CharField(max_length=255, default='')  # Add worker_name field

    def save(self, *args, **kwargs):
        # Populate worker_name with the username from associated User model
        self.worker_name = self.user_profile.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.worker_name


class Report(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('deleted', 'Deleted by Administrator'),
    ]

    ISSUE_CHOICES = [
        ('garbage', 'Garbage'),
        ('graffiti', 'Graffiti'),
        ('other', 'Other'),
    ]

    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    garbage_image = models.ImageField(blank=True, null=True)
    street_image = models.ImageField(blank=True, null=True)
    commentary = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    issue_type = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.street} - {self.status}"

class AssignedReport(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    worker_name = models.CharField(max_length=255, default='')
    report_name = models.CharField(max_length=255, default='')


    def save(self, *args, **kwargs):
        self.worker_name = self.worker.user_profile.user.username
        self.report_name = self.report.street
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assigned report: {self.report_name} - Worker: {self.worker_name}"

