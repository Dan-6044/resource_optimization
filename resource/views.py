from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from .forms import SignUpForm, UserPurposeForm, CompanyInfoForm
from datetime import datetime, timedelta
from .models import ManagementPurpose, FocusArea, Project, Project, Task, Resource, Team
from .models import Email, PaymentMethod, Invoice, BillingInfo,Subscription
import json




##############CREATING ACCOUNT####################
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm  # Make sure to import your SignUpForm

def signup_new(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user but don't save it to the database yet
            user = form.save(commit=False)
            # Set the password
            user.set_password(form.cleaned_data['password'])
            # Save the user to the database
            user.save()

            # Authenticate the user
            authenticated_user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if authenticated_user is not None:
                # Log the user in
                login(request, authenticated_user)
                messages.success(request, "Account created and logged in successfully.")
                return redirect('what_brings_you_here_today')
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'signup-new.html', {'form': form})



################BRINGS YOU HERE##################
def what_brings_you_here_today(request):
    if request.method == 'POST':
        form = UserPurposeForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data to the database
            return redirect('how_many_people_work_at_your_company')  
    else:
        form = UserPurposeForm()
    
    return render(request, 'what-brings-you-here-today.html', {'form': form})

#################PEOPLE WORKING############################
def how_many_people_work_at_your_company(request):
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('select_what_youd_like_to_manage'))  # Redirect after saving
    else:
        form = CompanyInfoForm()

    return render(request, 'how-many-people-work-at-your-compan.html', {'form': form})



################PRICING#######################
def pricing(request):
    return render(request, 'pricing.html')

####################SELECT WHAT YOU'D MANAGE########################
def select_what_youd_like_to_manage(request):
    if request.method == 'POST':
        selected_purpose = request.POST.get('purpose')
        if selected_purpose:
            # Create a new ManagementPurpose entry
            ManagementPurpose.objects.create(purpose=selected_purpose)
            # Redirect to a success page or another view as needed
            return redirect('pricing')  # Replace with your success page URL
    return render(request, 'select-what-youd-like-to-manage.html')  # Render the form again if not POST


###############FOCUS ON################
def focus_on(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        
        if purpose:
            # Create a new FocusArea instance without the user field
            focus_area = FocusArea(purpose=purpose)
            focus_area.save()
            messages.success(request, 'Focus area saved successfully!')
            return redirect('signin')  # Change this to the view you want to redirect to

        messages.error(request, 'Please select a purpose.')
        
    return render(request, 'focus-on.html')  # Replace with your template

################LOGGING IN#####################
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect(reverse('home_dashboard', args=[user.id]))  # Redirect to your desired page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'signin_new.html')  # Replace with your template

###########logout#############
def custom_logout(request):
    # Log the user out
    logout(request)
    
    # Redirect to a specific URL after logout (e.g., home page or login page)
    return redirect('home')  # Change 'home' to the URL name where you want the user to be redirected

################HOME PAGE##############
def home(request):
    return render(request, 'home.html')

##################DASHBAOARD HOMEPAGE#########################

def home_dashboard(request, user_id):
    # You can fetch user details or any related information here
    user = get_object_or_404(User, id=user_id)  # Assuming you are using Django's User model
    return render(request, 'home_dashboard.html', {'user': user})

from django.utils import timezone

def my_work(request, user_id):
    user = request.user  # Get the logged-in user
    projects = Project.objects.filter(user=user)

    tasks_data = []  # List to hold tasks data
    
    # Collect task data for each project
    for project in projects:
        tasks = Task.objects.filter(project=project)
        
        for task in tasks:
            tasks_data.append({
                'task_name': task.name,
                'start_date': task.start_date,
                'end_date': task.end_date,
            })
    
    # Pass tasks data and projects data to the template
    projects_data = []
    for project in projects:
        # Get team members for the project
        team_members = Team.objects.filter(project=project)
        
        # Sum up the resource costs for the project
        resources = Resource.objects.filter(project=project)
        total_budget = sum(resource.cost for resource in resources)

        # Calculate completed tasks and progress for the current project
        tasks = Task.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(end_date__lte=timezone.now()).count()
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        projects_data.append({
            'project': project,
            'team_members': team_members,
            'total_budget': total_budget,
            'progress': round(progress),  # Round progress to an integer
        })
    
    return render(request, 'mywork.html', {
        'projects_data': projects_data,
        'tasks_data': tasks_data  # Pass tasks data to the template
    })



################VISUALIZATION DASHBOARD###########################
def  dashboard(request, user_id):
    # You can fetch user details or any related information here
    user = get_object_or_404(User, id=user_id)  # Assuming you are using Django's User model
    return render(request, 'dashboard.html', {'user': user})



################CALENDAR VIEWING############################
def calendar_view(request):
    # Get the current date and time
    today = datetime.today()

    # Get the month and year from query parameters, default to current month/year if not provided
    try:
        current_month = int(request.GET.get('month', today.month))
        current_year = int(request.GET.get('year', today.year))
    except ValueError:
        # If there is a ValueError (like empty values or invalid month/year), default to current date
        current_month = today.month
        current_year = today.year

    # Validate that the month is between 1 and 12
    if current_month < 1 or current_month > 12:
        # If month is invalid, set to current month
        current_month = today.month

    # Calculate first and last days of the current month
    first_day_of_month = datetime(current_year, current_month, 1)
    last_day_of_month = datetime(current_year, current_month + 1, 1) - timedelta(days=1) if current_month < 12 else datetime(current_year + 1, 1, 1) - timedelta(days=1)

    # Fetch tasks for the current month
    tasks = Task.objects.filter(
        start_date__lte=last_day_of_month.date(),  # Convert to date
        end_date__gte=first_day_of_month.date()   # Convert to date
    )

    # Prepare calendar data
    calendar = []
    days_in_month = (last_day_of_month - first_day_of_month).days + 1
    # Start from the first weekday of the month (to align the calendar properly)
    start_day = first_day_of_month.weekday()

    # Create an empty list for the first week (fill the beginning with empty cells)
    week = [''] * start_day

    for i in range(days_in_month):
        day = first_day_of_month + timedelta(days=i)
        day_date = day.date()  # Convert to date for comparison
        # Gather tasks that are on this day
        day_tasks = [task.name for task in tasks if task.start_date <= day_date <= task.end_date]

        # Append the day and its tasks
        week.append({'day': day.day, 'tasks': day_tasks})

        # If it's the end of the week (Saturday), start a new week
        if len(week) == 7:
            calendar.append(week)
            week = []

    # Add the last incomplete week (if any)
    if len(week) > 0:
        while len(week) < 7:
            week.append('')
        calendar.append(week)

    # Prepare month navigation
    prev_month = current_month - 1 if current_month > 1 else 12
    prev_year = current_year if current_month > 1 else current_year - 1
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1

    context = {
        'calendar': calendar,
        'month_name': first_day_of_month.strftime('%B'),
        'year': current_year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today.day,
    }

    return render(request, 'calendar.html', context)


################BILLING PAGE INFO#########################
# viewing billing page
@login_required
def billings(request, user_id):
    payment_methods = PaymentMethod.objects.filter(user_id=user_id)  # Ensure user_id is used
    invoices = Invoice.objects.filter(user_id=user_id)
    billing_info = BillingInfo.objects.filter(user_id=user_id)

    for payment_method in payment_methods:
        print(payment_method.id)  # Debugging: Check if id is empty or None
        payment_method.expiry_date = payment_method.expiry_date.strftime('%Y-%m') if payment_method.expiry_date else None

    return render(request, 'billing.html', {
        'payment_methods': payment_methods,
        'invoices': invoices,
        'billing_info': billing_info
    })

###############CARDS INFO######################
# creating payment cards
def payment_methods_view(request):
    if request.method == 'POST':
        # Get data from the POST request
        card_type = request.POST.get('cardType')  # Visa or MasterCard
        card_number = request.POST.get('card_number')
        cardholder_name = request.POST.get('cardholder_name')
        expiry_date = request.POST.get('expiry_date')

        # Ensure expiry_date is in the correct format (YYYY-MM-DD)
        if expiry_date:
            try:
                # Add the default day "01" to the expiry_date to convert it to a valid date format
                expiry_date = f"{expiry_date}-01"
                # Try to parse it into a valid datetime object to check if the format is correct
                datetime.strptime(expiry_date, "%Y-%m-%d")
            except ValueError:
                return HttpResponse("Invalid expiry date format. Please provide a valid date.", status=400)
        
        # Ensure all required fields are provided
        if card_type and card_number and cardholder_name and expiry_date:
            # Create a new PaymentMethod instance
            payment_method = PaymentMethod(
                user=request.user,  # Associate with the logged-in user
                card_type=card_type,
                card_number=card_number,
                cardholder_name=cardholder_name,
                expiry_date=expiry_date
            )
            payment_method.save()  # Save the new payment method to the database
            referer = request.META.get('HTTP_REFERER', '/')
            return redirect(referer) # Redirect to the same page (or any other page you want)
        else:
            # If any field is missing, you can handle the error
            return HttpResponse("All fields are required.", status=400)
    else:
        # Get payment methods for the logged-in user to display in the template
        payment_methods = PaymentMethod.objects.filter(user=request.user)
        return render(request, 'billing.html', {'payment_methods': payment_methods , })

# Editing payment card
@csrf_exempt
def edit_payment_method(request, payment_method_id):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            
            # Get the payment method object
            payment_method = get_object_or_404(PaymentMethod, pk=payment_method_id)

            # Get the new values from the request
            card_type = data.get('cardType')
            card_number = data.get('cardNumber')
            cardholder_name = data.get('cardholderName')
            expiry_date = data.get('expiryDate')
            
           # Handle expiry date
            expiry_date = data.get('expiryDate')  # Expecting 'YYYY-MM'
            if expiry_date:
                try:
                    expiry_date = f"{expiry_date}-01"  # Add default day
                    payment_method.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
                except ValueError:
                    return JsonResponse({'success': False, 'error': 'Invalid expiry date format'})
            
            # Update the payment method fields
            if card_type:
                payment_method.card_type = card_type
            if card_number:
                payment_method.card_number = card_number
            if cardholder_name:
                payment_method.cardholder_name = cardholder_name
            if expiry_date:
                payment_method.expiry_date = expiry_date
            
            # Save the updated payment method
            payment_method.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# deleting payment info
def delete_payment_method(request, payment_method_id):
    # Ensure the user is logged in and trying to delete their own payment method
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to delete a payment method.")
        return redirect('signin')  # Redirect to login if not authenticated

    # Get the payment method object or 404 if it doesn't exist
    payment_method = get_object_or_404(PaymentMethod, pk=payment_method_id, user=request.user)

    # Delete the payment method
    payment_method.delete()

    # Show success message and redirect to the payment methods page
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


#############INVOICE INFO################
# creating invoice
@csrf_exempt
@login_required
def create_invoice(request):
    if request.method == 'POST':
        invoice_number = request.POST['invoice_number']
        amount = request.POST['amount']
        invoice_date = request.POST['invoice_date']
        user = request.user  # Assuming the invoice is for the logged-in user

        # Create the new invoice and save it to the database
        Invoice.objects.create(
            user=user,
            invoice_number=invoice_number,
            amount=amount,
            invoice_date=invoice_date
        )

        referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)



###########BILLING INFO###################
# creating billing info
@login_required
def add_billing_info(request):
    if request.method == 'POST':
        BillingInfo.objects.create(
            user=request.user,
            owner_name=request.POST.get('owner_name'),
            company_name=request.POST.get('company_name'),
            email=request.POST.get('email'),
            vat_number=request.POST.get('vat_number'),
        )
        referer = request.META.get('HTTP_REFERER', '/')   # Redirect to the page showing the billing info
        return redirect(referer)

    return render(request, 'billing.html')

# editing billing info
@login_required
def edit_billing_info(request):
    billing_info = get_object_or_404(BillingInfo, user=request.user)  # Ensure only existing info can be edited

    if request.method == 'POST':
        billing_info.owner_name = request.POST.get('owner_name')
        billing_info.company_name = request.POST.get('company_name')
        billing_info.email = request.POST.get('email')
        billing_info.vat_number = request.POST.get('vat_number')
        billing_info.save()
        referer = request.META.get('HTTP_REFERER', '/')   # Redirect to the page showing the billing info
        return redirect(referer)

    billing_info = BillingInfo.objects.get(user=request.user)
    return render(request, 'billing.html', {'billing_info': billing_info})

# deleting billing info
def delete_billing_info(request, billing_info_id):
    # Fetch the specific BillingInfo object using the ID
    billing_info = get_object_or_404(BillingInfo, id=billing_info_id, user=request.user)
    
    # Delete the billing info object
    billing_info.delete()
    
    # Redirect to a page (e.g., the billing info list page or dashboard)
    referer = request.META.get('HTTP_REFERER', '/')   # Redirect to the page showing the billing info
    return redirect(referer)


##################PROJECTS&TASKS###########################

# View to list all projects and Tasks for the logged-in user
@login_required
def view_project(request, user_id):

    user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(user=request.user).prefetch_related('tasks')
    return render(request, 'project_view.html', {'projects': projects})


################PROJECTS#############
# creating project for the logged-in user
@login_required
def create_project(request, user_id):
    # Ensure the user ID is valid and corresponds to a user
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_duration = request.POST.get('project_duration')
        num_tasks = request.POST.get('num_tasks')
        cost = request.POST.get('cost')

        # Save project to the database for the specified user
        Project.objects.create(
            user=user,  # Use the user from the URL
            name=project_name,
            duration=project_duration,
            num_tasks=num_tasks,
            cost=cost
        )
        return redirect('create_project', user_id=user_id)  # Redirect with user_id

    # Fetch projects for the specified user
    projects = Project.objects.filter(user=user)
    return render(request, 'project.html', {'projects': projects, 'user_id': user_id})


###############TASKS########################
# add tasks
@login_required
def add_task(request, user_id):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        task_name = request.POST.get('task_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        resources = request.POST.get('resources')
        dependencies = request.POST.get('dependencies')

        # Ensure the project exists for the logged-in user
        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            # Return an error or redirect to an error page if project does not exist
            return render(request, 'error.html', {'message': 'Project not found or does not belong to you.'})

        # Create and save the task
        Task.objects.create(
            project=project,
            name=task_name,
            start_date=start_date,
            end_date=end_date,
            resources_required=resources,
            dependencies=dependencies
        )

        return redirect('create_project', user_id=user_id)  # Redirect to project creation page

    # Fetch projects for the logged-in user to populate the dropdown
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project.html', {'projects': projects, 'user_id': user_id})



# Edit Task
def edit_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON body
        task = Task.objects.get(id=task_id)
        
        task.name = data.get('taskName')
        task.start_date = data.get('startDate')
        task.end_date = data.get('endDate')
        task.resources_required = data.get('resources')
        task.dependencies = data.get('dependencies')
        
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def delete_task(request, task_id):
    # Get the task to be deleted
    task = get_object_or_404(Task, id=task_id)
    
    # Get the referring URL (the page the user was on)
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Delete the task
    task.delete()
    
    # Redirect back to the referring page
    return redirect(referer)


##################MEMBER&RESOURCE##########################
# Viewing Team Member and Resource
@login_required
def manage(request, user_id):

    user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(user=request.user).prefetch_related('tasks')
    return render(request, 'resteam.html', {'projects': projects})


####################RESOURCES##############################
# Create Resource
@login_required
def add_resource(request, user_id):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        resource_name = request.POST.get('resource_name')
        provider = request.POST.get('provider')
        capacity = request.POST.get('capacity')
        location = request.POST.get('location')
        cost = request.POST.get('cost')

        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return render(request, 'error.html', {'message': 'Project not found or does not belong to you.'})

        Resource.objects.create(
            project=project,
            resource_name=resource_name,
            provider=provider,
            capacity=capacity,
            location=location,
            cost=cost
        )

        return redirect('add_resource', user_id=user_id)

    else:
        projects = Project.objects.filter(user=request.user)
        return render(request, 'resource.html', {'projects': projects, 'user_id': user_id})
    
# Delete Resource
@csrf_exempt
def delete_resource(request, resource_id):
    # Get the resource object or return 404 if not found
    resource = get_object_or_404(Resource, id=resource_id)

     # Get the referring URL (the page the user was on)
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Delete the resource
    resource.delete()
    
    # Redirect back to the referring page
    return redirect(referer)


# View for updating a resource
def edit_resource(request, resource_id):
    if request.method == 'POST':
        try:
            resource = get_object_or_404(Resource, id=resource_id)
            data = json.loads(request.body)
            
            resource.resource_name = data.get('resourceName')
            resource.provider = data.get('provider')
            resource.capacity = data.get('capacity')
            resource.location = data.get('location')
            resource.cost = data.get('resourceCost')
            resource.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    
############MEMBERS###########
# creating Team Member
@login_required
def add_team(request, user_id):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        member_name = request.POST.get('member_name')
        role = request.POST.get('role')
        additional_qualification = request.POST.get('additional_qualification', '')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return render(request, 'error.html', {'message': 'Project not found or does not belong to you.'})

        Team.objects.create(
            project=project,
            member_name=member_name,
            role=role,
            additional_qualification=additional_qualification,
            email=email,
            profile_picture=profile_picture
        )

        return redirect('add_resource', user_id=user_id)

    else:
        projects = Project.objects.filter(user=request.user)
        return render(request, 'resource.html', {'projects': projects, 'user_id': user_id})
    
# Viewing Team Member
def member_details(request, member_id):
    # Fetch member details
    member = get_object_or_404(Team, id=member_id)
    return JsonResponse({
        'name': member.member_name,
        'email': member.email,
        'role': member.role,
        'profile_picture': member.profile_picture.url,
    })

# Viewing Team Member
def project_team_members(request, project_id):
    # Fetch all team members for the given project
    project = get_object_or_404(Project, id=project_id)
    team_members = Team.objects.filter(project=project)
    members_data = [
        {
            'name': member.member_name,
            'email': member.email,
            'role': member.role,
            'profile_picture': member.profile_picture.url,
        }
        for member in team_members
    ]
    return JsonResponse({'team_members': members_data})

# Delete Team Member
@csrf_exempt
def delete_team_member(request, member_id):
    # Get the member object or return 404 if not found
    member = get_object_or_404(Team, id=member_id)

      # Get the referring URL (the page the user was on)
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Delete the member from the database
    member.delete()
    
     # Redirect back to the referring page
    return redirect(referer)

#  updating a team member
def edit_team_member(request, member_id):
    if request.method == 'POST':
        try:
            team_member = get_object_or_404(Team, id=member_id)
            data = json.loads(request.body)
            
            team_member.member_name = data.get('memberName')
            team_member.role = data.get('role')
            team_member.additional_qualification = data.get('qualification')
            team_member.email = data.get('email')
            team_member.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

#######################EMAILS####################################
# viewing emails on dashbaord
@login_required
def email_dashboard(request, user_id=None):
    # Use `user_id` if it's provided in the URL, otherwise use the logged-in user
    if user_id is None:
        user_id = request.user.id

    sent_emails = Email.objects.filter(sender_id=user_id, status=Email.SENT)
    scheduled_emails = Email.objects.filter(sender_id=user_id, status=Email.SCHEDULED)

    sent_emails_count = sent_emails.count()
    scheduled_emails_count = scheduled_emails.count()

    context = {
        'sent_emails': sent_emails,
        'scheduled_emails': scheduled_emails,
        'sent_emails_count': sent_emails_count,
        'scheduled_emails_count': scheduled_emails_count,
    }
    return render(request, 'emailing.html', context)

# Composing new Email
@login_required
def submit_email(request):
    if request.method == 'POST':
        sender = request.user
        receiver = request.POST.get('receiver')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        schedule_time = request.POST.get('schedule_time')

        # Determine if email is immediate or scheduled
        if schedule_time:
            scheduled_time = timezone.make_aware(timezone.datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M'))
            email = Email.objects.create(
                subject=subject,
                body=body,
                sender=sender,
                receiver=receiver,
                scheduled_time=scheduled_time,
                status=Email.SCHEDULED
            )
        else:
            email = Email.objects.create(
                subject=subject,
                body=body,
                sender=sender,
                receiver=receiver,
                sent_time=timezone.now(),
                status=Email.SENT
            )
        
         # Get the referring URL (the page the user was on)
        referer = request.META.get('HTTP_REFERER', '/')
        
        # Redirect back to the referring page
        return redirect(referer)

############PROFILE############





from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Project, Task
from datetime import date

def billings_demo(request, user_id):
    user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(user=user)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, id=project_id, user=user)

        tasks = project.tasks.all()
        all_tasks_completed = all(task.end_date <= date.today() for task in tasks) if tasks.exists() else False
        status = "Completed" if all_tasks_completed else "Ongoing"

        # Get the start date (start date of the first task) and end date (end date of the last task)
        start_date = tasks.order_by("start_date").first().start_date if tasks.exists() else None
        end_date = tasks.order_by("-end_date").first().end_date if tasks.exists() else None

        

        return JsonResponse({
            "status": status,
            "cost": project.cost,
            "start_date": start_date.strftime('%d.%m.%Y') if start_date else "N/A",
            "end_date": end_date.strftime('%d.%m.%Y') if end_date else "N/A",
            "name": project.name,
           
        })

    project_data = [
        {
            "id": project.id,
            "name": project.name,
        } for project in projects
    ]

    return render(request, 'template1.html', {
        'user': user,
        'projects': project_data
    })











############DEMO##############

from .models import Profile, Subscription, Project

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=request.user)
    subscription = Subscription.objects.filter(user=request.user).first()
    projects = Project.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile,
        'subscription': subscription,
        'projects': projects,
    })

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        referer = request.META.get('HTTP_REFERER', '/')
        
        # Redirect back to the referring page
        return redirect(referer)

@login_required
def update_bio(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.bio = request.POST.get('bio')
        profile.save()
        referer = request.META.get('HTTP_REFERER', '/')
        
        # Redirect back to the referring page
        return redirect(referer)


###########Subscription###########
def subscription_view(request):
    return render(request, 'subscription.html')


@login_required
def process_subscription_payment(request):
    if request.method == 'POST':
        # Retrieve subscription data from the form
        plan_name = request.POST.get('plan_name')
        price = request.POST.get('plan_price')
        period = request.POST.get('plan_period')
        payment_method = request.POST.get('payment_method')

        # Set expiry date based on the period
        expiry_date = request.POST.get('expiry_date')
        if not expiry_date:
            # Add logic for calculating expiry date if not provided
            expiry_date = datetime.today().date()

        # Retrieve payment details based on the payment method
        if payment_method == 'card':
            card_number = request.POST.get('card_number')
            card_cvv = request.POST.get('cvv')
            card_expiry_date = request.POST.get('expiry_date')
            mpesa_number = None
        else:
            mpesa_number = request.POST.get('mpesa_number')
            card_number = None
            card_cvv = None
            card_expiry_date = None

        # Save the subscription to the database
        subscription = Subscription.objects.create(
            user=request.user,
            plan_name=plan_name,
            price=price,
            period=period,
            expiry_date=expiry_date,
            payment_method=payment_method,
            payment_status='Pending',  # Set status to pending by default
            card_number=card_number,
            card_cvv=card_cvv,
            card_expiry_date=card_expiry_date,
            mpesa_number=mpesa_number,
        )

        # Redirect to a confirmation or success page
        return redirect(reverse('home_dashboard', args=[request.user.id]))  # Corrected to use request.user.id

    return redirect('subscription_page')  # In case of GET request


from django.core.mail import EmailMessage
from django.http import JsonResponse

def send_invite(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        attachments = request.FILES.getlist('attachment')

        # Prepare the email
        mail = EmailMessage(
            subject="Team Invitation",
            body=message,
            to=[email],
        )

        # Add attachments
        for file in attachments:
            mail.attach(file.name, file.read(), file.content_type)

        try:
            mail.send()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
