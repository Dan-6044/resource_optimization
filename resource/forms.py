from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserPurpose, CompanyInfo, Project

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not any(char.isdigit() for char in password) \
                or not any(char.isupper() for char in password) or not any(char in '!@#$%^&*()' for char in password):
            raise ValidationError("Password must be at least 8 characters long, contain an uppercase letter, a number, and a symbol.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")


class UserPurposeForm(forms.ModelForm):
    class Meta:
        model = UserPurpose
        fields = ['purpose', 'role']
        widgets = {
            'purpose': forms.RadioSelect,
            'role': forms.RadioSelect,
        }


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['purpose', 'role']
        widgets = {
            'purpose': forms.RadioSelect(choices=CompanyInfo.PURPOSE_CHOICES),
            'role': forms.RadioSelect(choices=CompanyInfo.ROLE_CHOICES),
        }


from django import forms
from .models import Project, Task

# Form for creating or editing a Project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'duration', 'num_tasks', 'cost']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (in days)'}),
            'num_tasks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Tasks'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost'}),
        }

# Form for creating or editing a Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'start_date', 'end_date', 'resources_required', 'dependencies']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'End Date', 'type': 'date'}),
            'resources_required': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resources Required'}),
            'dependencies': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task Dependencies'}),
        }

from django import forms
from .models import PaymentMethod

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['card_type', 'card_number', 'cardholder_name', 'expiry_date']


# forms.py
from django import forms
from .models import BillingInfo

class BillingInfoForm(forms.ModelForm):
    class Meta:
        model = BillingInfo
        fields = ['owner_name', 'company_name', 'email', 'vat_number']


from django import forms
from .models import Profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
