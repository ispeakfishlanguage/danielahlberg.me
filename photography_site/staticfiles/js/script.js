document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.querySelector('.lightbox-content');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxCaption = document.querySelector('.lightbox-caption');
    const contactForm = document.querySelector('.contact-form');

    // Initialize Rellax for parallax effects
    if (typeof Rellax !== 'undefined') {
        try {
            var rellax = new Rellax('.rellax', {
                speed: -7,
                center: false,
                wrapper: null,
                round: true,
                vertical: true,
                horizontal: false
            });

            console.log('Rellax initialized successfully');
        } catch (error) {
            console.warn('Rellax initialization failed:', error);
        }
    }

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only prevent default for anchor links
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();

                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');

                const targetId = href;
                const targetSection = document.querySelector(targetId);

                if (targetSection) {
                    const navbarHeight = navbar.offsetHeight;
                    const targetPosition = targetSection.offsetTop - navbarHeight;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }

                // Close Bootstrap navbar on mobile
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            }
        });
    });

    // Navbar scroll effect with color-on-scroll
    window.addEventListener('scroll', function() {
        const colorOnScrollValue = navbar.getAttribute('color-on-scroll');
        const scrollThreshold = colorOnScrollValue ? parseInt(colorOnScrollValue) : 100;

        if (window.scrollY > scrollThreshold) {
            navbar.classList.add('scrolled');
            navbar.classList.remove('navbar-transparent');
        } else {
            navbar.classList.remove('scrolled');
            navbar.classList.add('navbar-transparent');
        }

        // Update active navigation link for same-page navigation
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.scrollY + 150;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    if (href && href.startsWith('#')) {
                        link.classList.remove('active');
                        if (href === `#${sectionId}`) {
                            link.classList.add('active');
                        }
                    }
                });
            }
        });
    });

    // Portfolio filtering
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');

            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            galleryItems.forEach(item => {
                item.classList.add('hidden');
                item.classList.remove('fade-in');

                setTimeout(() => {
                    if (filter === 'all' || item.getAttribute('data-category') === filter) {
                        item.classList.remove('hidden');
                        item.classList.add('fade-in');
                    }
                }, 300);
            });
        });
    });

    // Lightbox functionality for both modern and legacy galleries
    const allGalleryItems = document.querySelectorAll('.gallery-item, .gallery-item-modern');

    allGalleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('.gallery-image, .gallery-image-modern');
            if (!img) return;

            const fullImage = img.getAttribute('data-full-image') || img.src;
            const title = img.getAttribute('data-title');
            const description = img.getAttribute('data-description');

            if (lightboxImg) {
                lightboxImg.src = fullImage;
                lightboxImg.alt = title || img.alt;
            }

            if (lightboxCaption) {
                let captionHtml = '';
                if (title) captionHtml += `<h3>${title}</h3>`;
                if (description) captionHtml += `<p>${description}</p>`;
                lightboxCaption.innerHTML = captionHtml;
            }

            if (lightbox) {
                lightbox.style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
        });
    });

    function closeLightbox() {
        if (lightbox) {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    if (lightboxClose) {
        lightboxClose.addEventListener('click', closeLightbox);
    }

    if (lightbox) {
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && lightbox && lightbox.style.display === 'block') {
            closeLightbox();
        }
    });

    // Contact form handling
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Sending...';
                submitBtn.disabled = true;

                // Re-enable button after form submission (Django will handle the redirect)
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    }

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add scroll animations to elements
    const animateElements = document.querySelectorAll('.gallery-item, .row');
    animateElements.forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });

    // Initial gallery animation
    galleryItems.forEach(item => {
        item.classList.add('fade-in');
    });
});