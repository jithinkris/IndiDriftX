/* World Risk Map — Leaflet.js country markers */

(function () {
    const countries = window.RISK_MAP_DATA;
    if (!countries || !countries.length) return;

    const map = L.map('riskMap', {
        center: [25, 10],
        zoom: 2,
        minZoom: 2,
        maxZoom: 8,
        worldCopyJump: true,
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 19,
    }).addTo(map);

    const riskSizes = {
        low: 8,
        medium: 10,
        high: 12,
        critical: 14,
    };

    countries.forEach(function (country) {
        const radius = riskSizes[country.risk_level] || 10;

        const marker = L.circleMarker([country.lat, country.lng], {
            radius: radius,
            fillColor: country.color,
            color: '#fff',
            weight: 1,
            opacity: 0.9,
            fillOpacity: 0.75,
        }).addTo(map);

        const popup = '<strong>' + country.name + '</strong><br>' +
            'Risk: <span style="color:' + country.color + '">' +
            country.risk_level.toUpperCase() + '</span> (' + country.risk_score + '/100)<br>' +
            'Oil: ' + country.oil_exposure + '% | Semi: ' + country.semiconductor_exposure +
            '% | Rare Earth: ' + country.rare_earth_exposure + '%<br>' +
            '<em>' + country.summary + '</em>';

        marker.bindPopup(popup);
    });

    const tbody = document.querySelector('#countryTable tbody');
    if (tbody) {
        const sorted = countries.slice().sort(function (a, b) {
            return b.risk_score - a.risk_score;
        });

        tbody.innerHTML = sorted.map(function (c) {
            return '<tr>' +
                '<td><span class="risk-dot risk-' + c.risk_level + '"></span> ' + c.name + '</td>' +
                '<td><span class="badge" style="background:' + c.color + '">' + c.risk_level + '</span></td>' +
                '<td>' + c.risk_score + '</td>' +
                '<td>' + c.oil_exposure + '%</td>' +
                '<td>' + c.semiconductor_exposure + '%</td>' +
                '<td>' + c.rare_earth_exposure + '%</td>' +
                '</tr>';
        }).join('');
    }
})();
