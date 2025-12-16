from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# ==========================
# FILE VALIDATORS
# ==========================

def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')


def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError('File size must be under 5MB.')


# ==========================
# PROJECT MODEL
# ==========================

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    url = models.TextField(validators=[URLValidator()], blank=True, null=True)
    github_url = models.TextField(validators=[URLValidator()], blank=True, null=True)
    technologies = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ==========================
# SKILL MODEL
# ==========================

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('DevOps', 'DevOps'),
        ('Design', 'Design'),
        ('Mobile', 'Mobile'),
        ('Cloud', 'Cloud'),
        ('Data Science', 'Data Science'),
        ('Game Development', 'Game Development'),
        ('Other', 'Other'),
    ]

    ICON_CHOICES = [
        ('fab fa-python', 'Python'),
        ('fas fa-leaf', 'Django'),
        ('fab fa-html5', 'HTML5'),
        ('fab fa-css3-alt', 'CSS3'),
        ('fab fa-js', 'JavaScript'),
        ('fab fa-react', 'React'),
        ('fab fa-node-js', 'Node.js'),
        ('fas fa-database', 'MySQL / PostgreSQL'),
        ('fab fa-aws', 'AWS'),
        ('fab fa-git-alt', 'Git'),
        ('fab fa-docker', 'Docker'),
        ('fab fa-linux', 'Linux'),
    ]

    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name


# ==========================
# DOCUMENT MODEL (CV, CERTS)
# ==========================

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('CV', 'Curriculum Vitae'),
        ('CERT', 'Certificate'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=150)
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='documents/',
        validators=[validate_pdf, validate_file_size]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


# ==========================
# CONTACT MESSAGE MODEL
# ==========================

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}"
