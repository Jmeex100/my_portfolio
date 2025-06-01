from django.db import models
from django.core.validators import URLValidator

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

from django.db import models

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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"