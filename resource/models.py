# models.py
from django.db import models
from django.contrib.auth.models import User

class UserPurpose(models.Model):
    PURPOSE_CHOICES = [
        ('work', 'Work'),
        ('school', 'School'),
        ('personal', 'Personal'),
        ('nonprofit', 'Non-Profit'),
    ]
    ROLE_CHOICES = [
        ('businessOwner', 'Business Owner'),
        ('teamLeader', 'Team Leader'),
        ('teamMember', 'Team Member'),
        ('freelancer', 'Freelancer'),
        ('director', 'Director'),
        ('cLevel', 'C-Level'),
        ('vp', 'VP'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('teacher', 'Teacher'),
        ('administrator', 'Administrator'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
        ('staff', 'Board Member'),
        ('employee', 'Employee'),
        ('itStaff', 'IT Staff'),
        ('other', 'Other'),
    ]
    

    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.purpose} - {self.role}"
    



class CompanyInfo(models.Model):
    PURPOSE_CHOICES = [
        ('Only Me', 'Only Me'),
        ('2-5', '2-5'),
        ('6-10', '6-10'),
        ('11-15', '11-15'),
        ('16-25', '16-25'),
        ('26-50', '26-50'),
        ('51-100', '51-100'),
        ('101-500', '101-500'),
    ]

    ROLE_CHOICES = [
        ('1-19', '1-19'),
        ('20-49', '20-49'),
        ('50-99', '50-99'),
        ('100-250', '100-250'),
        ('251-500', '251-500'),
        ('501+', '501+'),
    ]
    
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.purpose} - {self.role}"



class ManagementPurpose(models.Model):
    
    purpose = models.CharField(max_length=100)

    def __str__(self):
        return self.purpose


    
class FocusArea(models.Model):
    purpose = models.CharField(max_length=100)

    def __str__(self):
        return self.purpose

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure this links to the user who created the project
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # Duration of the project in days
    num_tasks = models.IntegerField()  # Number of tasks for the project
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of the project

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')  # Relating task to a project
    name = models.CharField(max_length=100)  # Task name
    start_date = models.DateField()  # Task start date
    end_date = models.DateField()  # Task end date
    resources_required = models.CharField(max_length=255)  # Resources required for the task
    dependencies = models.TextField(blank=True, null=True)  # Optional field for task dependencies

    def __str__(self):
        return self.name

class Resource(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    resource_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.resource_name

class Team(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    member_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    additional_qualification = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.member_name



class Email(models.Model):
    SENT = 'sent'
    SCHEDULED = 'scheduled'
    EMAIL_STATUS_CHOICES = [
        (SENT, 'Sent'),
        (SCHEDULED, 'Scheduled'),
    ]

    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    receiver = models.EmailField()
    sent_time = models.DateTimeField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=EMAIL_STATUS_CHOICES,
        default=SENT
    )
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.subject



class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    # Other fields as needed
    
    def __str__(self):
        return self.card_number
    




# models.py
from django.db import models

class PaymentMethod(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.card_type} - {self.card_number[-4:]}"  # Display last 4 digits of the card

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'







class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming the invoice is related to a user
    invoice_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField()

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.amount}"

    class Meta:
        ordering = ['-invoice_date']




class BillingInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing_info')
    owner_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    vat_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.owner_name} - {self.company_name}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Whether the notification has been read

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"


from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.DateField()  # e.g., weeks, months
    expiry_date = models.DateField()
    payment_method = models.CharField(max_length=50)  # card or mpesa
    payment_status = models.CharField(max_length=50, default='Pending')  # Can be Pending, Completed, etc.

    # Card payment details
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_cvv = models.CharField(max_length=3, blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)

    # M-Pesa payment details
    mpesa_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.plan_name} - {self.user.username} - {self.payment_status}"





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

