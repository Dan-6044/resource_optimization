# context_processors.py

from datetime import datetime, timedelta
from .models import Task, Project

def task_notifications(request):
    if not request.user.is_authenticated:
        return {'notifications': []}  # Return empty if the user is not authenticated

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Get the projects that the user is associated with
    user_projects = Project.objects.filter(user=request.user)

    if not user_projects.exists():
        return {'notifications': []}  # Return empty if no projects are associated with the user

    # Get tasks related to those projects and filter by end_date within today or tomorrow
    tasks = Task.objects.filter(project__in=user_projects, end_date__range=[today, tomorrow])

    # Prepare notifications based on the filtered tasks
    notifications = []
    for task in tasks:
        notifications.append({
            'message': f"Task '{task.name}' in project '{task.project.name}' will end in 1 day.",
            'time': task.end_date,
            'type': 'task',
        })

    return {'notifications': notifications}
