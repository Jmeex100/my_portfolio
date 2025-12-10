import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.contrib import messages

from .models import Project, Skill, ContactMessage, CV
from .forms import ContactForm


@require_GET
def cooldown_status(request):
    """API endpoint to check cooldown status for contact form"""
    email = request.GET.get('email', '').strip()
    ip_address = request.META.get('REMOTE_ADDR')

    # Check cooldown by email
    if email:
        remaining = ContactMessage.get_cooldown_remaining(email)
        if remaining > 0:
            return JsonResponse({'can_submit': False, 'remaining': remaining})

    # Check cooldown by IP (optional fallback)
    if ip_address:
        remaining_ip = ContactMessage.get_cooldown_remaining_by_ip(ip_address)
        if remaining_ip > 0:
            return JsonResponse({'can_submit': False, 'remaining': remaining_ip})

    return JsonResponse({'can_submit': True, 'remaining': 0})


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm(request=request)  # fresh form after success
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm(request=request)

    projects = Project.objects.all().order_by('-created_at')
    skills = Skill.objects.all().order_by('category', '-proficiency')
    
    # Get latest CV safely
    latest_cv = CV.objects.order_by('-uploaded_at').first()

    context = {
        'projects': projects,
        'skills': skills,
        'form': form,
        'cooldown_minutes': 2,
        'latest_cv': latest_cv,
    }
    return render(request, 'index.html', context)

def view_cv(request):
    """
    Serve the CV inline inside the iframe (prevents auto-download)
    """
    try:
        cv = CV.objects.order_by('-uploaded_at').first()

        if not cv or not cv.file:
            messages.error(request, 'No CV uploaded yet.')
            return redirect('home')

        file_path = cv.file.path

        if not os.path.exists(file_path):
            messages.error(request, 'CV file not found.')
            return redirect('home')

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/pdf'

        # INLINE instead of attachment = no auto-download
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = 'inline; filename="cv.pdf"'
        return response

    except Exception as e:
        print("Error displaying CV:", e)
        messages.error(request, 'Could not load CV.')
        return redirect('home')

def download_cv(request):
    """
    View to download the latest CV file - FIXED to prevent auto-download and handle filename correctly
    """
    try:
        cv = CV.objects.order_by('-uploaded_at').first()

        if not cv or not cv.file:
            messages.error(request, 'No CV uploaded yet.')
            return redirect('home')

        file_path = cv.file.path

        if not os.path.exists(file_path):
            messages.error(request, 'CV file not found on the server.')
            return redirect('home')

        # Determine correct MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        # FIXED: Extract clean filename from media path (e.g., 'Richman-Mushanga-FlowCV-Resume-blue_1.pdf')
        clean_filename = os.path.basename(cv.file.name)  # Gets just the filename without /cv/ prefix

        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{clean_filename}"'
        response['Content-Length'] = os.path.getsize(file_path)

        return response

    except Exception as e:
        print(f"Error downloading CV: {e}")  # For debugging
        messages.error(request, 'An error occurred while downloading the CV. Please try again.')
        return redirect('home')