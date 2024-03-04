from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('kourse_certificate/<int:image_number>/', views.kourse_certificate, name='kourse_certificate'),
    path('street_maintenance/', views.street_maintenance, name='street_maintenance'),
    path('street_maintenance/register/', views.register, name='register'),
    path('street_maintenance/login/', views.login_view, name='login'),
    path('street_maintenance_admin/', views.street_maintenance_admin, name='street_maintenance_admin'),
    path('street_maintenance_admin/grant-or-revoke-worker-status/', views.grant_worker_status, name='grant_worker_status'),  # Updated URL
    path('street_maintenance_admin/worker-list/', views.worker_list, name='worker_list'),
    path('street_maintenance_admin/admin-report-list/', views.admin_report_list, name='admin_report_list'),
    path('street_maintenance_admin/jobs/', views.jobs, name='jobs'),


path('street_maintenance_admin/worker-assignments/<int:worker_id>/', views.worker_assignments, name='worker_assignments'),
path('delete-reports/<int:worker_id>/', views.delete_reports, name='delete_reports'),
path('street_maintenance_admin/jobs/update-job/<int:worker_id>/', views.update_job, name='update_job'),

    path('street_maintenance_admin/save_reports_to_job/<int:worker_id>/', views.save_selected_reports, name='save_selected_reports'),
    path('street_maintenance_admin/worker_profile/<int:worker_id>/', views.worker_profile, name='worker_profile'),
    path('street_maintenance_worker/', views.worker_panel, name='worker_panel'),


path('street_maintenance_worker/worker_job/', views.worker_job, name='worker_job'),
path('street_maintenance_worker/worker-job-list/', views.worker_job_list, name='worker_job_list'),
path('mark_job_finished/<int:report_id>/', views.mark_job_finished, name='mark_job_finished'),
path('mark_job_accomplished/', views.mark_job_accomplished, name='mark_job_accomplished'),
    path('street_maintenance/logout/', views.logout_view, name='logout'),
    path('street_maintenance/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('street_maintenance/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('street_maintenance/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('street_maintenance/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('street_maintenance/create_report/', views.create_report, name='create_report'),
    path('street_maintenance/report_list/', views.report_list, name='report_list'),
    path('street_maintenance/report_detail/<int:report_id>/', views.report_detail, name='report_detail'),
    path('street_maintenance/user_reports/', views.user_report_list, name='user_report_list'),
    path('street_maintenance/update_user_report/<int:report_id>/', views.update_user_report, name='update_user_report'),
    path('street_maintenance/delete_user_report/<int:report_id>/', views.delete_user_report, name='delete_user_report'),
    path('street_maintenance/user_report_details/<int:report_id>/', views.user_report_details, name='user_report_details'),
    path('street_maintenance/user_profile/', views.user_profile, name='user_profile'),
    path('street_maintenance/user_profile_update/', views.user_profile_update, name='user_profile_update'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
