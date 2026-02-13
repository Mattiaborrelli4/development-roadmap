// Dati di esempio per la dashboard
const dashboardData = {
    week: {
        labels: ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'],
        vendite: [4500, 5200, 4800, 6100, 5500, 7200, 6800],
        entrate: [11250, 13000, 12000, 15250, 13750, 18000, 17000],
        utenti: [320, 385, 360, 440, 410, 520, 490],
        conversioni: [3.2, 3.8, 3.5, 4.1, 3.9, 4.8, 4.5]
    },
    month: {
        labels: ['Sett 1', 'Sett 2', 'Sett 3', 'Sett 4'],
        vendite: [32000, 38000, 35000, 42000],
        entrate: [80000, 95000, 87500, 105000],
        utenti: [2400, 2850, 2650, 3100],
        conversioni: [3.5, 4.2, 3.8, 4.5]
    },
    quarter: {
        labels: ['Gennaio', 'Febbraio', 'Marzo'],
        vendite: [145000, 158000, 172000],
        entrate: [362500, 395000, 430000],
        utenti: [10500, 11800, 12800],
        conversioni: [3.8, 4.1, 4.4]
    },
    year: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        vendite: [475000, 520000, 580000, 650000],
        entrate: [1187500, 1300000, 1450000, 1625000],
        utenti: [35100, 39500, 44500, 51200],
        conversioni: [3.9, 4.2, 4.5, 4.8]
    }
};

const categoryData = {
    categories: ['Elettronica', 'Abbigliamento', 'Casa & Giardino', 'Sport', 'Alimentari', 'Libri'],
    values: [35000, 28000, 22000, 18000, 15000, 12000]
};

const userDistribution = {
    labels: ['18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
    data: [15, 35, 28, 12, 7, 3]
};

const productPerformance = {
    products: ['Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Cuffie', 'Console'],
    sales: [8500, 7200, 5800, 4900, 4200, 3500]
};

const monthlyMetrics = {
    labels: ['Vendite', 'Entrate', 'Utenti', 'Conversione', 'Soddisfazione', 'Ritorno'],
    data: [85, 78, 92, 68, 88, 75]
};

// Configurazione globale Chart.js
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = '#475569';

// Variabili globali per i grafici
let lineChart, barChart, pieChart, horizontalBarChart, radarChart;
let currentPeriod = 'week';

// Inizializzazione
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupEventListeners();
    updateDashboard('week');
});

function initializeCharts() {
    // Grafico Linea - Trend Vendite e Entrate
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Vendite',
                    data: [],
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#4f46e5',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                },
                {
                    label: 'Entrate (€)',
                    data: [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    borderColor: '#475569',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.dataset.label === 'Entrate (€)') {
                                label += '€' + context.parsed.y.toLocaleString('it-IT');
                            } else {
                                label += context.parsed.y.toLocaleString('it-IT');
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '€' + value.toLocaleString('it-IT');
                        }
                    }
                }
            }
        }
    });

    // Grafico Barre - Vendite per Categoria
    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: categoryData.categories,
            datasets: [{
                label: 'Vendite (€)',
                data: categoryData.values,
                backgroundColor: [
                    'rgba(79, 70, 229, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(6, 182, 212, 0.8)'
                ],
                borderColor: [
                    'rgba(79, 70, 229, 1)',
                    'rgba(139, 92, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(6, 182, 212, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    callbacks: {
                        label: function(context) {
                            return '€' + context.parsed.y.toLocaleString('it-IT');
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '€' + (value / 1000) + 'k';
                        }
                    }
                }
            }
        }
    });

    // Grafico Torta - Distribuzione Utenti
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    pieChart = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: userDistribution.labels,
            datasets: [{
                data: userDistribution.data,
                backgroundColor: [
                    'rgba(79, 70, 229, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(6, 182, 212, 0.8)'
                ],
                borderColor: 'rgba(30, 41, 59, 1)',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return context.label + ': ' + percentage + '%';
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });

    // Grafico Barre Orizzontali - Performance Prodotti
    const horizontalBarCtx = document.getElementById('horizontalBarChart').getContext('2d');
    horizontalBarChart = new Chart(horizontalBarCtx, {
        type: 'bar',
        data: {
            labels: productPerformance.products,
            datasets: [{
                label: 'Vendite',
                data: productPerformance.sales,
                backgroundColor: 'rgba(79, 70, 229, 0.8)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    callbacks: {
                        label: function(context) {
                            return context.parsed.x.toLocaleString('it-IT') + ' unità';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    }
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    // Grafico Radar - Metriche Mensili
    const radarCtx = document.getElementById('radarChart').getContext('2d');
    radarChart = new Chart(radarCtx, {
        type: 'radar',
        data: {
            labels: monthlyMetrics.labels,
            datasets: [{
                label: 'Performance',
                data: monthlyMetrics.data,
                backgroundColor: 'rgba(79, 70, 229, 0.2)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 3,
                pointBackgroundColor: 'rgba(79, 70, 229, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.95)',
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.r + '/100';
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    angleLines: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    pointLabels: {
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

function setupEventListeners() {
    // Filtri periodo
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentPeriod = this.dataset.period;
            updateDashboard(currentPeriod);
        });
    });

    // Filtri categoria
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            updateChartVisibility();
        });
    });

    // Selettore tipo grafico
    const chartTypeSelects = document.querySelectorAll('.chart-type-select');
    chartTypeSelects.forEach(select => {
        select.addEventListener('change', function() {
            const chartId = this.dataset.chart;
            changeChartType(chartId, this.value);
        });
    });
}

function updateDashboard(period) {
    const data = dashboardData[period];

    // Aggiorna grafico linea
    lineChart.data.labels = data.labels;
    lineChart.data.datasets[0].data = data.vendite;
    lineChart.data.datasets[1].data = data.entrate;
    lineChart.update('active');

    // Aggiorna statistiche
    updateStats(data);

    // Aggiorna tabella
    updateTable(data);
}

function updateStats(data) {
    const totalRevenue = data.entrate.reduce((a, b) => a + b, 0);
    const totalSales = data.vendite.reduce((a, b) => a + b, 0);
    const activeUsers = data.utenti[data.utenti.length - 1];
    const avgConversion = (data.conversioni.reduce((a, b) => a + b, 0) / data.conversioni.length).toFixed(1);

    animateValue('totalRevenue', totalRevenue, '€');
    animateValue('activeUsers', activeUsers, '');
    animateValue('totalSales', totalSales, '');
    animateValue('conversionRate', avgConversion, '%');
}

function animateValue(elementId, value, prefix) {
    const element = document.getElementById(elementId);
    const startValue = 0;
    const duration = 1000;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const currentValue = startValue + (value - startValue) * easeOutQuart(progress);

        if (prefix === '€') {
            element.textContent = prefix + Math.floor(currentValue).toLocaleString('it-IT');
        } else if (prefix === '%') {
            element.textContent = currentValue + prefix;
        } else {
            element.textContent = Math.floor(currentValue).toLocaleString('it-IT');
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function easeOutQuart(x) {
    return 1 - Math.pow(1 - x, 4);
}

function updateTable(data) {
    const tbody = document.getElementById('dataTableBody');
    tbody.innerHTML = '';

    data.labels.forEach((label, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${label}</td>
            <td>${data.vendite[index].toLocaleString('it-IT')}</td>
            <td>€${data.entrate[index].toLocaleString('it-IT')}</td>
            <td>${data.utenti[index].toLocaleString('it-IT')}</td>
            <td>${data.conversioni[index]}%</td>
        `;
        tbody.appendChild(row);
    });
}

function updateChartVisibility() {
    const checkboxes = document.querySelectorAll('.category-filter:checked');
    const visibleCategories = Array.from(checkboxes).map(cb => cb.value);

    // Mostra/nascondi dataset nel grafico linea
    lineChart.data.datasets.forEach((dataset, index) => {
        if (index === 0) {
            dataset.hidden = !visibleCategories.includes('vendite');
        } else if (index === 1) {
            dataset.hidden = !visibleCategories.includes('entrate');
        }
    });
    lineChart.update('active');
}

function changeChartType(chartId, newType) {
    const chart = eval(chartId);
    const config = chart.config;

    // Destroy and recreate chart with new type
    chart.destroy();

    if (chartId === 'lineChart') {
        const ctx = document.getElementById('lineChart').getContext('2d');
        lineChart = new Chart(ctx, {
            type: newType,
            data: config.data,
            options: config.options
        });
    }
}

// Simula aggiornamento dati in tempo reale
setInterval(() => {
    // Aggiorna leggermente i dati del radar chart
    radarChart.data.datasets[0].data = radarChart.data.datasets[0].data.map(value => {
        const change = Math.floor(Math.random() * 5) - 2;
        return Math.max(0, Math.min(100, value + change));
    });
    radarChart.update('none');
}, 5000);
