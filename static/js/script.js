
document.querySelectorAll('.modal').forEach(modal => {

    modal.addEventListener('shown.bs.modal', () => {
        const iframe = modal.querySelector('.carousel-item.active iframe[data-video-id]')
        if (iframe) {
            iframe.src = `https://www.youtube.com/embed/${iframe.dataset.videoId}?autoplay=0`
        }
    })

    modal.addEventListener('hidden.bs.modal', () => {
        modal.querySelectorAll('iframe').forEach(iframe => iframe.src = '')
    })

    modal.querySelectorAll('.carousel').forEach(carousel => {

        carousel.addEventListener('slide.bs.carousel', () => {
            carousel.querySelectorAll('iframe').forEach(iframe => iframe.src = '')
        })

        carousel.addEventListener('slid.bs.carousel', () => {
            const iframe = carousel.querySelector('.carousel-item.active iframe[data-video-id]')
            if (iframe) {
                iframe.src = `https://www.youtube.com/embed/${iframe.dataset.videoId}?autoplay=0`
            }
        })

    })
})

document.querySelectorAll('.modal').forEach(modal => {

    modal.addEventListener('shown.bs.modal', () => {
        const carouselEl = modal.querySelector('.carousel')
        if (!carouselEl) return

        // Get or create carousel instance
        let carousel = bootstrap.Carousel.getInstance(carouselEl)
        if (!carousel) {
            carousel = new bootstrap.Carousel(carouselEl, {
                interval: false,
                ride: false
            })
        }

        // Reset to first slide
        carousel.to(0)

        // Start video if first slide is a video
        const iframe = carouselEl.querySelector(
            '.carousel-item.active iframe[data-video-id]'
        )
        if (iframe) {
            iframe.src =
                `https://www.youtube.com/embed/${iframe.dataset.videoId}?autoplay=1`
        }
    })

    modal.addEventListener('hidden.bs.modal', () => {
        // Stop all videos
        modal.querySelectorAll('iframe').forEach(iframe => {
            iframe.src = ''
        })
    })

})

        const sections = document.querySelectorAll(".fixed-section");
        const backgrounds = document.querySelectorAll(".fixed-bg");

        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const index = [...sections].indexOf(entry.target);

                        backgrounds.forEach(bg => bg.classList.remove("active"));
                        backgrounds[index]?.classList.add("active");
                    }
                });
            },
            { threshold: 0.6 }
        );
        sections.forEach(section => observer.observe(section));