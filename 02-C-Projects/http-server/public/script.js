// Server HTTP in C - Script JavaScript

console.log('Server HTTP in C - JavaScript caricato con successo!');

// Mostra un messaggio di benvenuto quando la pagina è caricata
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pagina completamente caricata');

    // Aggiungi un timestamp nel footer
    const footer = document.querySelector('footer');
    if (footer) {
        const timestamp = new Date().toLocaleString('it-IT');
        const timeElement = document.createElement('p');
        timeElement.textContent = `Ultimo accesso: ${timestamp}`;
        timeElement.style.marginTop = '10px';
        timeElement.style.fontSize = '0.8rem';
        footer.appendChild(timeElement);
    }

    // Aggiungi animazione alle card
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            this.style.color = 'white';
            const h3 = this.querySelector('h3');
            const p = this.querySelector('p');
            if (h3) h3.style.color = 'white';
            if (p) p.style.color = 'rgba(255,255,255,0.9)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
            this.style.color = '';
            const h3 = this.querySelector('h3');
            const p = this.querySelector('p');
            if (h3) h3.style.color = '';
            if (p) p.style.color = '';
        });
    });

    // Mostra informazioni di connessione
    console.log('========================================');
    console.log('Server HTTP in C');
    console.log('========================================');
    console.log('Protocollo: HTTP/1.1');
    console.log('Linguaggio: C');
    console.log('Threading: Multi-threaded');
    console.log('Socket: TCP/IP');
    console.log('========================================');
});

// Test delle performance
window.addEventListener('load', function() {
    const perfData = performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`Tempo di caricamento pagina: ${pageLoadTime}ms`);
});

// Funzione per testare le richieste AJAX (opzionale)
function testAjaxRequest() {
    console.log('Test richiesta AJAX al server...');

    fetch('/test.html')
        .then(response => {
            console.log('Status:', response.status);
            console.log('Status Text:', response.statusText);
            console.log('Content-Type:', response.headers.get('Content-Type'));
            return response.text();
        })
        .then(data => {
            console.log('Risposta ricevuta, lunghezza:', data.length);
        })
        .catch(error => {
            console.error('Errore:', error);
        });
}

// Esporiamo la funzione globalmente per testing
window.testAjaxRequest = testAjaxRequest;
