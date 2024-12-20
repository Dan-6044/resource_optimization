from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('pricing/', views.pricing, name='pricing'),
    path('signup_new/', views.signup_new, name='signup_new'),
    path('focus_on/', views.focus_on, name='focus_on'),
    path('signin/', views.signin, name='signin'),
    path('what_brings_you_here_today/', views.what_brings_you_here_today, name='what_brings_you_here_today'),
    path('how-many-people-work-at-your-company/', views.how_many_people_work_at_your_company, name='how_many_people_work_at_your_company'),
    path('select_what_youd_like_to_manage/', views.select_what_youd_like_to_manage, name='select_what_youd_like_to_manage'),

    path('home_dashboard/<int:user_id>/', views.home_dashboard, name='home_dashboard'),
    path('my_work/<int:user_id>/', views.my_work, name='my_work'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('emailing/<int:user_id>/', views.email_dashboard, name='emailing'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),
    path('billings/<int:user_id>/', views.billings, name='billings'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
      
    
    path('create_project/<int:user_id>/', views.create_project, name='create_project'),
    path('project_view/<int:user_id>/', views.view_project, name='sample'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('add_task/<int:user_id>/', views.add_task, name='add_task'),

    path('manage/<int:user_id>/', views.manage, name='manage'),
    path('add_resource/<int:user_id>/', views.add_resource, name='add_resource'),
    path('add_team/<int:user_id>/', views.add_team, name='add_team'),
    path('api/member/<int:member_id>/', views.member_details, name='member-details'),
    path('api/project/<int:project_id>/team/', views.project_team_members, name='project-team-members'),
    path('resources/delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    path('team-members/delete/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('edit-resource/<int:resource_id>/', views.edit_resource, name='edit_resource'),
    path('edit-team-member/<int:member_id>/', views.edit_team_member, name='edit_team_member'),

   path('submit_email/', views.submit_email, name='submit_email'),

   path('billings_demo/<int:user_id>/', views.billings_demo, name='billing'),
   path('payment-methods/', views.payment_methods_view, name='payment_methods'),
   path('edit-payment-method/<int:payment_method_id>/', views.edit_payment_method, name='edit_payment_method'),
   path('delete-payment-method/<int:payment_method_id>/', views.delete_payment_method, name='delete_payment_method'),
   path('create-invoice/', views.create_invoice, name='create_invoice'),
   path('add_billing_info/', views.add_billing_info, name='add_billing_info'),
   path('edit_billing_info/', views.edit_billing_info, name='edit_billing_info'),
   path('delete-billing-info/<int:billing_info_id>/', views.delete_billing_info, name='delete_billing_info'),

   path('subscription/', views.subscription_view, name='subscription'),
    path('process-subscription-payment/', views.process_subscription_payment, name='process_subscription_payment'),

   path('logout/', views.custom_logout, name='logout'),
    path('update-profile-picture/', views.update_profile_picture, name='update-profile-picture'),
    path('update-bio/', views.update_bio, name='update-bio'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
