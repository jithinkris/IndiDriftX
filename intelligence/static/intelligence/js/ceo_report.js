/* CEO Report Generator — Groq API integration */

(function () {
    const config = window.CEO_CONFIG;
    if (!config) return;

    const shockSelect = document.getElementById('ceoShockSelect');
    const severitySlider = document.getElementById('ceoSeverity');
    const severityValue = document.getElementById('ceoSeverityValue');
    const generateBtn = document.getElementById('generateReport');
    const statusEl = document.getElementById('reportStatus');
    const reportContent = document.getElementById('reportContent');
    const reportMeta = document.getElementById('reportMeta');
    const exportActions = document.getElementById('reportExportActions');
    const exportReportCsv = document.getElementById('exportReportCsv');
    const exportReportPdf = document.getElementById('exportReportPdf');

    if (severitySlider) {
        severitySlider.addEventListener('input', function () {
            severityValue.textContent = severitySlider.value;
        });
    }

    function setExportLinks(reportId) {
        if (!reportId || !exportActions) return;
        exportActions.classList.remove('hidden');
        if (exportReportCsv) {
            exportReportCsv.href = config.exportCsvBase + reportId + '/csv/';
        }
        if (exportReportPdf) {
            exportReportPdf.href = config.exportPdfBase + reportId + '/pdf/';
        }
    }

    if (generateBtn) {
        generateBtn.addEventListener('click', function () {
            const shockType = shockSelect.value;
            const severity = parseInt(severitySlider.value, 10);

            statusEl.textContent = 'Generating report via Groq AI...';
            statusEl.className = 'status-message loading';
            generateBtn.disabled = true;

            if (exportActions) exportActions.classList.add('hidden');

            reportContent.innerHTML = '<div class="report-placeholder">' +
                '<span class="placeholder-icon">⏳</span>' +
                '<p>Analyzing supply chain shock scenario and generating executive briefing...</p></div>';

            fetch(config.generateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': config.csrfToken,
                },
                body: JSON.stringify({
                    shock_type: shockType,
                    severity: severity,
                }),
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    generateBtn.disabled = false;
                    if (data.error) {
                        statusEl.textContent = data.error;
                        statusEl.className = 'status-message error';
                        reportContent.innerHTML = '<div class="report-placeholder">' +
                            '<span class="placeholder-icon">⚠️</span>' +
                            '<p>' + data.error + '</p></div>';
                    } else {
                        statusEl.textContent = 'Report #' + data.id + ' generated successfully.';
                        statusEl.className = 'status-message success';
                        reportMeta.textContent = data.shock_type.replace(/_/g, ' ').toUpperCase() +
                            ' — Severity ' + data.severity + '%';
                        reportContent.innerHTML = formatReport(data.report);
                        setExportLinks(data.id);
                    }
                })
                .catch(function (err) {
                    generateBtn.disabled = false;
                    statusEl.textContent = 'Generation failed: ' + err.message;
                    statusEl.className = 'status-message error';
                });
        });
    }

    document.querySelectorAll('.view-report-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const item = btn.closest('.history-item');
            const report = item.dataset.report;
            const reportId = item.dataset.reportId;
            if (report) {
                reportContent.innerHTML = formatReport(report);
                reportMeta.textContent = 'Previous Report';
                setExportLinks(reportId);
            }
        });
    });

    function formatReport(text) {
        let html = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';
        html = html.replace(/<p><\/p>/g, '');
        html = html.replace(/<p>(<h[234]>)/g, '$1');
        html = html.replace(/(<\/h[234]>)<\/p>/g, '$1');
        html = html.replace(/<p>(<ul>)/g, '$1');
        html = html.replace(/(<\/ul>)<\/p>/g, '$1');

        return html;
    }
})();
