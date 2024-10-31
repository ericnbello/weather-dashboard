/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        dongle: ['Dongle', 'sans-serif']
      },
      backgroundImage: {
        'day': "url('/images/day.jpeg')",
        'night': "url('/images/night.jpeg')"
      }
    },
  },
  plugins: [],
}
