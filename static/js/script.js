document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav-menu');
    const searchBar = document.getElementById('search-bar');
    const emptySearch = document.querySelector('.empty-search');

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
        if (themeToggle) {
            themeToggle.textContent = 'Светлая тема';
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark');
            themeToggle.textContent = document.body.classList.contains('dark') ? 'Светлая тема' : 'Тёмная тема';

            if (document.body.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.removeItem('theme');
            }
        });
    }

    if (searchBar) {
        searchBar.addEventListener('input', (event) => {
            const search = event.target.value.trim().toLowerCase();
            let visibleCount = 0;

            document.querySelectorAll('.tools-grid .tool-tile').forEach((tile) => {
                const haystack = (tile.dataset.toolName || tile.textContent).toLowerCase();
                const isVisible = haystack.includes(search);
                tile.hidden = !isVisible;
                if (isVisible) {
                    visibleCount += 1;
                }
            });

            if (emptySearch) {
                emptySearch.hidden = visibleCount > 0;
            }

            document.querySelectorAll('.tool-category-group').forEach((group) => {
                const hasVisibleTool = Array.from(group.querySelectorAll('.tool-tile')).some((tile) => !tile.hidden);
                group.hidden = !hasVisibleTool;
            });
        });
    }

    if (menuToggle && nav) {
        menuToggle.addEventListener('click', () => {
            const isOpen = nav.classList.toggle('active');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });
    }
});
