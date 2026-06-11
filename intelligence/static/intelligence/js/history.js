/* Shock History — trend line charts */

(function () {
    const data = window.HISTORY_DATA;
    if (!data || !data.labels || !data.labels.length) return;

    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#94a3b8' } },
        },
        scales: {
            x: {
                ticks: { color: '#94a3b8', maxRotation: 45 },
                grid: { color: 'rgba(30,58,95,0.3)' },
            },
            y: {
                ticks: { color: '#94a3b8' },
                grid: { color: 'rgba(30,58,95,0.5)' },
            },
        },
    };

    const priceCtx = document.getElementById('priceTrendChart');
    if (priceCtx) {
        new Chart(priceCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Price Increase (%)',
                    data: data.price_increase,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: data.colors,
                    pointRadius: 5,
                }],
            },
            options: chartDefaults,
        });
    }

    const shortageCtx = document.getElementById('shortageTrendChart');
    if (shortageCtx) {
        new Chart(shortageCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Shortage Probability (%)',
                    data: data.shortage_probability,
                    borderColor: '#eab308',
                    backgroundColor: 'rgba(234, 179, 8, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: data.colors,
                    pointRadius: 5,
                }],
            },
            options: chartDefaults,
        });
    }

    const combinedCtx = document.getElementById('combinedTrendChart');
    if (combinedCtx) {
        new Chart(combinedCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Severity (%)',
                        data: data.severity,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.05)',
                        tension: 0.3,
                        yAxisID: 'y',
                    },
                    {
                        label: 'GDP Impact (%)',
                        data: data.gdp_impact,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.05)',
                        tension: 0.3,
                        yAxisID: 'y',
                    },
                ],
            },
            options: chartDefaults,
        });
    }
})();
