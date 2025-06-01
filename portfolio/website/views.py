from django.shortcuts import render
from .models import Project, Skill
from .forms import ContactForm
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    projects = Project.objects.all().order_by('-created_at')
    skills = Skill.objects.all().order_by('category', '-proficiency')  # Group by category, descending proficiency

    context = {
        'projects': projects,
        'skills': skills,
        'form': form,
    }
    return render(request, 'index.html', context)
