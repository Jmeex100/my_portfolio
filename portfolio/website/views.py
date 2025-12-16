import os
import mimetypes

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.contrib import messages

from .models import Project, Skill, ContactMessage, Document
from .forms import ContactForm


# ==========================
# CONTACT COOLDOWN API
# ==========================

@require_GET
def cooldown_status(request):
    email = request.GET.get('email', '').strip()
    ip_address = request.META.get('REMOTE_ADDR')

    if email:
        remaining = ContactMessage.get_cooldown_remaining(email)
        if remaining > 0:
            return JsonResponse({'can_submit': False, 'remaining': remaining})

    if ip_address:
        remaining_ip = ContactMessage.get_cooldown_remaining_by_ip(ip_address)
        if remaining_ip > 0:
            return JsonResponse({'can_submit': False, 'remaining': remaining_ip})

    return JsonResponse({'can_submit': True, 'remaining': 0})


# ==========================
# HOME PAGE
# ==========================
def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm(request=request)  # fresh form after success
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm(request=request)

    projects = Project.objects.all().order_by('-created_at')
    skills = Skill.objects.all().order_by('category', '-proficiency')
    
    # FIXED: Use Document model to get the latest CV
    latest_cv = Document.objects.filter(doc_type='CV', is_public=True).order_by('-uploaded_at').first()

    context = {
        'projects': projects,
        'skills': skills,
        'form': form,
        'latest_cv': latest_cv,
    }
    return render(request, 'index.html', context)

# ==========================
# VIEW DOCUMENT INLINE (PDF)
# ==========================

def view_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, is_public=True)

    file_path = document.file.path

    if not os.path.exists(file_path):
        messages.error(request, 'File not found.')
        return redirect('home')

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/pdf'

    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response


# ==========================
# DOWNLOAD DOCUMENT
# ==========================

def download_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id, is_public=True)

    file_path = document.file.path

    if not os.path.exists(file_path):
        messages.error(request, 'File not found.')
        return redirect('home')

    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'

    filename = os.path.basename(file_path)

    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Content-Length'] = os.path.getsize(file_path)

    return response
