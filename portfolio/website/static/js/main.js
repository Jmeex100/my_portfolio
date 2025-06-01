document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const themeIcon = themeToggle.querySelector('i');

    // Apply system preference or saved theme
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        htmlElement.classList.add('dark');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    themeToggle.addEventListener('click', () => {
        htmlElement.classList.toggle('dark');
        if (htmlElement.classList.contains('dark')) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
});
// Skill bars animation - improved version
const animateSkillBars = () => {
    const skillBars = document.querySelectorAll('.skill-bar');
    
    skillBars.forEach(bar => {
        const rect = bar.getBoundingClientRect();
        // Check if element is in viewport
        if (rect.top < window.innerHeight && rect.bottom >= 0) {
            const width = bar.getAttribute('data-width');
            bar.style.width = width;
            bar.style.transition = 'width 1.5s ease-in-out'; // Smooth animation
        }
    });
};

// Run on initial load
document.addEventListener('DOMContentLoaded', animateSkillBars);

// Run on scroll
window.addEventListener('scroll', animateSkillBars);