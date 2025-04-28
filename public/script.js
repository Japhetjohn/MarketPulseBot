
// - Animations, mobile menu, tabs, icons, back-to-top, accessibility
document.addEventListener('DOMContentLoaded', function () {
    // Lucide icons
    if (window.lucide) lucide.createIcons();

    // Set current year in footer
    var yearEl = document.getElementById('current-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // Tabs functionality (supports multiple tab groups)
    document.querySelectorAll('.tabs, .example-tabs').forEach(function (tabsContainer) {
        var triggers = tabsContainer.querySelectorAll('.tab-trigger');
        var contents = tabsContainer.querySelectorAll('.tab-content');
        triggers.forEach(function (trigger) {
            trigger.addEventListener('click', function () {
                var tabId = trigger.getAttribute('data-tab');
                triggers.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));
                trigger.classList.add('active');
                var tabContent = tabsContainer.querySelector('#' + tabId);
                if (tabContent) tabContent.classList.add('active');
            });
        });
    });

    // Mobile menu toggle
    var menuBtn = document.querySelector('.mobile-menu-btn');
    var mobileMenu = document.querySelector('.mobile-menu');
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('show');
            if (mobileMenu.classList.contains('show')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
        // Close mobile menu when clicking a link
        mobileMenu.querySelectorAll('.mobile-link').forEach(function (link) {
            link.addEventListener('click', function () {
                mobileMenu.classList.remove('show');
                document.body.style.overflow = '';
            });
        });
    }

    // Animate cards on scroll (fade/slide in)
    var animatedEls = document.querySelectorAll('.card, .rounded-lg');
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    animatedEls.forEach(function (el) {
        el.classList.add('pre-animate');
        observer.observe(el);
    });

    // Back to top button
    var backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', function () {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });
        backToTopButton.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
