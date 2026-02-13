// Markdown Editor - Applicazione principale
// Utilizza moderne feature JavaScript ES6+

class MarkdownEditor {
    constructor() {
        // Elementi DOM
        this.input = document.getElementById('markdownInput');
        this.preview = document.getElementById('preview');
        this.exportBtn = document.getElementById('exportBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.saveStatus = document.getElementById('saveStatus');

        // Chiave LocalStorage
        this.storageKey = 'markdown-editor-content';

        // Inizializza l'editor
        this.init();
    }

    // Inizializzazione
    init = () => {
        this.loadFromStorage();
        this.attachEventListeners();
        this.updatePreview();
    }

    // Allega gli event listeners
    attachEventListeners = () => {
        // Input event per anteprima live
        this.input.addEventListener('input', () => {
            this.updatePreview();
            this.saveToStorage();
        });

        // Export HTML
        this.exportBtn.addEventListener('click', () => {
            this.exportHTML();
        });

        // Cancella contenuto
        this.clearBtn.addEventListener('click', () => {
            this.clearContent();
        });
    }

    // Aggiorna l'anteprima
    updatePreview = () => {
        const markdownText = this.input.value;
        const htmlContent = this.parseMarkdown(markdownText);
        this.preview.innerHTML = htmlContent;
    }

    // Parser Markdown principale
    parseMarkdown = (text) => {
        if (!text) return '<p style="color: var(--text-secondary);">Inizia a scrivere per vedere l\'anteprima...</p>';

        let html = text;

        // Escape HTML per sicurezza
        html = this.escapeHTML(html);

        // Code blocks (```code```)
        html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

        // Inline code (`code`)
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Headers (###, ##, #)
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // Bold (**text**)
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Italic (*text*)
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

        // Unordered lists (- item)
        html = this.parseLists(html);

        // Links ([text](url))
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Paragraphs (double newline)
        html = this.parseParagraphs(html);

        return html;
    }

    // Parser per liste
    parseLists = (html) => {
        const lines = html.split('\n');
        let result = [];
        let inList = false;
        let listItems = [];

        for (let line of lines) {
            // Check se è un item di lista
            if (line.trim().startsWith('- ')) {
                const content = line.replace(/^(\s*)- (.*)/, '$2');
                const indent = line.match(/^(\s*)/)[0].length;

                if (!inList) {
                    inList = true;
                    listItems = [];
                }

                listItems.push({ content, indent });
            } else {
                // Chiudi la lista se aperta
                if (inList) {
                    result.push(this.buildList(listItems));
                    inList = false;
                    listItems = [];
                }
                result.push(line);
            }
        }

        // Chiudi lista alla fine
        if (inList) {
            result.push(this.buildList(listItems));
        }

        return result.join('\n');
    }

    // Costruisci HTML lista
    buildList = (items) => {
        let html = '<ul>';
        let currentIndent = 0;

        items.forEach((item, index) => {
            if (item.indent > currentIndent) {
                html += '<ul>';
                currentIndent = item.indent;
            } else if (item.indent < currentIndent) {
                html += '</ul>';
                currentIndent = item.indent;
            }
            html += `<li>${item.content}</li>`;
        });

        // Chiudi tutti i ul aperti
        html += '</ul>';
        return html;
    }

    // Parser per paragrafi
    parseParagraphs = (html) => {
        const lines = html.split('\n');
        let result = [];
        let inParagraph = false;

        for (let line of lines) {
            // Salta linee vuote
            if (line.trim() === '') {
                if (inParagraph) {
                    result.push('</p>');
                    inParagraph = false;
                }
                continue;
            }

            // Salta linee che sono già HTML tags
            if (line.trim().startsWith('<')) {
                if (inParagraph) {
                    result.push('</p>');
                    inParagraph = false;
                }
                result.push(line);
                continue;
            }

            // Inizia paragrafo
            if (!inParagraph) {
                result.push('<p>');
                inParagraph = true;
            }

            result.push(line);
        }

        if (inParagraph) {
            result.push('</p>');
        }

        return result.join('\n');
    }

    // Escape HTML per sicurezza
    escapeHTML = (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Salva in LocalStorage
    saveToStorage = () => {
        this.saveStatus.textContent = 'Salvataggio...';
        this.saveStatus.classList.add('saving');

        try {
            localStorage.setItem(this.storageKey, this.input.value);

            // Feedback visivo
            setTimeout(() => {
                this.saveStatus.textContent = 'Salvato';
                this.saveStatus.classList.remove('saving');
            }, 500);
        } catch (error) {
            console.error('Errore salvataggio:', error);
            this.saveStatus.textContent = 'Errore salvataggio';
        }
    }

    // Carica da LocalStorage
    loadFromStorage = () => {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) {
                this.input.value = saved;
            }
        } catch (error) {
            console.error('Errore caricamento:', error);
        }
    }

    // Esporta come HTML
    exportHTML = () => {
        const markdownText = this.input.value;
        const htmlContent = this.parseMarkdown(markdownText);

        // Crea documento HTML completo
        const fullHTML = `<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Export</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
            line-height: 1.6;
            color: #333;
        }
        h1, h2, h3 { margin-top: 2rem; }
        h1 { color: #2563eb; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }
        h2 { color: #4f46e5; }
        h3 { color: #7c3aed; }
        code { background: #f3f4f6; padding: 0.2rem 0.5rem; border-radius: 4px; }
        pre { background: #1e293b; color: #f1f5f9; padding: 1rem; border-radius: 8px; overflow-x: auto; }
        pre code { background: transparent; color: inherit; }
        ul, ol { margin-left: 2rem; }
        li { margin-bottom: 0.5rem; }
        strong { color: #2563eb; }
        em { color: #dc2626; }
    </style>
</head>
<body>
${htmlContent}
</body>
</html>`;

        // Crea blob e scarica
        const blob = new Blob([fullHTML], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.href = url;
        a.download = `markdown-export-${Date.now()}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    // Cancella contenuto
    clearContent = () => {
        if (confirm('Sei sicuro di voler cancellare tutto? Questa azione non può essere annullata.')) {
            this.input.value = '';
            this.updatePreview();
            localStorage.removeItem(this.storageKey);
            this.saveStatus.textContent = 'Cancellato';
        }
    }
}

// Inizializza l'applicazione quando il DOM è pronto
document.addEventListener('DOMContentLoaded', () => {
    new MarkdownEditor();
});
