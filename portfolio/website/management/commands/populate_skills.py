from django.core.management.base import BaseCommand
from website.models import Skill

class Command(BaseCommand):
    help = 'Populate the database with predefined skills'

    def handle(self, *args, **options):
        # Mapping of icon classes to categories
        icon_to_category = {
            'fab fa-python': 'Backend',
            'fas fa-leaf': 'Backend',  # Django
            'fab fa-html5': 'Frontend',
            'fab fa-css3-alt': 'Frontend',
            'fab fa-js': 'Frontend',
            'fab fa-react': 'Frontend',
            'fab fa-node-js': 'Backend',
            'fas fa-database': 'Database',
            'fab fa-aws': 'Cloud',
            'fab fa-git-alt': 'DevOps',
            'fab fa-docker': 'DevOps',
            'fas fa-network-wired': 'DevOps',  # Kubernetes
            'fab fa-linux': 'DevOps',
            'fas fa-wind': 'Frontend',  # TailwindCSS
            'fab fa-bootstrap': 'Frontend',
            'fab fa-vuejs': 'Frontend',
            'fab fa-angular': 'Frontend',
            'fab fa-js-square': 'Frontend',  # TypeScript
            'fas fa-project-diagram': 'Backend',  # GraphQL
            'fab fa-php': 'Backend',
            'fab fa-laravel': 'Backend',
            'fab fa-java': 'Backend',
            'fas fa-code': 'Backend',  # C#
            'fas fa-seedling': 'Backend',  # Spring
            'fas fa-gamepad': 'Game Development',  # Unity
            'fab fa-adobe': 'Design',
        }

        # Define proficiency levels based on skill level
        proficiency_levels = {
            'fab fa-python': 75,  # Intermediate
            'fas fa-leaf': 75,  # Django - Intermediate
            'fab fa-html5': 70,  # Intermediate
            'fab fa-css3-alt': 70,  # Intermediate
            'fab fa-js': 70,  # Intermediate
            'fab fa-react': 70,  # Intermediate
            'fab fa-node-js': 70,  # Intermediate
            'fas fa-database': 70,  # Intermediate
            'fab fa-aws': 50,  # Basic
            'fab fa-git-alt': 75,  # Intermediate
            'fab fa-docker': 60,  # Basic to intermediate
            'fas fa-network-wired': 50,  # Kubernetes - Basic
            'fab fa-linux': 70,  # Intermediate
            'fas fa-wind': 70,  # TailwindCSS - Intermediate
            'fab fa-bootstrap': 70,  # Intermediate
            'fab fa-vuejs': 50,  # Basic
            'fab fa-angular': 50,  # Basic
            'fab fa-js-square': 70,  # TypeScript - Intermediate
            'fas fa-project-diagram': 50,  # GraphQL - Basic
            'fab fa-php': 50,  # Basic
            'fab fa-laravel': 50,  # Basic
            'fab fa-java': 50,  # Basic
            'fas fa-code': 50,  # C# - Basic
            'fas fa-seedling': 50,  # Spring - Basic
            'fas fa-gamepad': 50,  # Unity - Basic (games basic)
            'fab fa-adobe': 70,  # Intermediate
        }

        for icon_class, display_name in Skill.ICON_CHOICES:
            category = icon_to_category.get(icon_class, 'other skils')
            proficiency = proficiency_levels.get(icon_class, 60)  # Default to 60 if not specified
            skill, created = Skill.objects.get_or_create(
                name=display_name,
                defaults={
                    'category': category,
                    'icon': icon_class,
                    'proficiency': proficiency
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {display_name} with proficiency {proficiency}%'))
            else:
                # Update existing skill if proficiency differs
                if skill.proficiency != proficiency:
                    skill.proficiency = proficiency
                    skill.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated skill: {display_name} to proficiency {proficiency}%'))
                else:
                    self.stdout.write(f'Skill already exists: {display_name}')

        # Create additional skills
        for skill_info in additional_skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_info['name'],
                defaults={
                    'category': skill_info['category'],
                    'icon': skill_info['icon'],
                    'proficiency': skill_info['proficiency']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {skill_info["name"]} with proficiency {skill_info["proficiency"]}%'))
            else:
                if skill.proficiency != skill_info['proficiency']:
                    skill.proficiency = skill_info['proficiency']
                    skill.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated skill: {skill_info["name"]} to proficiency {skill_info["proficiency"]}%'))
                else:
                    self.stdout.write(f'Skill already exists: {skill_info["name"]}')