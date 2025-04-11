document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('fileInput');
    const processingSection = document.querySelector('.processing-section');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            showError('Please upload an image file');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            showError('File size must be less than 10MB');
            return;
        }

        document.querySelector('.upload-card').classList.add('d-none');
        processingSection.classList.remove('d-none');

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                window.location.href = '/result';
            } else {
                showError('Analysis failed. Please try again.');
            }
        }).catch(() => {
            showError('Network error. Please check your connection.');
        });
    }

    function showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container-fluid').prepend(alert);
    }
});

// static/js/main.js'e eklemeler
// Intersection Observer ile scroll animasyonları
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('slide-in');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

// Image Comparison Slider
function initImageSlider() {
    const slider = document.querySelector('.image-comparison');
    if (!slider) return;

    const sliderHandle = document.createElement('div');
    sliderHandle.className = 'slider-handle floating';
    sliderHandle.innerHTML = '<i class="fas fa-arrows-left-right"></i>';
    slider.appendChild(sliderHandle);

    let isDragging = false;
    const moveSlider = (e) => {
        const rect = slider.getBoundingClientRect();
        const x = (e.clientX || e.touches[0].clientX) - rect.left;
        const percentage = (x / rect.width) * 100;
        
        slider.style.setProperty('--slider-pos', `${Math.max(0, Math.min(100, percentage))}%`);
        sliderHandle.style.left = `calc(${percentage}% - 25px)`;
    };

    sliderHandle.addEventListener('mousedown', () => isDragging = true);
    document.addEventListener('mousemove', (e) => {
        if (isDragging) moveSlider(e);
    });
    document.addEventListener('mouseup', () => isDragging = false);

    // Touch events
    sliderHandle.addEventListener('touchstart', () => isDragging = true);
    document.addEventListener('touchmove', (e) => {
        if (isDragging) moveSlider(e);
    });
    document.addEventListener('touchend', () => isDragging = false);
}

// Progress Bar Animation
function animateProgressBar() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.getAttribute('aria-valuenow');
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = `${targetWidth}%`;
        }, 300);
    });
}

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', () => {
    initImageSlider();
    animateProgressBar();
});