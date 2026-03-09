/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fff8ed',
          100: '#ffeccc',
          200: '#ffd699',
          300: '#ffbf66',
          400: '#ffab33',
          DEFAULT: '#FF9500',
          500: '#FF9500',
          600: '#e08500',
          700: '#b86d00',
          800: '#8f5500',
          900: '#663d00',
          light: '#ffab33',
          dark: '#e08500',
        },
        secondary: {
          50: '#e6faf8',
          100: '#b3f0ea',
          200: '#80e6dc',
          300: '#4ddbce',
          400: '#1ad1c0',
          DEFAULT: '#00BEAE',
          500: '#00BEAE',
          600: '#00a89a',
          700: '#008f83',
          800: '#00756c',
          900: '#005c55',
          light: '#1ad1c0',
          dark: '#00a89a',
        },
        accent: {
          50: '#fff8ed',
          100: '#ffefd4',
          400: '#f5b74a',
          DEFAULT: '#F4A261',
          500: '#F4A261',
          600: '#e08832',
        },
        dark: {
          DEFAULT: '#353C3B',
          500: '#353C3B',
          600: '#2a302f',
          700: '#1f2423',
        },
        light: {
          DEFAULT: '#F8F9F9',
          500: '#F8F9F9',
        },
        muted: '#4D5756',
      },
      fontFamily: {
        cairo: ['Cairo', 'Tajawal', 'sans-serif'],
        arabic: ['Tajawal', 'Cairo', 'sans-serif'],
        sora: ['Sora', 'sans-serif'],
        english: ['Inter', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
