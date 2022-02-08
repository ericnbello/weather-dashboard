module.exports = {
    content: ['../templates/**/*.{html,js}'],
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                dongle: ['Dongle']
            },
            colors: {
                primary: '#715AFF',
                dark: '#131112',
                cornflowerblue: '#5887FF',
                mayaBlue: '#55C1FF',
                prussianBlue: '#102E4A',
                midPurple: '#A682FF',
                bitterSweet: '#FF715B',
            },
            backgroundImage: {
                'main': 'url(/static/images/weather-bg.jpg)',
            },
        },
    },
    plugins: [],
}