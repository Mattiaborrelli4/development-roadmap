// Script.js per il server HTTP C++

console.log('🚀 HTTP Server C++ - Client-side JavaScript');
console.log('✨ Pagina caricata con successo!');

// Aggiunge interattività alle card
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(1.05)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });

    // Mostra timestamp
    const now = new Date();
    console.log(`📅 Data e ora: ${now.toLocaleString('it-IT')}`);

    // Test fetch API
    fetch('/index.html')
        .then(response => {
            console.log('✅ Fetch test successful - Status:', response.status);
            return response.text();
        })
        .then(data => {
            console.log('📄 Response length:', data.length, 'bytes');
        })
        .catch(error => {
            console.error('❌ Fetch test failed:', error);
        });

    // Aggiungi animazione alle sezioni
    const sections = document.querySelectorAll('section');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});

// Test performance
window.addEventListener('load', function() {
    const perfData = performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`⚡ Page load time: ${pageLoadTime}ms`);
});
