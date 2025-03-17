// Применение темы при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
        document.getElementById('theme-toggle').textContent = 'Светлая тема';
    }
});

// Переключение темы
document.getElementById('theme-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const btn = document.getElementById('theme-toggle');
    btn.textContent = document.body.classList.contains('dark') ? 'Светлая тема' : 'Тёмная тема';
    // Сохранение темы в localStorage
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.removeItem('theme');
    }
});

// Поиск по инструментам
document.getElementById('search-bar').addEventListener('input', (e) => {
    const search = e.target.value.toLowerCase();
    document.querySelectorAll('.tool-tile').forEach(tile => {
        const name = tile.querySelector('h2').textContent.toLowerCase();
        tile.style.display = name.includes(search) ? 'block' : 'none';
    });
});

// Бургер-меню
document.querySelector('.menu-toggle').addEventListener('click', () => {
    const nav = document.querySelector('.nav-menu');
    nav.classList.toggle('active');
});