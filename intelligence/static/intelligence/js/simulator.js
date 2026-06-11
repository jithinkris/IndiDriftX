/* Shock Simulator — interactive severity slider and live updates */

(function () {
    const config = window.SIMULATOR_CONFIG;
    if (!config) return;

    let currentShock = config.selectedShock;
    let currentSeverity = config.severity;

    const slider = document.getElementById('severitySlider');
    const severityValue = document.getElementById('severityValue');
    const shockBtns = document.querySelectorAll('.shock-btn');
    const runBtn = document.getElementById('runSimulation');
    const statusEl = document.getElementById('simStatus');
    const exportCsv = document.getElementById('exportCsv');
    const exportPdf = document.getElementById('exportPdf');

    function updateExportLinks() {
        const query = '?shock=' + currentShock + '&severity=' + currentSeverity;
        if (exportCsv) exportCsv.href = config.exportCsvBase + query;
        if (exportPdf) exportPdf.href = config.exportPdfBase + query;
    }

    updateExportLinks();

    shockBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            shockBtns.forEach(function (b) { b.classList.remove('active'); });
            btn.classList.add('active');
            currentShock = btn.dataset.shock;
            fetchImpact();
            updateExportLinks();
        });
    });

    if (slider) {
        slider.addEventListener('input', function () {
            currentSeverity = parseInt(slider.value, 10);
            severityValue.textContent = currentSeverity;
            fetchImpact();
            updateExportLinks();
        });
    }

    function fetchImpact() {
        const url = config.apiUrl + '?shock=' + currentShock + '&severity=' + currentSeverity;
        fetch(url)
            .then(function (res) { return res.json(); })
            .then(function (data) { updateUI(data.impact); })
            .catch(function (err) { console.error('Impact fetch failed:', err); });
    }

    function updateUI(impact) {
        document.getElementById('priceImpact').textContent = '+' + impact.price_increase_pct + '%';
        document.getElementById('shortageProb').textContent = impact.shortage_probability + '%';
        document.getElementById('gdpImpact').textContent = impact.gdp_impact_pct + '%';
        document.getElementById('affectedCount').textContent = impact.affected_count;

        const timeline = document.getElementById('shockTimeline');
        if (timeline && impact.timeline) {
            timeline.innerHTML = impact.timeline.map(function (phase) {
                return '<div class="timeline-item">' +
                    '<div class="timeline-marker"></div>' +
                    '<div class="timeline-content">' +
                    '<strong>' + phase.phase + ' — ' + phase.label + '</strong>' +
                    '<p>' + phase.description + '</p>' +
                    '</div></div>';
            }).join('');
        }

        const countries = document.getElementById('affectedCountries');
        if (countries && impact.affected_countries) {
            countries.innerHTML = impact.affected_countries.map(function (c) {
                return '<div class="affected-country">' +
                    '<span class="country-name">' + c.name + '</span>' +
                    '<div class="impact-bar"><div class="impact-fill" style="width:' + c.impact + '%"></div></div>' +
                    '<span class="impact-value">' + c.impact + '%</span>' +
                    '</div>';
            }).join('');
        }
    }

    if (runBtn) {
        runBtn.addEventListener('click', function () {
            statusEl.textContent = 'Running simulation...';
            statusEl.className = 'status-message loading';

            fetch(config.runUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': config.csrfToken,
                },
                body: JSON.stringify({
                    shock_type: currentShock,
                    severity: currentSeverity,
                }),
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    if (data.error) {
                        statusEl.textContent = data.error;
                        statusEl.className = 'status-message error';
                    } else {
                        statusEl.textContent = 'Simulation #' + data.id + ' saved successfully.';
                        statusEl.className = 'status-message success';
                        updateUI(data.impact);
                    }
                })
                .catch(function (err) {
                    statusEl.textContent = 'Simulation failed: ' + err.message;
                    statusEl.className = 'status-message error';
                });
        });
    }
})();
