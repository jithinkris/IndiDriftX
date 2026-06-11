/* Investment Dashboard — Chart.js visualizations */

(function () {
    const data = window.INVESTMENT_DATA;
    if (!data) return;

    const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#94a3b8' },
            },
        },
    };

    const pieCtx = document.getElementById('recommendationChart');
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'doughnut',
            data: {
                labels: ['BUY', 'HOLD', 'SELL'],
                datasets: [{
                    data: [data.buyCount, data.holdCount, data.sellCount],
                    backgroundColor: ['#22c55e', '#eab308', '#ef4444'],
                    borderColor: '#111d35',
                    borderWidth: 2,
                }],
            },
            options: {
                ...chartDefaults,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8', padding: 16 },
                    },
                },
            },
        });
    }

    const barCtx = document.getElementById('returnsChart');
    if (barCtx && data.sectors) {
        const labels = data.sectors.map(function (s) { return s.sector; });
        const returns = data.sectors.map(function (s) { return s.expected_return; });
        const colors = returns.map(function (r) {
            return r > 0 ? 'rgba(34, 197, 94, 0.7)' : 'rgba(239, 68, 68, 0.7)';
        });

        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Expected Return (%)',
                    data: returns,
                    backgroundColor: colors,
                    borderRadius: 4,
                }],
            },
            options: {
                ...chartDefaults,
                indexAxis: 'y',
                scales: {
                    x: {
                        grid: { color: 'rgba(30, 58, 95, 0.5)' },
                        ticks: { color: '#94a3b8' },
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#e2e8f0' },
                    },
                },
            },
        });
    }
})();
