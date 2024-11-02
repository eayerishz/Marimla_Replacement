from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Declined", "Declined"),
        ("Completed", "Completed"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()  # Changed to TextField for longer descriptions
    location = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    approved_by_user = models.BooleanField(default=False)
    approved_by_admin = models.ForeignKey(
        User, null=True, blank=True, related_name="approved_projects", on_delete=models.SET_NULL
    )
    declined_by_admin = models.ForeignKey(
        User, null=True, blank=True, related_name="declined_projects", on_delete=models.SET_NULL
    )
    declined_by_user = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def total_cost(self):
        return sum(
            element.materials.aggregate(total=models.Sum('total_cost'))['total'] or 0
            for element in self.elements.all()
            if element.materials.exists()
        )

    def approve_project(self, user):
        self.status = "Approved"
        self.start_date = timezone.now()
        self.approved_by_user = True
        self.approved_by_admin = user
        self.save()

    def complete_project(self):
        self.status = "Completed"
        self.end_date = timezone.now()
        self.save()


class ProjectElement(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="elements"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Element of {self.project.name}"


from django.db import models

class Material(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    element = models.ForeignKey(
        'ProjectElement', related_name="materials", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    qty = models.FloatField()
    unit = models.CharField(max_length=50)
    price_per_qty = models.FloatField()
    markup_percentage = models.FloatField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )

    @property
    def total_cost(self):
        return self.qty * self.price_per_qty * (1 + self.markup_percentage / 100)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    materials = models.ManyToManyField(Material, related_name='pricings')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pricings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)  # New field for approval status

    def __str__(self):
        return f'Pricing for {self.project.name} on {self.date}'
