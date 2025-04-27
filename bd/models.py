from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content_hash = models.TextField(default="")
    requirements = models.TextField(blank=True, null=True)
    beneficiaries = models.TextField(blank=True, null=True) # Salary, vacation and other benefits
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    salary = models.CharField(max_length=200, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200, unique=True)
    category = models.CharField(max_length=200, blank=True, null=True) # Frontend development, Backend development, Full Stack development, Data Science, App development, UI/UX, Manager, Marketing
    is_suitable = models.BooleanField(default=False)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('FT', 'Full Time'),
            ('PT', 'Part Time'),
            ('CT', 'Contract'),
            ('FL', 'Freelance')
        ],
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-date_posted']