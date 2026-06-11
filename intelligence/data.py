"""Hardcoded supply chain impact data — no external datasets."""

SHOCK_TYPES = {
    'oil': {
        'name': 'Oil Supply Shock',
        'description': 'Disruption to crude oil production, refining, or maritime chokepoints.',
        'base_price_impact': 18.5,
        'base_shortage_prob': 42.0,
        'icon': '⛽',
        'color': '#f59e0b',
    },
    'semiconductor': {
        'name': 'Semiconductor Shock',
        'description': 'Fab outages, export controls, or advanced chip supply bottlenecks.',
        'base_price_impact': 24.0,
        'base_shortage_prob': 55.0,
        'icon': '🔌',
        'color': '#3b82f6',
    },
    'rare_earth': {
        'name': 'Rare Earth Shock',
        'description': 'Mining restrictions or processing concentration risks for critical minerals.',
        'base_price_impact': 31.0,
        'base_shortage_prob': 48.0,
        'icon': '⚛️',
        'color': '#8b5cf6',
    },
}

COUNTRIES = [
    {'name': 'United States', 'code': 'USA', 'lat': 39.8, 'lng': -98.5, 'risk_level': 'medium', 'risk_score': 45,
     'oil_exposure': 55, 'semiconductor_exposure': 70, 'rare_earth_exposure': 40,
     'summary': 'Moderate exposure across energy and tech supply chains.'},
    {'name': 'China', 'code': 'CHN', 'lat': 35.8, 'lng': 104.1, 'risk_level': 'high', 'risk_score': 72,
     'oil_exposure': 65, 'semiconductor_exposure': 85, 'rare_earth_exposure': 95,
     'summary': 'Dominant rare earth processor; high semiconductor manufacturing concentration.'},
    {'name': 'Russia', 'code': 'RUS', 'lat': 61.5, 'lng': 105.3, 'risk_level': 'critical', 'risk_score': 88,
     'oil_exposure': 92, 'semiconductor_exposure': 30, 'rare_earth_exposure': 55,
     'summary': 'Major oil exporter; geopolitical volatility amplifies energy shock risk.'},
    {'name': 'Saudi Arabia', 'code': 'SAU', 'lat': 23.9, 'lng': 45.1, 'risk_level': 'high', 'risk_score': 68,
     'oil_exposure': 98, 'semiconductor_exposure': 15, 'rare_earth_exposure': 20,
     'summary': 'OPEC+ swing producer; oil shock epicenter.'},
    {'name': 'Taiwan', 'code': 'TWN', 'lat': 23.7, 'lng': 121.0, 'risk_level': 'critical', 'risk_score': 91,
     'oil_exposure': 80, 'semiconductor_exposure': 98, 'rare_earth_exposure': 60,
     'summary': 'TSMC hub; semiconductor shock would cascade globally.'},
    {'name': 'South Korea', 'code': 'KOR', 'lat': 35.9, 'lng': 127.8, 'risk_level': 'high', 'risk_score': 74,
     'oil_exposure': 75, 'semiconductor_exposure': 90, 'rare_earth_exposure': 50,
     'summary': 'Memory chip powerhouse with high import dependency.'},
    {'name': 'Japan', 'code': 'JPN', 'lat': 36.2, 'lng': 138.3, 'risk_level': 'medium', 'risk_score': 52,
     'oil_exposure': 70, 'semiconductor_exposure': 65, 'rare_earth_exposure': 45,
     'summary': 'Advanced materials supplier; energy import vulnerability.'},
    {'name': 'Germany', 'code': 'DEU', 'lat': 51.2, 'lng': 10.5, 'risk_level': 'medium', 'risk_score': 48,
     'oil_exposure': 60, 'semiconductor_exposure': 55, 'rare_earth_exposure': 35,
     'summary': 'Industrial manufacturing hub sensitive to energy and chip inputs.'},
    {'name': 'India', 'code': 'IND', 'lat': 20.6, 'lng': 78.9, 'risk_level': 'medium', 'risk_score': 50,
     'oil_exposure': 72, 'semiconductor_exposure': 45, 'rare_earth_exposure': 30,
     'summary': 'Growing demand center with rising import dependency.'},
    {'name': 'Australia', 'code': 'AUS', 'lat': -25.3, 'lng': 133.8, 'risk_level': 'low', 'risk_score': 28,
     'oil_exposure': 40, 'semiconductor_exposure': 20, 'rare_earth_exposure': 75,
     'summary': 'Rare earth mining potential; relatively insulated energy posture.'},
    {'name': 'Brazil', 'code': 'BRA', 'lat': -14.2, 'lng': -51.9, 'risk_level': 'low', 'risk_score': 32,
     'oil_exposure': 45, 'semiconductor_exposure': 25, 'rare_earth_exposure': 40,
     'summary': 'Commodity exporter with moderate diversification.'},
    {'name': 'United Kingdom', 'code': 'GBR', 'lat': 55.4, 'lng': -3.4, 'risk_level': 'medium', 'risk_score': 42,
     'oil_exposure': 50, 'semiconductor_exposure': 40, 'rare_earth_exposure': 25,
     'summary': 'Financial and services economy with moderate supply chain exposure.'},
    {'name': 'Vietnam', 'code': 'VNM', 'lat': 14.1, 'lng': 108.3, 'risk_level': 'medium', 'risk_score': 46,
     'oil_exposure': 55, 'semiconductor_exposure': 60, 'rare_earth_exposure': 35,
     'summary': 'Emerging electronics assembly hub.'},
    {'name': 'Indonesia', 'code': 'IDN', 'lat': -0.8, 'lng': 113.9, 'risk_level': 'medium', 'risk_score': 44,
     'oil_exposure': 50, 'semiconductor_exposure': 35, 'rare_earth_exposure': 70,
     'summary': 'Nickel and rare earth processing growth market.'},
    {'name': 'Chile', 'code': 'CHL', 'lat': -35.7, 'lng': -71.5, 'risk_level': 'low', 'risk_score': 25,
     'oil_exposure': 30, 'semiconductor_exposure': 15, 'rare_earth_exposure': 55,
     'summary': 'Lithium supplier; critical for EV supply chains.'},
]

SECTOR_RECOMMENDATIONS = {
    'oil': [
        {'sector': 'Energy', 'recommendation': 'BUY', 'confidence': 82, 'expected_return': 14.5,
         'rationale': 'Oil shocks historically boost upstream producers and integrated majors.'},
        {'sector': 'Transportation', 'recommendation': 'SELL', 'confidence': 75, 'expected_return': -8.2,
         'rationale': 'Airlines and logistics face margin compression from fuel cost spikes.'},
        {'sector': 'Consumer Discretionary', 'recommendation': 'HOLD', 'confidence': 60, 'expected_return': 2.1,
         'rationale': 'Mixed impact; premium brands resilient, mass market pressured.'},
        {'sector': 'Utilities', 'recommendation': 'BUY', 'confidence': 70, 'expected_return': 9.3,
         'rationale': 'Regulated returns and fuel pass-through mechanisms provide stability.'},
        {'sector': 'Technology', 'recommendation': 'HOLD', 'confidence': 55, 'expected_return': 1.5,
         'rationale': 'Data center costs rise but cloud demand remains structural.'},
        {'sector': 'Materials', 'recommendation': 'BUY', 'confidence': 78, 'expected_return': 11.0,
         'rationale': 'Commodity producers benefit from energy-linked pricing power.'},
    ],
    'semiconductor': [
        {'sector': 'Technology', 'recommendation': 'HOLD', 'confidence': 65, 'expected_return': 3.5,
         'rationale': 'Chip shortages hurt hardware margins but favor fabless leaders with pricing power.'},
        {'sector': 'Automotive', 'recommendation': 'SELL', 'confidence': 80, 'expected_return': -12.4,
         'rationale': 'Production halts and inventory build costs devastate OEM earnings.'},
        {'sector': 'Industrials', 'recommendation': 'HOLD', 'confidence': 58, 'expected_return': 0.8,
         'rationale': 'Automation demand persists but capex delays likely.'},
        {'sector': 'Healthcare', 'recommendation': 'BUY', 'confidence': 72, 'expected_return': 7.6,
         'rationale': 'Medical devices less chip-intensive; defensive characteristics.'},
        {'sector': 'Semiconductors', 'recommendation': 'BUY', 'confidence': 88, 'expected_return': 18.2,
         'rationale': 'Scarcity drives ASP increases; equipment makers see surge orders.'},
        {'sector': 'Consumer Electronics', 'recommendation': 'SELL', 'confidence': 77, 'expected_return': -9.5,
         'rationale': 'Smartphone and PC shipments constrained; promotional pricing unsustainable.'},
    ],
    'rare_earth': [
        {'sector': 'Materials', 'recommendation': 'BUY', 'confidence': 85, 'expected_return': 16.8,
         'rationale': 'Mining and processing companies capture scarcity premiums.'},
        {'sector': 'Clean Energy', 'recommendation': 'SELL', 'confidence': 78, 'expected_return': -10.1,
         'rationale': 'Wind turbine and EV motor costs spike; project delays mount.'},
        {'sector': 'Defense', 'recommendation': 'BUY', 'confidence': 80, 'expected_return': 12.3,
         'rationale': 'Governments stockpile critical minerals; defense primes secure contracts.'},
        {'sector': 'Automotive', 'recommendation': 'SELL', 'confidence': 83, 'expected_return': -14.0,
         'rationale': 'EV adoption slows as battery mineral costs surge.'},
        {'sector': 'Industrials', 'recommendation': 'HOLD', 'confidence': 62, 'expected_return': 2.5,
         'rationale': 'Magnet-dependent manufacturing faces input cost pressure.'},
        {'sector': 'Technology', 'recommendation': 'HOLD', 'confidence': 55, 'expected_return': 1.0,
         'rationale': 'Data center expansion continues but hardware costs increase.'},
    ],
}

CONSUMER_PRODUCTS = {
    'oil': [
        {'product': 'Gasoline', 'category': 'Transport', 'base_price_increase': 22.0, 'base_shortage': 15.0},
        {'product': 'Diesel', 'category': 'Transport', 'base_price_increase': 25.0, 'base_shortage': 18.0},
        {'product': 'Heating Oil', 'category': 'Energy', 'base_price_increase': 28.0, 'base_shortage': 20.0},
        {'product': 'Airline Tickets', 'category': 'Travel', 'base_price_increase': 15.0, 'base_shortage': 5.0},
        {'product': 'Food (Transport-linked)', 'category': 'Groceries', 'base_price_increase': 12.0, 'base_shortage': 8.0},
        {'product': 'Plastics & Packaging', 'category': 'Consumer', 'base_price_increase': 10.0, 'base_shortage': 12.0},
    ],
    'semiconductor': [
        {'product': 'Smartphones', 'category': 'Electronics', 'base_price_increase': 18.0, 'base_shortage': 35.0},
        {'product': 'Laptops & PCs', 'category': 'Electronics', 'base_price_increase': 22.0, 'base_shortage': 40.0},
        {'product': 'New Vehicles', 'category': 'Automotive', 'base_price_increase': 15.0, 'base_shortage': 55.0},
        {'product': 'Gaming Consoles', 'category': 'Electronics', 'base_price_increase': 20.0, 'base_shortage': 45.0},
        {'product': 'Home Appliances', 'category': 'Consumer', 'base_price_increase': 12.0, 'base_shortage': 30.0},
        {'product': 'Medical Devices', 'category': 'Healthcare', 'base_price_increase': 8.0, 'base_shortage': 25.0},
    ],
    'rare_earth': [
        {'product': 'Electric Vehicles', 'category': 'Automotive', 'base_price_increase': 20.0, 'base_shortage': 38.0},
        {'product': 'Wind Turbines', 'category': 'Energy', 'base_price_increase': 18.0, 'base_shortage': 42.0},
        {'product': 'Smartphones', 'category': 'Electronics', 'base_price_increase': 10.0, 'base_shortage': 20.0},
        {'product': 'LED Lighting', 'category': 'Consumer', 'base_price_increase': 14.0, 'base_shortage': 28.0},
        {'product': 'Defense Equipment', 'category': 'Government', 'base_price_increase': 12.0, 'base_shortage': 35.0},
        {'product': 'Industrial Magnets', 'category': 'Industrial', 'base_price_increase': 30.0, 'base_shortage': 50.0},
    ],
}

RISK_COLORS = {
    'low': '#22c55e',
    'medium': '#eab308',
    'high': '#f97316',
    'critical': '#ef4444',
}

EXPOSURE_FIELD = {
    'oil': 'oil_exposure',
    'semiconductor': 'semiconductor_exposure',
    'rare_earth': 'rare_earth_exposure',
}


def calculate_shock_impact(shock_type, severity):
    """Calculate impact metrics from shock type and severity (0-100)."""
    shock = SHOCK_TYPES[shock_type]
    factor = severity / 50.0

    price_increase = round(shock['base_price_impact'] * factor, 1)
    shortage_prob = min(99.0, round(shock['base_shortage_prob'] * factor, 1))
    gdp_impact = round(price_increase * 0.35, 2)

    exposure_key = EXPOSURE_FIELD[shock_type]
    affected = []
    for country in COUNTRIES:
        exposure = country[exposure_key]
        country_impact = round(exposure * (severity / 100), 1)
        if country_impact >= 25:
            affected.append({
                'name': country['name'],
                'code': country['code'],
                'impact': country_impact,
                'risk_level': country['risk_level'],
            })

    affected.sort(key=lambda x: x['impact'], reverse=True)

    return {
        'shock_type': shock_type,
        'shock_name': shock['name'],
        'severity': severity,
        'price_increase_pct': price_increase,
        'shortage_probability': shortage_prob,
        'gdp_impact_pct': gdp_impact,
        'affected_countries': affected,
        'affected_count': len(affected),
        'timeline': _build_timeline(shock_type, severity),
    }


def _build_timeline(shock_type, severity):
    """Generate phased shock timeline."""
    weeks = [
        {'phase': 'Week 1-2', 'label': 'Initial Disruption',
         'description': 'Spot prices spike; panic buying begins in wholesale markets.'},
        {'phase': 'Week 3-6', 'label': 'Supply Rationing',
         'description': 'Allocation protocols activate; downstream production slows.'},
        {'phase': 'Week 7-12', 'label': 'Consumer Pass-through',
         'description': 'Retail prices adjust; substitution and demand destruction emerge.'},
        {'phase': 'Month 4-6', 'label': 'Structural Adjustment',
         'description': 'Alternative suppliers ramp; inventory rebuild cycles start.'},
    ]
    intensity = severity / 100
    for entry in weeks:
        entry['intensity'] = round(intensity * 100)
    return weeks


def get_consumer_impacts(shock_type, severity):
    """Calculate consumer product impacts."""
    products = CONSUMER_PRODUCTS.get(shock_type, [])
    factor = severity / 50.0
    results = []
    for p in products:
        results.append({
            'product': p['product'],
            'category': p['category'],
            'price_increase': round(p['base_price_increase'] * factor, 1),
            'shortage_probability': min(99.0, round(p['base_shortage'] * factor, 1)),
        })
    return results


def get_sector_data(shock_type):
    """Return sector recommendations for a shock type."""
    return SECTOR_RECOMMENDATIONS.get(shock_type, [])


SUPPLIERS = [
    {'name': 'TSMC', 'sector': 'Semiconductors', 'country': 'TWN', 'tier': 1,
     'oil_exposure': 70, 'semiconductor_exposure': 98, 'rare_earth_exposure': 55,
     'description': 'World\'s largest contract chipmaker; single-point failure for advanced nodes.'},
    {'name': 'Samsung Electronics', 'sector': 'Semiconductors', 'country': 'KOR', 'tier': 1,
     'oil_exposure': 65, 'semiconductor_exposure': 92, 'rare_earth_exposure': 50,
     'description': 'Memory and logic chip giant; fabs in Korea and abroad.'},
    {'name': 'ASML', 'sector': 'Semiconductor Equipment', 'country': 'DEU', 'tier': 1,
     'oil_exposure': 40, 'semiconductor_exposure': 95, 'rare_earth_exposure': 30,
     'description': 'Monopoly on EUV lithography tools required for cutting-edge chips.'},
    {'name': 'Intel', 'sector': 'Semiconductors', 'country': 'USA', 'tier': 1,
     'oil_exposure': 50, 'semiconductor_exposure': 85, 'rare_earth_exposure': 45,
     'description': 'IDM with global fab network; sensitive to equipment and materials supply.'},
    {'name': 'Toyota Motor', 'sector': 'Automotive', 'country': 'JPN', 'tier': 1,
     'oil_exposure': 75, 'semiconductor_exposure': 80, 'rare_earth_exposure': 70,
     'description': 'Just-in-time manufacturing; highly exposed to chips and rare earth magnets.'},
    {'name': 'Apple', 'sector': 'Consumer Electronics', 'country': 'USA', 'tier': 1,
     'oil_exposure': 45, 'semiconductor_exposure': 88, 'rare_earth_exposure': 60,
     'description': 'Global supply chain orchestrator; Taiwan/Korea fab dependency.'},
    {'name': 'Aramco', 'sector': 'Energy', 'country': 'SAU', 'tier': 1,
     'oil_exposure': 99, 'semiconductor_exposure': 10, 'rare_earth_exposure': 15,
     'description': 'World\'s largest oil producer; epicenter of energy shock scenarios.'},
    {'name': 'ExxonMobil', 'sector': 'Energy', 'country': 'USA', 'tier': 1,
     'oil_exposure': 96, 'semiconductor_exposure': 25, 'rare_earth_exposure': 20,
     'description': 'Integrated oil major; refining and upstream operations globally.'},
    {'name': 'Shell', 'sector': 'Energy', 'country': 'GBR', 'tier': 1,
     'oil_exposure': 94, 'semiconductor_exposure': 20, 'rare_earth_exposure': 18,
     'description': 'Global LNG and refining player; European energy hub exposure.'},
    {'name': 'CATL', 'sector': 'Battery / EV', 'country': 'CHN', 'tier': 1,
     'oil_exposure': 40, 'semiconductor_exposure': 55, 'rare_earth_exposure': 90,
     'description': 'Largest EV battery maker; critical rare earth and lithium dependency.'},
    {'name': 'BYD', 'sector': 'Automotive / EV', 'country': 'CHN', 'tier': 1,
     'oil_exposure': 35, 'semiconductor_exposure': 70, 'rare_earth_exposure': 85,
     'description': 'Vertical EV integrator; battery and chip supply chain concentration.'},
    {'name': 'MP Materials', 'sector': 'Rare Earth Mining', 'country': 'USA', 'tier': 2,
     'oil_exposure': 30, 'semiconductor_exposure': 25, 'rare_earth_exposure': 92,
     'description': 'Only scaled rare earth mine in the US; processing still partly offshore.'},
    {'name': 'Lynas Rare Earths', 'sector': 'Rare Earth Processing', 'country': 'AUS', 'tier': 2,
     'oil_exposure': 25, 'semiconductor_exposure': 20, 'rare_earth_exposure': 95,
     'description': 'Non-Chinese rare earth separation; strategic Western supply alternative.'},
    {'name': 'Foxconn (Hon Hai)', 'sector': 'Electronics Manufacturing', 'country': 'TWN', 'tier': 2,
     'oil_exposure': 55, 'semiconductor_exposure': 75, 'rare_earth_exposure': 45,
     'description': 'Contract manufacturer for Apple, Dell, and others; assembly hub risk.'},
    {'name': 'Bosch', 'sector': 'Automotive Parts', 'country': 'DEU', 'tier': 2,
     'oil_exposure': 60, 'semiconductor_exposure': 78, 'rare_earth_exposure': 55,
     'description': 'Auto parts and chips supplier; European industrial backbone.'},
    {'name': 'Nidec', 'sector': 'Industrial Motors', 'country': 'JPN', 'tier': 2,
     'oil_exposure': 45, 'semiconductor_exposure': 50, 'rare_earth_exposure': 88,
     'description': 'EV motor and magnet manufacturer; neodymium dependency.'},
    {'name': 'Vestas', 'sector': 'Wind Energy', 'country': 'DEU', 'tier': 2,
     'oil_exposure': 30, 'semiconductor_exposure': 40, 'rare_earth_exposure': 82,
     'description': 'Wind turbine OEM; permanent magnet and gearbox supply risk.'},
    {'name': 'Maersk', 'sector': 'Logistics / Shipping', 'country': 'DEU', 'tier': 2,
     'oil_exposure': 85, 'semiconductor_exposure': 30, 'rare_earth_exposure': 20,
     'description': 'Container shipping leader; fuel costs and chokepoint exposure.'},
    {'name': 'Qualcomm', 'sector': 'Semiconductors', 'country': 'USA', 'tier': 2,
     'oil_exposure': 40, 'semiconductor_exposure': 82, 'rare_earth_exposure': 35,
     'description': 'Fabless chip designer; TSMC fabrication dependency.'},
    {'name': 'BASF', 'sector': 'Chemicals', 'country': 'DEU', 'tier': 3,
     'oil_exposure': 72, 'semiconductor_exposure': 35, 'rare_earth_exposure': 40,
     'description': 'Petrochemical giant; natural gas and oil feedstock sensitivity.'},
    {'name': 'Rio Tinto', 'sector': 'Mining', 'country': 'AUS', 'tier': 3,
     'oil_exposure': 35, 'semiconductor_exposure': 15, 'rare_earth_exposure': 70,
     'description': 'Diversified miner with lithium and rare earth interests.'},
    {'name': 'LG Energy Solution', 'sector': 'Battery / EV', 'country': 'KOR', 'tier': 2,
     'oil_exposure': 38, 'semiconductor_exposure': 60, 'rare_earth_exposure': 88,
     'description': 'Major EV battery supplier; cathode material concentration risk.'},
]


def _supplier_risk_level(score):
    if score >= 70:
        return 'critical'
    if score >= 50:
        return 'high'
    if score >= 30:
        return 'medium'
    return 'low'


def get_affected_suppliers(shock_type, severity):
    """Return suppliers ranked by risk for a given shock scenario."""
    exposure_key = EXPOSURE_FIELD[shock_type]
    results = []
    for supplier in SUPPLIERS:
        exposure = supplier[exposure_key]
        risk_score = round(exposure * (severity / 100), 1)
        if risk_score < 15:
            continue
        country_name = next(
            (c['name'] for c in COUNTRIES if c['code'] == supplier['country']),
            supplier['country'],
        )
        results.append({
            'name': supplier['name'],
            'sector': supplier['sector'],
            'country': country_name,
            'country_code': supplier['country'],
            'tier': supplier['tier'],
            'risk_score': risk_score,
            'risk_level': _supplier_risk_level(risk_score),
            'description': supplier['description'],
        })
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    return results


def compare_scenarios(shock_a, severity_a, shock_b, severity_b):
    """Compare two shock scenarios side by side."""
    impact_a = calculate_shock_impact(shock_a, severity_a)
    impact_b = calculate_shock_impact(shock_b, severity_b)
    return {
        'scenario_a': impact_a,
        'scenario_b': impact_b,
        'delta': {
            'price_increase_pct': round(impact_b['price_increase_pct'] - impact_a['price_increase_pct'], 1),
            'shortage_probability': round(impact_b['shortage_probability'] - impact_a['shortage_probability'], 1),
            'gdp_impact_pct': round(impact_b['gdp_impact_pct'] - impact_a['gdp_impact_pct'], 2),
            'affected_count': impact_b['affected_count'] - impact_a['affected_count'],
        },
        'suppliers_a': get_affected_suppliers(shock_a, severity_a)[:8],
        'suppliers_b': get_affected_suppliers(shock_b, severity_b)[:8],
    }
