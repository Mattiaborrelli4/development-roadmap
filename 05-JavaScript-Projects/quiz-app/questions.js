// ===== Question Data Structure =====
// Categories: javascript, html, css, general

const categories = [
    {
        id: 'javascript',
        name: 'JavaScript',
        icon: 'fab fa-js',
        color: '#f7df1e',
        description: 'DOM, ES6+, Funzioni, Oggetti'
    },
    {
        id: 'html',
        name: 'HTML',
        icon: 'fab fa-html5',
        color: '#e34f26',
        description: 'Struttura, Semantica, Form'
    },
    {
        id: 'css',
        name: 'CSS',
        icon: 'fab fa-css3-alt',
        color: '#1572b6',
        description: 'Layout, Flexbox, Grid, Animazioni'
    },
    {
        id: 'general',
        name: 'Generale',
        icon: 'fas fa-code',
        color: '#6366f1',
        description: 'Web Development, Best Practices'
    }
];

// Question database
const questionsDB = {
    javascript: [
        {
            question: 'Qual è il risultato di typeof null in JavaScript?',
            answers: ['null', 'undefined', 'object', 'number'],
            correct: 2,
            difficulty: 'easy',
            explanation: 'In JavaScript, typeof null restituisce "object". Questo è un bug storico del linguaggio.'
        },
        {
            question: 'Qual è la differenza tra == e ===?',
            answers: [
                'Non c\'è differenza',
                '== controlla solo il valore, === controlla valore e tipo',
                '=== è più veloce di ==',
                '== è più veloce di ==='
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: '=== è l\'operatore di uguaglianza stretta che confronta sia il valore che il tipo, mentre == fa coercizione di tipo.'
        },
        {
            question: 'Cosa restituisce Array.isArray([])?',
            answers: ['true', 'false', 'undefined', 'null'],
            correct: 0,
            difficulty: 'easy',
            explanation: 'Array.isArray([]) restituisce true perché [] è un array vuoto.'
        },
        {
            question: 'Qual è il risultato di [1, 2, 3] + [4, 5, 6]?',
            answers: ['[1, 2, 3, 4, 5, 6]', '[1, 2, 34, 5, 6]', '"1,2,34,5,6"', 'TypeError'],
            correct: 2,
            difficulty: 'medium',
            explanation: 'Quando si usano l\'operatore + con array, questi vengono convertiti in stringhe e concatenati.'
        },
        {
            question: 'Cosa fa il metodo Array.map()?',
            answers: [
                'Filtra gli elementi di un array',
                'Riduce un array a un singolo valore',
                'Crea un nuovo array trasformando ogni elemento',
                'Ordina gli elementi di un array'
            ],
            correct: 2,
            difficulty: 'easy',
            explanation: 'Array.map() crea un nuovo array applicando una funzione a ogni elemento dell\'array originale.'
        },
        {
            question: 'Qual è la differenza tra var, let e const?',
            answers: [
                'Non ci sono differenze',
                'var è scoped alla funzione, let e const sono scoped al blocco',
                'let e const non possono essere ridefiniti',
                'Solo const è immutabile'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'var ha function scope, mentre let e const hanno block scope. const non può essere riassegnato.'
        },
        {
            question: 'Cosa restituisce Promise.all([])?',
            answers: ['Promise che risolve immediatamente con []', 'Promise che rifiuta', 'undefined', 'Errore'],
            correct: 0,
            difficulty: 'hard',
            explanation: 'Promise.all([]) restituisce una Promise che viene risolta immediatamente con un array vuoto.'
        },
        {
            question: 'Qual è il risultato di 2 + "2"?',
            answers: ['4', '"22"', 'NaN', 'TypeError'],
            correct: 1,
            difficulty: 'easy',
            explanation: 'JavaScript converte il numero in stringa e concatena: "2" + "2" = "22".'
        },
        {
            question: 'Cosa fa l\'operatore spread (...)?',
            answers: [
                'Espande un iterabile in elementi singoli',
                'Comprime un array in un singolo elemento',
                'Crea una copia profonda di un oggetto',
                'Elimina elementi da un array'
            ],
            correct: 0,
            difficulty: 'medium',
            explanation: 'L\'operatore spread espande un iterabile (come un array) in elementi singoli dove sono previsti più argomenti.'
        },
        {
            question: 'Qual è il risultato di !!null?',
            answers: ['null', 'true', 'false', 'undefined'],
            correct: 2,
            difficulty: 'medium',
            explanation: '!! converte il valore in un booleano. !!null è false perché null è falsy.'
        },
        {
            question: 'Cosa restituisce setTimeout(() => {}, 0)?',
            answers: ['undefined', '0', 'Un ID del timer', 'null'],
            correct: 2,
            difficulty: 'medium',
            explanation: 'setTimeout restituisce un ID del timer che può essere usato con clearTimeout().'
        },
        {
            question: 'Qual è la differenza tra call() e apply()?',
            answers: [
                'Non ci sono differenze',
                'call accetta argomenti separati, apply accetta un array',
                'apply è più veloce',
                'call è deprecato'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'Entrambi invocano una funzione con un this specifico, ma call() accetta argomenti separati, apply() un array.'
        },
        {
            question: 'Cosa fa il destructuring in JavaScript?',
            answers: [
                'Distrugge gli oggetti',
                'Estrae proprietà da oggetti o elementi da array',
                'Crea copie profonde',
                'Elimina variabili'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'Il destructuring permette di estrarre proprietà da oggetti o elementi da array in variabili distinte.'
        },
        {
            question: 'Qual è il risultato di [1, 2, 3].findIndex(x => x === 2)?',
            answers: ['2', '1', 'true', 'undefined'],
            correct: 1,
            difficulty: 'easy',
            explanation: 'findIndex restituisce l\'indice del primo elemento che soddisfa la condizione, quindi 1.'
        },
        {
            question: 'Cosa succede con "use strict"?',
            answers: [
                'Il codice gira più velocemente',
                'Abilita la modalità Strict che impone regole più severe',
                'Disabilita il console.log',
                'Rende il codice obsoleto'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: '"use strict" abilita la modalità Strict che cattura errori comuni e impone regole di scrittura più sicure.'
        }
    ],
    html: [
        {
            question: 'Qual è lo scopo del tag <meta> in HTML?',
            answers: [
                'Definire meta-dati sulla pagina',
                'Creare metafore',
                'Definire lo stile della pagina',
                'Includere script esterni'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'Il tag <meta> fornisce meta-informazioni sulla pagina HTML come charset, descrizione, keywords, ecc.'
        },
        {
            question: 'Qual è la differenza tra <div> e <span>?',
            answers: [
                'Non ci sono differenze',
                '<div> è inline, <span> è block',
                '<div> è block, <span> è inline',
                '<span> non si può usare con CSS'
            ],
            correct: 2,
            difficulty: 'easy',
            explanation: '<div> è un elemento block-level, mentre <span> è inline per piccole porzioni di testo.'
        },
        {
            question: 'Cosa fa l\'attributo "required" in un form?',
            answers: [
                'Rende il form obbligatorio',
                'Rende il campo obbligatorio prima del submit',
                'Rende il campo readonly',
                'Rende il form disabled'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'L\'attributo "required" indica che il campo deve essere compilato prima di inviare il form.'
        },
        {
            question: 'Qual è il tag HTML5 corretto per la navigazione?',
            answers: ['<navigation>', '<nav>', '<menu>', '<navbar>'],
            correct: 1,
            difficulty: 'easy',
            explanation: '<nav> è il tag semantico HTML5 per definire sezioni di navigazione.'
        },
        {
            question: 'A cosa serve l\'attributo "alt" nelle immagini?',
            answers: [
                'A definire l\'allineamento',
                'A fornire un testo alternativo',
                'A definire l\'animazione',
                'A rendere l\'image responsive'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'L\'attributo "alt" fornisce un testo alternativo per le immagini, importante per l\'accessibilità.'
        },
        {
            question: 'Qual è il tag corretto per creare un hyperlink?',
            answers: ['<link>', '<a>', '<href>', '<url>'],
            correct: 1,
            difficulty: 'easy',
            explanation: '<a> (anchor) è il tag usato per creare collegamenti ipertestuali con l\'attributo href.'
        },
        {
            question: 'Cosa definisce l\'attributo "data-*"?',
            answers: [
                'Dati per il database',
                'Dati custom privati per la pagina',
                'Data di creazione',
                'Data di modifica'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'Gli attributi data-* permettono di memorizzare informazioni custom private nella pagina.'
        },
        {
            question: 'Qual è la differenza tra id e class?',
            answers: [
                'Non ci sono differenze',
                'id è unico, class può essere ripetuta',
                'class è unica, id può essere ripetuto',
                'id non si può usare con CSS'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'Un id deve essere unico nel documento, mentre una class può essere applicata a più elementi.'
        },
        {
            question: 'Cosa fa il tag <canvas>?',
            answers: [
                'Crea un layout canvas',
                'Fornisce un area per disegnare grafica con JavaScript',
                'Crea una tela per immagini',
                'Definisce un contenitore responsive'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: '<canvas> fornisce un area bitmap dove disegnare grafica dinamicamente con JavaScript.'
        },
        {
            question: 'Qual è lo scopo dell\'elemento <section>?',
            answers: [
                'Creare sezioni di codice',
                'Definire una sezione tematica di un documento',
                'Dividere la pagina in colonne',
                'Creare separatori orizzontali'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: '<section> rappresenta una sezione generica di un documento con un tema comune.'
        },
        {
            question: 'Cosa fa l\'attributo "autocomplete"?',
            answers: [
                'Compila automaticamente il form',
                'Indica se il browser deve completare automaticamente i campi',
                'Crea suggerimenti automatici',
                'Valida il form automaticamente'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'L\'attributo autocomplete indica se il browser deve riempire automaticamente i campi del form.'
        },
        {
            question: 'Qual è il tag per creare una lista ordinata?',
            answers: ['<ul>', '<ol>', '<li>', '<list>'],
            correct: 1,
            difficulty: 'easy',
            explanation: '<ol> (ordered list) crea una lista numerata, mentre <ul> crea una lista non ordinata.'
        },
        {
            question: 'A cosa serve l\'attributo "placeholder"?',
            answers: [
                'A definire il valore del campo',
                'A mostrare un suggerimento temporaneo nel campo',
                'A validare il campo',
                'A rendere il campo readonly'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'placeholder mostra un suggerimento che scompare quando l\'utente inizia a digitare.'
        },
        {
            question: 'Qual è la differenza tra <script> in head e body?',
            answers: [
                'Non ci sono differenze',
                'Nel body è caricato prima, nell\'head dopo',
                'Nel head blocca il rendering, nel body no',
                'Nel body non funziona'
            ],
            correct: 2,
            difficulty: 'medium',
            explanation: 'Gli script nell\'head bloccano il rendering della pagina fino al caricamento.'
        },
        {
            question: 'Cosa fa l\'attributo "charset"?',
            answers: [
                'Definisce la dimensione dei caratteri',
                'Specifica la codifica dei caratteri del documento',
                'Definisce il font da usare',
                'Crea caratteri speciali'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'L\'attributo charset specifica la codifica dei caratteri, solitamente UTF-8.'
        }
    ],
    css: [
        {
            question: 'Qual è la differenza tra padding e margin?',
            answers: [
                'Non ci sono differenze',
                'Padding è esterno, margin è interno',
                'Padding è interno, margin è esterno',
                'Entrambi sono interni'
            ],
            correct: 2,
            difficulty: 'easy',
            explanation: 'Padding è lo spazio interno tra il contenuto e il bordo, margin è lo spazio esterno tra elementi.'
        },
        {
            question: 'Cosa fa la proprietà "display: flex"?',
            answers: [
                'Rende l\'elemento flessibile',
                'Attiva il flexbox layout',
                'Rende l\'elemento invisibile',
                'Crea una griglia'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'display: flex attiva il Flexbox layout per il contenitore e i suoi figli diretti.'
        },
        {
            question: 'Qual è la differenza tra position: relative e absolute?',
            answers: [
                'Non ci sono differenze',
                'Relative è rispetto al documento, absolute al parent',
                'Relative è rispetto alla posizione normale, absolute al parent positioned',
                'Absolute non funziona'
            ],
            correct: 2,
            difficulty: 'medium',
            explanation: 'Relative posiziona rispetto alla sua posizione normale. Absolute rispetto al parent più vicino con positioning.'
        },
        {
            question: 'Cosa fa la proprietà "z-index"?',
            answers: [
                'Definisce la larghezza',
                'Controlla l\'ordine di sovrapposizione degli elementi',
                'Definisce l\'altezza',
                'Crea zoom'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'z-index controlla l\'ordine di sovrapposizione degli elementi positioned sullo stack.'
        },
        {
            question: 'Qual è l\'unità "rem" in CSS?',
            answers: [
                'Percentuale relativa al body',
                'Dimensione relativa alla radice (root)',
                'Pixel relativi',
                'Em dimensione'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'rem è relativo al font-size dell\'elemento radice (html), solitamente 16px di default.'
        },
        {
            question: 'Cosa fa "box-sizing: border-box"?',
            answers: [
                'Include padding e border nella width/height',
                'Esclude padding e border dalla width/height',
                'Crea un box',
                'Rende il box responsive'
            ],
            correct: 0,
            difficulty: 'medium',
            explanation: 'border-box include padding e border nelle dimensioni totali dell\'elemento.'
        },
        {
            question: 'Qual è la differenza tra :nth-child() e :nth-of-type()?',
            answers: [
                'Non ci sono differenze',
                'nth-child conta tutti i figli, nth-of-type solo quelli dello stesso tipo',
                'nth-of-type conta tutti i figli',
                'Entrambi contano solo i fratelli'
            ],
            correct: 1,
            difficulty: 'hard',
            explanation: ':nth-child() considera tutti i figli, mentre :nth-of-type() solo quelli dello stesso elemento.'
        },
        {
            question: 'Cosa fa la proprietà "grid-template-columns"?',
            answers: [
                'Definisce le colonne del grid',
                'Definisce le righe',
                'Crea un template',
                'Definisce i gap'
            ],
            correct: 0,
            difficulty: 'medium',
            explanation: 'grid-template-columns definisce il numero e la dimensione delle colonne in un CSS Grid.'
        },
        {
            question: 'Qual è lo scopo di "@media" in CSS?',
            answers: [
                'Includere media',
                'Creare media queries per il responsive design',
                'Definire animazioni',
                'Importare file CSS'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: '@media crea media queries per applicare stili diversi in base a condizioni come la larghezza dello schermo.'
        },
        {
            question: 'Cosa fa "transform: translate()"?',
            answers: [
                'Ruota l\'elemento',
                'Sposta l\'elemento',
                'Scala l\'elemento',
                'Inclina l\'elemento'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'translate() sposta l\'elemento dallo sua posizione originale sugli assi X e/o Y.'
        },
        {
            question: 'Qual è la differenza between em e rem?',
            answers: [
                'Non ci sono differenze',
                'em è relativo al parent, rem alla radice',
                'rem è relativo al parent, em alla radice',
                'Entrambi sono uguali a px'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'em è relativo al font-size dell\'elemento parent. rem è relativo al font-size della radice.'
        },
        {
            question: 'Cosa fa la proprietà "opacity"?',
            answers: [
                'Rende l\'elemento invisibile',
                'Controlla la trasparenza dell\'elemento',
                'Crea un effetto blur',
                'Rimuove l\'elemento'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'opacity controlla il livello di trasparenza dell\'elemento, da 0 (invisibile) a 1 (completamente opaco).'
        },
        {
            question: 'Qual è lo scopo di CSS Variables (--var)?',
            answers: [
                'Creare variabili JavaScript',
                'Definire valori riutilizzabili in CSS',
                'Definire variabili per il database',
                'Creare animazioni'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'CSS Variables (custom properties) permettono di definire valori riutilizzabili in tutto il CSS.'
        },
        {
            question: 'Cosa fa "justify-content" in Flexbox?',
            answers: [
                'Allinea gli elementi sull\'asse principale',
                'Allinea gli elementi sull\'asse trasversale',
                'Giustifica il testo',
                'Distribuisce lo spazio'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'justify-content allinea i flex item lungo l\'asse principale (orizzontale di default).'
        },
        {
            question: 'Qual è la differenza tra visibility: hidden e display: none?',
            answers: [
                'Non ci sono differenze',
                'hidden nasconde ma mantiene lo spazio, none rimuove completamente',
                'none mantiene lo spazio, hidden no',
                'Entrambi sono uguali'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'visibility: hidden nasconde l\'elemento ma mantiene lo spazio. display: none lo rimuove completamente dal layout.'
        }
    ],
    general: [
        {
            question: 'Cosa significa "DOM"?',
            answers: [
                'Document Object Model',
                'Data Object Mode',
                'Digital Ordinance Model',
                'Document Orientation Mode'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'DOM (Document Object Model) è la rappresentazione ad albero della struttura HTML della pagina.'
        },
        {
            question: 'Qual è lo scopo di CDN?',
            answers: [
                'Creare database',
                'Distribuire contenuti velocemente globalmente',
                'Compilare codice',
                'Creare design'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'CDN (Content Delivery Network) distribuisce contenuti come librerie velocemente tramite server globali.'
        },
        {
            question: 'Cosa significa "Responsive Design"?',
            answers: [
                'Design che risponde alle interazioni',
                'Design che si adatta a diverse dimensioni di schermo',
                'Design con animazioni',
                'Design veloce'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'Responsive Design crea layout che si adattano automaticamente a diverse dimensioni di dispositivi.'
        },
        {
            question: 'Qual è lo scopo di localStorage?',
            answers: [
                'Memorizzare file sul server',
                'Salvare dati persistente nel browser',
                'Creare database locali',
                'Gestire le sessioni'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'localStorage permette di salvare dati persistenti nel browser dell\'utente senza scadenza.'
        },
        {
            question: 'Cosa significa "API"?',
            answers: [
                'Application Programming Interface',
                'Advanced Programming Integration',
                'Automated Protocol Interface',
                'Application Process Integration'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'API (Application Programming Interface) è un insieme di protocolli per comunicare tra software.'
        },
        {
            question: 'Qual è la differenza tra GET e POST?',
            answers: [
                'Non ci sono differenze',
                'GET richiede dati, POST invia dati',
                'GET invia dati, POST richiede dati',
                'POST è più veloce'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'GET richiede dati dal server (parametri nell\'URL). POST invia dati nel body della richiesta.'
        },
        {
            question: 'Cosa significa "SEO"?',
            answers: [
                'Search Engine Optimization',
                'Site Enhancement Organization',
                'Secure Electronic Order',
                'Search Engine Organization'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'SEO (Search Engine Optimization) è l\'ottimizzazione per migliorare la visibilità nei motori di ricerca.'
        },
        {
            question: 'Qual è lo scopo di Git?',
            answers: [
                'Creare siti web',
                'Gestire versioni del codice',
                'Compilare JavaScript',
                'Ottimizzare immagini'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'Git è un sistema di controllo di versione per tracciare le modifiche nel codice.'
        },
        {
            question: 'Cosa significa "HTTP"?',
            answers: [
                'HyperText Transfer Protocol',
                'High Tech Transfer Protocol',
                'HyperText Transmission Process',
                'Hybrid Text Transfer Protocol'
            ],
            correct: 0,
            difficulty: 'easy',
            explanation: 'HTTP (HyperText Transfer Protocol) è il protocollo per trasferire dati sul web.'
        },
        {
            question: 'Qual è la differenza tra HTTP e HTTPS?',
            answers: [
                'Non ci sono differenze',
                'HTTPS è sicuro (crittografato), HTTP no',
                'HTTP è più veloce',
                'HTTPS non funziona'
            ],
            correct: 1,
            difficulty: 'easy',
            explanation: 'HTTPS è la versione sicura di HTTP con crittografia SSL/TLS per proteggere i dati.'
        },
        {
            question: 'Cosa significa "CRUD"?',
            answers: [
                'Create, Read, Update, Delete',
                'Code, Run, Upload, Download',
                'Create, Remove, Update, Display',
                'Compile, Run, Use, Delete'
            ],
            correct: 0,
            difficulty: 'medium',
            explanation: 'CRUD rappresenta le quattro operazioni base: Create, Read, Update, Delete sui dati.'
        },
        {
            question: 'Qual è lo scopo di Web Accessibility?',
            answers: [
                'Velocizzare il sito',
                'Rendere il sito utilizzabile da tutti, inclusi con disabilità',
                'Migliorare il design',
                'Ottimizzare per mobile'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'Web Accessibility rende i siti utilizzabili da persone con disabilità visive, motorie, cognitive.'
        },
        {
            question: 'Cosa significa "MVC"?',
            answers: [
                'Model View Controller',
                'Multiple View Control',
                'Model Variable Component',
                'Main View Container'
            ],
            correct: 0,
            difficulty: 'hard',
            explanation: 'MVC (Model-View-Controller) è un pattern architetturale che separa logica, interfaccia e controllo.'
        },
        {
            question: 'Qual è lo scopo del file "package.json"?',
            answers: [
                'Definire i pacchetti del server',
                'Configurare il progetto Node.js e le dipendenze',
                'Creare pacchetti JavaScript',
                'Definire lo stile del progetto'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'package.json contiene i metadati del progetto e l\'elenco delle dipendenze npm.'
        },
        {
            question: 'Cosa significa "Semantic HTML"?',
            answers: [
                'HTML con significato',
                'HTML che usa tag con significato semantico',
                'HTML veloce',
                'HTML con commenti'
            ],
            correct: 1,
            difficulty: 'medium',
            explanation: 'Semantic HTML usa tag con significato (header, nav, article) per descrivere il contenuto.'
        }
    ]
};

// Funzione per ottenere domande per categoria e difficoltà
function getQuestions(category, difficulty, count = 10) {
    let questions = questionsDB[category] || [];

    // Filtra per difficoltà se specificata
    if (difficulty && difficulty !== 'all') {
        questions = questions.filter(q => q.difficulty === difficulty);
    }

    // Se non ci sono abbastanza domande, prendi tutte
    if (questions.length === 0) {
        questions = questionsDB[category] || [];
    }

    // Mischia le domande
    const shuffled = shuffleArray([...questions]);

    // Restituisci il numero richiesto di domande
    return shuffled.slice(0, Math.min(count, shuffled.length));
}

// Funzione per mescolare un array (Algoritmo Fisher-Yates)
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Funzione per mescolare le risposte mantenendo traccia di quella corretta
function shuffleAnswers(question) {
    const answers = question.answers.map((answer, index) => ({
        text: answer,
        isCorrect: index === question.correct
    }));

    const shuffledAnswers = shuffleArray(answers);
    const correctIndex = shuffledAnswers.findIndex(a => a.isCorrect);

    return {
        ...question,
        shuffledAnswers,
        correctIndex
    };
}

// Funzione per ottenere domande dall'Open Trivia API (opzionale)
async function fetchQuestionsFromAPI(amount = 10, category = 9, difficulty = 'medium') {
    try {
        const url = `https://opentdb.com/api.php?amount=${amount}&category=${category}&difficulty=${difficulty}&type=multiple`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.results) {
            return data.results.map(q => ({
                question: decodeHTML(q.question),
                answers: shuffleArray([
                    decodeHTML(q.correct_answer),
                    ...q.incorrect_answers.map(a => decodeHTML(a))
                ]),
                correct: 0, // Sarà ricalcolato dopo lo shuffle
                difficulty: q.difficulty,
                explanation: 'Domanda dall\'Open Trivia Database'
            }));
        }

        return [];
    } catch (error) {
        console.error('Errore nel fetch delle domande:', error);
        return [];
    }
}

// Funzione helper per decodificare HTML entities
function decodeHTML(html) {
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
}

// Export per l'uso in altri file
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        categories,
        questionsDB,
        getQuestions,
        shuffleArray,
        shuffleAnswers,
        fetchQuestionsFromAPI
    };
}
