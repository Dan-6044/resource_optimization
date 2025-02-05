from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import UserPurpose, FocusArea, CompanyInfo, ManagementPurpose, Project

# Unregister the original User model
admin.site.unregister(User)

# Register the User model again with any custom configuration (optional)
@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    # Customize the UserAdmin if needed
    pass


# Register the model with the admin site
@admin.register(UserPurpose)  # Replace UserPurpose with your model name
class UserPurposeAdmin(admin.ModelAdmin):
    list_display = ('id', 'purpose', 'role')  # Adjust fields as necessary
    search_fields = ('purpose', 'role')  # Fields to be searchable
    list_filter = ('purpose',)  # Add filters to the admin panel


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('purpose', 'role')
    list_filter = ('purpose', 'role')


@admin.register(ManagementPurpose)
class ManagementPurposeAdmin(admin.ModelAdmin):
    list_display = ('id', 'purpose')  # Display these fields in the admin list view
    search_fields = ('purpose',)  # Add a search box for the purpose field

@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ('purpose',)
    search_fields = ('purpose',)

from django.contrib import admin
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'num_tasks', 'cost')  # Only valid fields from Project model
    list_filter = ('duration',)  # You can add valid fields for filtering
    search_fields = ('name',)  # Optional: Allow searching by project name

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date', 'resources_required', 'dependencies', 'cost', 'priority')
    list_filter = ('project', 'start_date', 'end_date')  # Valid filters for Task model
    search_fields = ('name', 'project__name')  # Search by task name and related project name

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)

from .models import Resource, Team, Project
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_name', 'provider', 'capacity', 'location', 'cost', 'project')  # Fields to display in list view
    search_fields = ('resource_name', 'provider', 'location')  # Allow search by these fields
    list_filter = ('project', 'provider')  # Filter by project and provider
    ordering = ('project', 'resource_name')  # Order by project and resource name

class TeamAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'role', 'email', 'profile_picture', 'project')  # Fields to display in list view
    search_fields = ('member_name', 'role', 'email')  # Allow search by these fields
    list_filter = ('project', 'role')  # Filter by project and role
    ordering = ('project', 'member_name')  # Order by project and member name

# Register models to appear in the admin interface
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Team, TeamAdmin)



from django.contrib import admin
from .models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'status', 'sent_time', 'scheduled_time')
    list_filter = ('status',)
    search_fields = ('subject', 'sender', 'receiver')
    date_hierarchy = 'sent_time'

admin.site.register(Email, EmailAdmin)

# admin.py
from django.contrib import admin
from .models import PaymentMethod

@admin.register(PaymentMethod)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'card_number', 'cardholder_name', 'expiry_date')
    search_fields = ('user__username', 'card_number', 'cardholder_name')
    list_filter = ('card_type',)





# admin.py
from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'amount', 'invoice_date', 'user')
    search_fields = ('invoice_number', 'user__username')
    list_filter = ('invoice_date',)

admin.site.register(Invoice, InvoiceAdmin)
# admin.py
from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'time', 'is_read')
    list_filter = ('is_read', 'time')  # Filter notifications by read status and time
    search_fields = ('user__username', 'message')  # Search by username or message
    actions = ['mark_as_read']

    # Action to mark notifications as read
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"

admin.site.register(Notification, NotificationAdmin)

from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'price', 'expiry_date', 'payment_method', 'payment_status', 'card_number', 'mpesa_number')
    search_fields = ('user__username', 'plan_name', 'payment_method')
    list_filter = ('payment_status', 'plan_name', 'payment_method')
    list_display_links = ('user', 'plan_name')

    # You can also customize the fields displayed in the form when adding/editing a Subscription
    fields = ('user', 'plan_name', 'price', 'period', 'expiry_date', 'payment_method', 'payment_status', 
              'card_number', 'card_cvv', 'card_expiry_date', 'mpesa_number')