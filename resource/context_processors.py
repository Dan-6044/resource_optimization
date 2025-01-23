from datetime import datetime, timedelta
from .models import Task, Project, Subscription

def task_notifications(request):
    if not request.user.is_authenticated:
        return {'notifications': []}  # Return empty if the user is not authenticated

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Get the projects that the user is associated with
    user_projects = Project.objects.filter(user=request.user)

    # Prepare task notifications
    task_notifications = []
    if user_projects.exists():
        # Get tasks related to those projects and filter by end_date within today or tomorrow
        tasks = Task.objects.filter(project__in=user_projects, end_date__range=[today, tomorrow])
        for task in tasks:
            task_notifications.append({
                'message': f"Task '{task.name}' in project '{task.project.name}' will end in 1 day.",
                'time': task.end_date,
                'type': 'task',
            })

    # Prepare subscription notifications
    subscription_notifications = []
    subscriptions = Subscription.objects.filter(user=request.user, period__gte=today)
    for subscription in subscriptions:
        days_remaining = (subscription.period - today).days
        if days_remaining <= 5:
            if days_remaining == 1:
                message = f"Your subscription '{subscription.plan_name}' will expire tomorrow."
            elif days_remaining == 0:
                message = f"Your subscription '{subscription.plan_name}' expires today."
            else:
                message = f"Your subscription '{subscription.plan_name}' will expire in {days_remaining} days."

            subscription_notifications.append({
                'message': message,
                'time': subscription.period,
                'type': 'subscription',
            })

    # Combine all notifications
    notifications = task_notifications + subscription_notifications

    return {'notifications': notifications}
