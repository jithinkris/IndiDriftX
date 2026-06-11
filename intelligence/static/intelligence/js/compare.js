/* Scenario Comparison — side-by-side shock analysis */

(function () {
    const config = window.COMPARE_CONFIG;
    if (!config) return;

    let shockA = config.shockA;
    let shockB = config.shockB;
    let severityA = config.severityA;
    let severityB = config.severityB;
    let compareChart = null;

    document.querySelectorAll('.shock-btn-a').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.shock-btn-a').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            shockA = btn.dataset.shock;
            fetchCompare();
        });
    });

    document.querySelectorAll('.shock-btn-b').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.shock-btn-b').forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            shockB = btn.dataset.shock;
            fetchCompare();
        });
    });

    const sliderA = document.getElementById('severityA');
    const sliderB = document.getElementById('severityB');

    if (sliderA) {
        sliderA.addEventListener('input', function () {
            severityA = parseInt(sliderA.value, 10);
            document.getElementById('severityValueA').textContent = severityA;
            fetchCompare();
        });
    }

    if (sliderB) {
        sliderB.addEventListener('input', function () {
            severityB = parseInt(sliderB.value, 10);
            document.getElementById('severityValueB').textContent = severityB;
            fetchCompare();
        });
    }

    function fetchCompare() {
        const url = config.apiUrl + '?shock_a=' + shockA + '&severity_a=' + severityA +
            '&shock_b=' + shockB + '&severity_b=' + severityB;
        fetch(url)
            .then(function (res) { return res.json(); })
            .then(function (data) { updateUI(data); })
            .catch(function (err) { console.error('Compare fetch failed:', err); });
    }

    function updateUI(data) {
        updateMetrics('metricsA', data.scenario_a);
        updateMetrics('metricsB', data.scenario_b);
        updateDelta(data.delta);
        updateSuppliers('suppliersA', data.suppliers_a);
        updateSuppliers('suppliersB', data.suppliers_b);
        updateChart(data);
    }

    function updateMetrics(id, impact) {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML =
            '<div class="compare-metric"><span>Price Increase</span><strong class="text-danger">+' +
            impact.price_increase_pct + '%</strong></div>' +
            '<div class="compare-metric"><span>Shortage Prob.</span><strong class="text-warning">' +
            impact.shortage_probability + '%</strong></div>' +
            '<div class="compare-metric"><span>GDP Impact</span><strong>' +
            impact.gdp_impact_pct + '%</strong></div>' +
            '<div class="compare-metric"><span>Countries</span><strong>' +
            impact.affected_count + '</strong></div>';
    }

    function updateDelta(delta) {
        function fmt(val, suffix) {
            return (val > 0 ? '+' : '') + val + suffix;
        }
        const priceEl = document.getElementById('deltaPrice');
        const shortEl = document.getElementById('deltaShortage');
        const gdpEl = document.getElementById('deltaGdp');
        if (priceEl) {
            priceEl.textContent = fmt(delta.price_increase_pct, '%');
            priceEl.className = delta.price_increase_pct > 0 ? 'text-danger' :
                delta.price_increase_pct < 0 ? 'text-success' : '';
        }
        if (shortEl) shortEl.textContent = fmt(delta.shortage_probability, '%');
        if (gdpEl) gdpEl.textContent = fmt(delta.gdp_impact_pct, '%');
    }

    function updateSuppliers(id, suppliers) {
        const el = document.getElementById(id);
        if (!el) return;
        el.innerHTML = suppliers.map(function (s) {
            return '<div class="supplier-mini risk-' + s.risk_level + '">' +
                '<strong>' + s.name + '</strong>' +
                '<span>' + s.sector + '</span>' +
                '<span class="risk-badge-mini">' + s.risk_score + '%</span></div>';
        }).join('');
    }

    function updateChart(data) {
        const ctx = document.getElementById('compareChart');
        if (!ctx) return;

        const labels = ['Price Increase', 'Shortage Prob.', 'GDP Impact', 'Countries'];
        const datasetA = [
            data.scenario_a.price_increase_pct,
            data.scenario_a.shortage_probability,
            data.scenario_a.gdp_impact_pct,
            data.scenario_a.affected_count,
        ];
        const datasetB = [
            data.scenario_b.price_increase_pct,
            data.scenario_b.shortage_probability,
            data.scenario_b.gdp_impact_pct,
            data.scenario_b.affected_count,
        ];

        if (compareChart) {
            compareChart.data.datasets[0].data = datasetA;
            compareChart.data.datasets[0].label = data.scenario_a.shock_name;
            compareChart.data.datasets[1].data = datasetB;
            compareChart.data.datasets[1].label = data.scenario_b.shock_name;
            compareChart.update();
            return;
        }

        compareChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: data.scenario_a.shock_name,
                        data: datasetA,
                        backgroundColor: 'rgba(245, 158, 11, 0.7)',
                        borderRadius: 4,
                    },
                    {
                        label: data.scenario_b.shock_name,
                        data: datasetB,
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#94a3b8' } },
                },
                scales: {
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(30,58,95,0.5)' } },
                    x: { ticks: { color: '#e2e8f0' }, grid: { display: false } },
                },
            },
        });
    }

    if (config.initial) {
        updateChart(config.initial);
    }
})();
