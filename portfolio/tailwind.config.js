/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
        './website/templates/**/*.html',  // Website app templates
    './website/static/js/**/*.js',    // Website app JS file
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
// tailwind.config.js