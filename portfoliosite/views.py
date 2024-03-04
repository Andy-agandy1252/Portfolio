from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import ReportForm, CustomUserCreationForm, UserProfileForm, UserProfileUpdateForm, GrantWorkerStatusForm, WorkerStatusForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Worker, Report
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

def index(request):
    context = {
        'title': 'Andrej - Backend Developer',
        'first_name': 'Andrej',
        'last_name': 'Agarin',
        'date_of_birth': '10.11.1990',
        'address': 'Celle Germany',
        'zip_code': '29223',
        'email': 'a.agarin1252@gmail.com',
        'phone': '+49152 1397 8994',
        'profession': 'Backend Developer',
        'about_me': '''A Backend Developer with experience in building and maintaining server-side web 
        applications. Skilled in databases, server logic, and APIs to ensure smooth application 
        functionality, and more...''',
        'about_me_2': '''Greetings! I'm Andrej Agarin, a passionate and dedicated individual with a keen 
        interest in the world of technology and creativity. As a programmer, I thrive on turning ideas 
        into innovative solutions, constantly seeking to expand my knowledge and skills in 
        the ever-evolving landscape.''',
        'resume_data': [
            {
                'year': '2022-2022',
                'degree': 'Basic PYTHON programming skills',
                'university': 'CodeAcademy',
                'short_description': 'Learned basic programming knowledge in PYTHON language',
                'image_number': 1  # Add the image_number for the left box
            },
            {
                'year': '2022-2023',
                'degree': 'Bachelor of Science in Software Engineering',
                'university': 'CodeAcademy',
                'short_description': 'Specialized in software engineering, with a focus on backend development.',
                'image_number': 2  # Add the image_number for the right box
            }
        ],
        'skills_data': {
            'Python': 90,
            'JavaScript': 65,
            'HTML': 85,
            'CSS': 80,
            'Django': 80,
            'Flask': 70,
            'SQL': 80,
            'RESTful APIs': 85,
            'Web Scraping': 85,
            'Machine Learning': 65,
            'Linux': 40,
            'Problem Solving': 85,
        }
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_from_user = request.POST.get('message')
        message = f'Name: {name}\nSubject: {subject}\nEmail: {email}\nMessage: {message_from_user}'
        recipient_email = settings.EMAIL_HOST_USER  # Use the recipient email from .env
        sender_email = email
        send_mail(subject, message, sender_email, [recipient_email])
        # Set a success message
        messages.success(request, '''Thanks for your message! I'll contact you as soon as possible.''')
        # Redirect to the same page to avoid form resubmission on page refresh
        return redirect('index')
    # Render the portfolio.html to show the specific content
    return render(request, 'portfolio.html', context)


def kourse_certificate(request, image_number):
    pdf_path = f"images/certificate_{image_number}.pdf"  # Adjust the path to your PDF files
    return render(request, 'kourse_certificate.html', {'image_path': pdf_path})


# ==========Project=============

def street_maintenance(request):
    user = request.user
    profile = None

    if user.is_authenticated:
        profile = user.userprofile

    # Query only reports with status "queued"
    reports = Report.objects.filter(Q(status='queued') | Q(status='in_progress'))

    # Add the 'url' attribute to each report object
    for report in reports:
        report.url = reverse('report_detail', args=[report.id])

    # Pass the 'reports' context to the template
    return render(request, 'street_maintenance.html', {'user': user, 'profile': profile, 'reports': reports})


# Admin Panel----------------


@user_passes_test(lambda u: u.is_superuser)
def street_maintenance_admin(request):
    user = request.user
    reports = Report.objects.all()
    workers = Worker.objects.all()

    # Calculate total reports
    total_reports = reports.count()

    # Calculate today's date
    today = timezone.now().date()

    # Filter reports created today
    today_reports = reports.filter(created_at__date=today)

    # Calculate counts for each issue type for today's reports
    today_garbage_reports_count = today_reports.filter(issue_type='garbage').count()
    today_graffiti_reports_count = today_reports.filter(issue_type='graffiti').count()
    today_other_reports_count = today_reports.filter(issue_type='other').count()

    # Get count of reports currently in progress
    in_progress_reports = reports.filter(status='in_progress')

    # Calculate counts for each issue type for reports in progress
    garbage_reports_count_in_progress = in_progress_reports.filter(issue_type='garbage').count()
    graffiti_reports_count_in_progress = in_progress_reports.filter(issue_type='graffiti').count()
    other_reports_count_in_progress = in_progress_reports.filter(issue_type='other').count()

    # Calculate counts for each status
    queued_reports_count = reports.filter(status='queued').count()
    in_progress_reports_count = reports.filter(status='in_progress').count()
    finished_reports_count = reports.filter(status='finished').count()

    # Calculate counts for each worker status
    available_workers_count = workers.filter(status='available').count()
    works_workers_count = workers.filter(status='works').count()
    sick_workers_count = workers.filter(status='sick').count()
    not_working_today_count = workers.filter(status='not_working_today').count()
    on_holiday_count = workers.filter(status='on_holiday').count()
    pending_count = workers.filter(status='pending').count()

    # Calculate counts for today's works, garbage, graffiti, and other reports
    today_works_count = AssignedReport.objects.filter(worker__status__in=['works', 'pending']).values('worker').distinct().count()

    context = {
        'user': user,
        'workers': workers,
        'total_reports': total_reports,
        'today_reports': today_reports.count(),
        'today_garbage_reports_count': today_garbage_reports_count,
        'today_graffiti_reports_count': today_graffiti_reports_count,
        'today_other_reports_count': today_other_reports_count,
        'garbage_reports_count_in_progress': garbage_reports_count_in_progress,
        'graffiti_reports_count_in_progress': graffiti_reports_count_in_progress,
        'other_reports_count_in_progress': other_reports_count_in_progress,
        'queued_reports_count': queued_reports_count,
        'in_progress_reports_count': in_progress_reports_count,
        'finished_reports_count': finished_reports_count,
        'available_workers_count': available_workers_count,
        'works_workers_count': works_workers_count,
        'sick_workers_count': sick_workers_count,
        'not_working_today_count': not_working_today_count,
        'on_holiday_count': on_holiday_count,
        'pending_count': pending_count,
        'today_works_count': today_works_count,
        'in_progress_reports': in_progress_reports,  # Add this line
    }
    return render(request, 'street_maintenance_admin.html', context)


@user_passes_test(lambda u: u.is_superuser)
def grant_worker_status(request):
    user_found = False
    is_worker = False
    button_text = "Grant Worker Status"  # Button text when user is not a worker
    if request.method == 'POST':
        form = GrantWorkerStatusForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                worker = Worker.objects.filter(user_profile=user.userprofile).first()
                if worker:
                    is_worker = True
                user_found = True
                if 'grant' in request.POST and not worker:  # Check if user is not already a worker
                    Worker.objects.create(user_profile=user.userprofile, is_worker=True)
                    messages.success(request, f"{username} has been granted worker status.")
                elif 'revoke' in request.POST and worker:  # Check if user is already a worker
                    # Transaction to ensure atomicity
                    with transaction.atomic():
                        # Retrieve the AssignedReport instances for the worker
                        assigned_reports = AssignedReport.objects.filter(worker=worker)
                        # Update the status of associated reports and then delete AssignedReport
                        for assigned_report in assigned_reports:
                            assigned_report.report.status = 'queued'  # Update the status as needed
                            assigned_report.report.save()  # Save the changes
                            assigned_report.delete()  # Delete the AssignedReport
                    messages.success(request, f"Worker status revoked for {username}.")
                else:
                    if worker:
                        messages.error(request, f"{username} is already a worker.")
                    else:
                        messages.error(request, f"{username} is not a worker.")
            except User.DoesNotExist:
                messages.error(request, f"User {username} not found.")
    else:
        form = GrantWorkerStatusForm()

    # Determine button text based on user being a worker or not
    if is_worker:
        button_text = "Revoke Worker Status"

    # Get the newest message
    newest_message = None
    for message in messages.get_messages(request):
        newest_message = message

    return render(request, 'grant_worker_status.html', {
        'form': form,
        'user_found': user_found,
        'is_worker': is_worker,
        'button_text': button_text,
        'newest_message': newest_message,
    })



@user_passes_test(lambda u: u.is_superuser)
def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})



@user_passes_test(lambda u: u.is_superuser)
def worker_assignments(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    city = worker.user_profile.city
    country = worker.user_profile.country

    # Fetch all unique cities from reports
    cities = Report.objects.order_by().values_list('city', flat=True).distinct()

    selected_city = request.GET.get('city')
    queued_reports = None  # Initialize queued_reports variable

    if selected_city:
        # Fetch queued reports for the selected city
        queued_reports = Report.objects.filter(city=selected_city, status='queued')

    context = {'worker': worker, 'city': city, 'country': country, 'cities': cities, 'selected_city': selected_city, 'queued_reports': queued_reports}
    return render(request, 'worker_assignments.html', context)


@user_passes_test(lambda u: u.is_superuser)
def save_selected_reports(request, worker_id):
    if request.method == 'POST':
        selected_report_ids = request.POST.getlist('selected_reports')
        worker = Worker.objects.get(id=worker_id)

        # Check if the worker already has 6 assigned reports
        if worker.assignedreport_set.count() + len(selected_report_ids) > 6:
            return HttpResponseBadRequest("Cannot assign more than 6 reports to a worker.")

        # Save the selected reports to the database
        for report_id in selected_report_ids:
            report = Report.objects.get(id=report_id)
            report.status = 'in_progress'
            report.save()

            assigned_report = AssignedReport(worker=worker, report=report)
            assigned_report.save()

        # Update worker status to 'pending'
        worker.status = 'pending'
        worker.save()

        # Redirect back to jobs page after saving reports
        return redirect('jobs')
    else:
        return HttpResponseBadRequest("Invalid request method")

@user_passes_test(lambda u: u.is_superuser)
def jobs(request):
    # Query workers with at least one report associated with them
    workers_with_reports = Worker.objects.filter(assignedreport__isnull=False).distinct()

    queued_reports = Report.objects.filter(status='queued')

    context = {
        'workers': workers_with_reports,
        'queued_reports': queued_reports,
    }

    return render(request, 'jobs.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_reports(request, worker_id):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        if report_id is not None:
            report = get_object_or_404(AssignedReport, id=report_id, worker_id=worker_id)
            # Get the corresponding report
            report_instance = report.report
            # Update the status of the report to "queued"
            report_instance.status = 'queued'
            report_instance.save()  # Save the changes to the database
            # Delete the report
            report.delete()

            # Redirect back to the same page
            return redirect(request.META.get('HTTP_REFERER', reverse('jobs')))
        else:
            return HttpResponse("Report ID not provided", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)

@user_passes_test(lambda u: u.is_superuser)
def update_job(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    cities = Report.objects.values_list('city', flat=True).distinct()
    selected_city = request.GET.get('city')

    if selected_city:
        queued_reports = Report.objects.filter(city=selected_city, status='queued')
    else:
        queued_reports = Report.objects.filter(status='queued')

    context = {
        'worker': worker,
        'queued_reports': queued_reports,
        'cities': cities,
        'selected_city': selected_city,
    }

    return render(request, 'update_job.html', context)

@user_passes_test(lambda u: u.is_superuser)
def worker_profile(request, worker_id):
    worker = Worker.objects.get(id=worker_id)
    if request.method == 'POST':
        form = WorkerStatusForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('worker_profile', worker_id=worker.id)
    else:
        form = WorkerStatusForm(instance=worker)
    return render(request, 'worker_profile.html', {'worker': worker, 'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_report_list(request):
    # Fetch all reports from the database
    all_reports = Report.objects.all()

    return render(request, 'admin_report_list.html', {'all_reports': all_reports})



# Worker Panel -----------
@login_required
def worker_panel(request):
    user = request.user
    user_profile = user.userprofile
    worker = user_profile.worker

    if request.method == 'POST':
        if worker.status == 'available':
            worker.status = 'sick'
            worker.save()
            return redirect('worker_panel')

    return render(request, 'street_maintenance_worker.html', {'user': user})



from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AssignedReport

@login_required
def worker_job(request):
    user = request.user
    profile = user.userprofile
    user_city = profile.city
    assigned_reports = AssignedReport.objects.filter(worker=profile.worker)
    assigned_reports_data = list(assigned_reports.values('report__coordinates',
                                                         'report__street',
                                                         'report__house_number',
                                                         'report__city',
                                                         'report__issue_type',
                                                         'report__country',
                                                         'report__status'))
    worker_job_list_url = reverse('worker_job_list')

    context = {
        'user': user,
        'profile': profile,
        'assigned_reports': assigned_reports,
        'user_city': user_city,
        'assigned_reports_data': assigned_reports_data,
        'worker_job_list_url': worker_job_list_url
    }
    return render(request, 'worker_job.html', context)




@login_required
def worker_job_list(request):
    # Assuming you have the worker object associated with the logged-in user
    worker = request.user.userprofile.worker

    # Change the worker's status to "works"
    worker.status = "works"
    worker.save()
    user = request.user
    profile = user.userprofile
    user_city = profile.city
    assigned_reports = AssignedReport.objects.filter(worker=profile.worker)

    # Check if all assigned reports have a status of "finished"
    all_reports_finished = assigned_reports.filter(report__status='finished').count() == assigned_reports.count()

    assigned_reports_data = list(assigned_reports.values('report__coordinates',
                                                         'report__street',
                                                         'report__house_number',
                                                         'report__city',
                                                         'report__issue_type',
                                                         'report__country',
                                                         'report__status'))
    worker_job_list_url = reverse('worker_job_list')

    context = {
        'user': user,
        'profile': profile,
        'assigned_reports': assigned_reports,
        'user_city': user_city,
        'assigned_reports_data': assigned_reports_data,
        'worker_job_list_url': worker_job_list_url,
        'all_reports_finished': all_reports_finished  # Pass the flag to the template
    }
    # Check if there are assigned reports
    if assigned_reports.exists():
        return render(request, 'worker_job_list.html', context)
    else:
        # Redirect to another page or display a message
        return HttpResponse("You have no assigned reports.")


@login_required
def mark_job_finished(request, report_id):
    if request.method == 'POST':
        # Get the assigned report object
        assigned_report = get_object_or_404(AssignedReport, id=report_id)
        # Update the report status to "finished"
        assigned_report.report.status = 'finished'
        assigned_report.report.save()
        # Redirect back to the worker job list
        return redirect('worker_job_list')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required
def mark_job_accomplished(request):
    if request.method == 'GET':
        # Assuming you have the worker object associated with the logged-in user
        worker = request.user.userprofile.worker

        # Change the worker status to "available"
        worker.status = 'available'
        worker.save()

        # Delete assigned reports
        AssignedReport.objects.filter(worker=worker).delete()

        # Redirect to street_maintenance_worker.html
        return redirect('worker_panel')
    else:
        return HttpResponseNotAllowed(['GET'])


# Register part  ---------
@csrf_protect
def register(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Check if the success message is not already in the session
            if not any(msg for msg in messages.get_messages(request) if "registered successfully" in msg.message):
                messages.info(request, f'User {user.username} registered successfully!')

            return redirect('login')
        else:
            messages.error(request, 'Invalid form data. Please check the form.')
    else:
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {'user_form': user_form, 'profile_form': profile_form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('street_maintenance_admin')  # Redirect superusers to the admin panel
            else:
                return redirect('street_maintenance')  # Redirect regular users to the main page
        else:
            # Handle invalid login attempt
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('street_maintenance')


@login_required
def create_report(request):
    issue_type = request.GET.get('issue_type')

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            # Extract and save coordinates
            coordinates_str = form.cleaned_data.get('coordinates')
            if coordinates_str:
                try:
                    # Split the coordinates into latitude and longitude
                    latitude, longitude = map(float, coordinates_str.split(','))
                    report.coordinates = f"{latitude},{longitude}"

                    # Set the user
                    report.user = request.user

                    # Extract and save issue_type
                    issue_type_str = form.cleaned_data.get('issue_type') or issue_type or 'other'
                    report.issue_type = issue_type_str

                    # Additional processing or validation if needed
                    report.save()
                    return redirect('create_report')  # Redirect to create_report.html
                except ValueError as e:
                    # Print the error for debugging
                    print(f"Error processing coordinates: {e}")
                    # Handle invalid coordinates format
                    return HttpResponseBadRequest("Invalid coordinates format.")
            else:
                # Handle case where 'coordinates' is None
                return HttpResponseBadRequest("Coordinates are required.")
        else:
            # Print form errors for debugging
            print(form.errors)
            # Handle form validation errors
            return HttpResponseBadRequest("Form is not valid.")
    else:
        form = ReportForm(initial={'issue_type': issue_type})  # Pass issue_type as initial value
    return render(request, 'create_report.html', {'form': form, 'selected_option': issue_type})

def report_list(request):
    user = request.user
    profile = None

    if user.is_authenticated:
        profile = user.userprofile

    reports = Report.objects.filter(Q(status='queued') | Q(status='in_progress'))
    # Add the 'url' attribute to each report object
    for report in reports:
        report.url = reverse('report_detail', args=[report.id])

    return render(request, 'report_list.html', {'user': user, 'profile': profile, 'reports': reports})


def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'report_detail.html', {'report': report})


@login_required
def user_report_list(request):
    user = request.user
    profile = None
    user_reports = []

    if user.is_authenticated:
        profile = user.userprofile
        # Filter reports by user ID and status "queued" or "in_progress"
        user_reports = Report.objects.filter(user=user, status__in=['queued', 'in_progress'])

    return render(request, 'user_report_list.html', {'user': user, 'profile': profile, 'user_reports': user_reports})




@login_required
def update_user_report(request, report_id, action=None):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            # Set the issue_type in the form
            issue_type_str = form.cleaned_data.get('issue_type')
            form.instance.issue_type = issue_type_str

            # Save the form and report
            form.save()

            # Redirect after update
            if action == 'delete':
                return redirect('user_report_list')  # Redirect to user_report_list after delete
            else:
                return redirect('user_report_list')  # Redirect to user_report_list after update
    else:
        form = ReportForm(instance=report)

    return render(request, 'update_user_report.html', {'form': form, 'report': report})




@login_required
def delete_user_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        report.delete()
        if request.user.is_staff:  # Check if the user is an admin
            return redirect('admin_report_list')  # Redirect to admin_report_list if admin
        else:
            return redirect('user_report_list')  # Redirect to user_report_list for non-admin users
    return render(request, 'delete_user_report.html', {'report': report})


@login_required
def user_report_details(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'user_report_details.html', {'report': report})


@login_required
def user_profile(request):
    user = request.user
    profile = user.userprofile

    return render(request, 'user_profile.html', {'user': user, 'profile': profile})


@login_required
def user_profile_update(request):
    user = request.user
    profile = user.userprofile
    initial_data = {
        'username': user.username,
        'email': user.email,
        'city': profile.city,
        'zipcode': profile.zipcode,
        'country': profile.country,
    }

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

            form.save()  # Save the UserProfile instance

            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
        else:
            # Handle invalid form data
            messages.error(request, 'Invalid form data. Please check the form.')

            # If you want to display errors next to specific fields, you can add them to the context
            return render(request, 'user_profile_update.html', {'user': user, 'profile': profile, 'form': form})
    else:
        form = UserProfileUpdateForm(initial=initial_data)

    return render(request, 'user_profile_update.html', {'user': user, 'profile': profile, 'form': form})