/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        '../../**/models.py',
    ],
    theme: {
      extend: {
        fontFamily: {
          // This links the utility 'font-brand' to your custom font
          'brand': ['ClientBrand', 'sans-serif'],
          'ict': ['ITBrand', 'sans-serif'],
          'tab': ['Tabs', 'sans-serif'],
        },
        colors: {
            'agile-blue': '#3b82f6', // Ensure your brand blue is still defined
            'agile-green':'#24b81f',
            'agile-grey': '#6c6363',
        },
      },
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
    ],
}