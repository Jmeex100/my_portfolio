# models.py
from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

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


class Skill(models.Model):
    # Define choices
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
        ('fas fa-network-wired', 'Kubernetes'),
        ('fab fa-linux', 'Linux'),
        ('fas fa-wind', 'TailwindCSS'),
        ('fab fa-bootstrap', 'Bootstrap'),
        ('fab fa-vuejs', 'Vue.js'),
        ('fab fa-angular', 'Angular'),
        ('fab fa-js-square', 'TypeScript'),
        ('fas fa-project-diagram', 'GraphQL'),
        ('fab fa-php', 'PHP'),
        ('fab fa-laravel', 'Laravel'),
        ('fab fa-java', 'Java'),
        ('fas fa-code', 'C#'),
        ('fas fa-seedling', 'Spring'),
        ('fas fa-gamepad', 'Unity'),
        ('fab fa-adobe', 'Photoshop / Illustrator'),
    ]

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
        ('other skils', 'other skils'),
    ]

    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50)  # percentage
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name


class CV(models.Model):
    file = models.FileField(upload_to='cv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV uploaded on {self.uploaded_at}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True, editable=False)
    user_agent = models.TextField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Add a unique constraint for additional protection
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"Message from {self.name}"

    def clean(self):
        """
        Custom validation to prevent rapid submissions
        """
        super().clean()
        
        # Check if this is a new message (not updating existing)
        if not self.pk:
            # Check for recent submissions from same email (2 minutes cooldown)
            five_minutes_ago = timezone.now() - timedelta(minutes=2)
            recent_by_email = ContactMessage.objects.filter(
                email=self.email,
                created_at__gte=five_minutes_ago
            )
            
            if recent_by_email.exists():
                raise ValidationError(
                    'Please wait at least 5 minutes before sending another message.'
                )
            
            # Optional: Also check by IP address (if available)
            if self.ip_address:
                recent_by_ip = ContactMessage.objects.filter(
                    ip_address=self.ip_address,
                    created_at__gte=five_minutes_ago
                )
                
                if recent_by_ip.exists():
                    raise ValidationError(
                        'Please wait at least 5 minutes before sending another message.'
                    )

    def can_send_message(self, email=None, ip_address=None):
        """
        Helper method to check if a message can be sent
        """
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        
        # Check by email
        if email:
            recent_by_email = ContactMessage.objects.filter(
                email=email,
                created_at__gte=five_minutes_ago
            )
            if recent_by_email.exists():
                return False, "Please wait 5 minutes before sending another message."
        
        # Check by IP (optional)
        if ip_address:
            recent_by_ip = ContactMessage.objects.filter(
                ip_address=ip_address,
                created_at__gte=five_minutes_ago
            )
            if recent_by_ip.exists():
                return False, "Please wait 5 minutes before sending another message."
        
        return True, ""

    @classmethod
    def get_cooldown_remaining(cls, email):
        """
        Get remaining cooldown time in seconds for an email
        """
        try:
            last_message = cls.objects.filter(email=email).latest('created_at')
            cooldown_end = last_message.created_at + timedelta(minutes=2)
            now = timezone.now()

            if now < cooldown_end:
                return (cooldown_end - now).total_seconds()
        except cls.DoesNotExist:
            pass

        return 0

    @classmethod
    def get_cooldown_remaining_by_ip(cls, ip_address):
        """
        Get remaining cooldown time in seconds for an IP address
        """
        try:
            last_message = cls.objects.filter(ip_address=ip_address).latest('created_at')
            cooldown_end = last_message.created_at + timedelta(minutes=5)
            now = timezone.now()
            
            if now < cooldown_end:
                return (cooldown_end - now).total_seconds()
        except cls.DoesNotExist:
            pass
        
        return 0

    def save(self, *args, **kwargs):
        """
        Custom save to ensure validation runs
        """
        self.full_clean()
        super().save(*args, **kwargs)