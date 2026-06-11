import json

import requests
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .data import (
    COUNTRIES,
    RISK_COLORS,
    SHOCK_TYPES,
    calculate_shock_impact,
    compare_scenarios,
    get_affected_suppliers,
    get_consumer_impacts,
    get_sector_data,
)
from .exporters import (
    build_simulation_export_data,
    export_ceo_report_csv,
    export_ceo_report_pdf,
    export_simulation_csv,
    export_simulation_pdf,
)
from .models import CEOReport, ShockSimulation


def dashboard(request):
    """Main dashboard overview."""
    default_shock = 'oil'
    default_severity = 50
    impact = calculate_shock_impact(default_shock, default_severity)
    context = {
        'shock_types': SHOCK_TYPES,
        'countries': COUNTRIES,
        'risk_colors': RISK_COLORS,
        'default_impact': impact,
        'recent_simulations': ShockSimulation.objects.all()[:5],
        'recent_reports': CEOReport.objects.all()[:3],
    }
    return render(request, 'intelligence/dashboard.html', context)


def shock_simulator(request):
    """Shock simulator with severity slider."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))

    impact = calculate_shock_impact(shock_type, severity)

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'severity': severity,
        'impact': impact,
        'impact_json': json.dumps(impact),
    }
    return render(request, 'intelligence/shock_simulator.html', context)


@require_POST
def run_simulation(request):
    """API endpoint to run and persist a shock simulation."""
    try:
        body = json.loads(request.body)
        shock_type = body.get('shock_type', 'oil')
        severity = int(body.get('severity', 50))
        severity = max(0, min(100, severity))

        if shock_type not in SHOCK_TYPES:
            return JsonResponse({'error': 'Invalid shock type'}, status=400)

        impact = calculate_shock_impact(shock_type, severity)

        simulation = ShockSimulation.objects.create(
            shock_type=shock_type,
            severity=severity,
            price_increase_pct=impact['price_increase_pct'],
            shortage_probability=impact['shortage_probability'],
            affected_countries=impact['affected_count'],
            gdp_impact_pct=impact['gdp_impact_pct'],
            results_json=impact,
        )

        return JsonResponse({
            'id': simulation.id,
            'impact': impact,
            'message': 'Simulation saved successfully',
        })
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)


def risk_map(request):
    """World risk map with Leaflet markers."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'

    countries_data = []
    for c in COUNTRIES:
        countries_data.append({
            'name': c['name'],
            'code': c['code'],
            'lat': c['lat'],
            'lng': c['lng'],
            'risk_level': c['risk_level'],
            'risk_score': c['risk_score'],
            'color': RISK_COLORS[c['risk_level']],
            'summary': c['summary'],
            'oil_exposure': c['oil_exposure'],
            'semiconductor_exposure': c['semiconductor_exposure'],
            'rare_earth_exposure': c['rare_earth_exposure'],
        })

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'countries_json': json.dumps(countries_data),
        'risk_colors': RISK_COLORS,
    }
    return render(request, 'intelligence/risk_map.html', context)


def consumer_impact(request):
    """Consumer impact cards."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))

    impacts = get_consumer_impacts(shock_type, severity)
    shock = SHOCK_TYPES[shock_type]

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'severity': severity,
        'impacts': impacts,
        'shock': shock,
    }
    return render(request, 'intelligence/consumer_impact.html', context)


def investment_dashboard(request):
    """Investment dashboard with Chart.js."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'

    sectors = get_sector_data(shock_type)
    buy_count = sum(1 for s in sectors if s['recommendation'] == 'BUY')
    hold_count = sum(1 for s in sectors if s['recommendation'] == 'HOLD')
    sell_count = sum(1 for s in sectors if s['recommendation'] == 'SELL')

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'sectors': sectors,
        'sectors_json': json.dumps(sectors),
        'buy_count': buy_count,
        'hold_count': hold_count,
        'sell_count': sell_count,
    }
    return render(request, 'intelligence/investment.html', context)


def ceo_report(request):
    """CEO report generator page."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'severity': severity,
        'has_api_key': bool(settings.GROQ_API_KEY),
        'groq_model': settings.GROQ_MODEL,
        'recent_reports': CEOReport.objects.all()[:5],
    }
    return render(request, 'intelligence/ceo_report.html', context)


@require_POST
def generate_ceo_report(request):
    """Generate CEO report via Groq API."""
    try:
        body = json.loads(request.body)
        shock_type = body.get('shock_type', 'oil')
        severity = int(body.get('severity', 50))
        severity = max(0, min(100, severity))

        if shock_type not in SHOCK_TYPES:
            return JsonResponse({'error': 'Invalid shock type'}, status=400)

        if not settings.GROQ_API_KEY:
            return JsonResponse({
                'error': 'GROQ_API_KEY not configured. Add it to your .env file.',
            }, status=500)

        impact = calculate_shock_impact(shock_type, severity)
        consumer = get_consumer_impacts(shock_type, severity)
        sectors = get_sector_data(shock_type)

        prompt = _build_ceo_prompt(impact, consumer, sectors)

        response = requests.post(
            settings.GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {settings.GROQ_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.GROQ_MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': (
                            'You are a chief strategy officer briefing the CEO on global '
                            'supply chain shocks. Write concise, executive-level reports '
                            'with clear sections: Executive Summary, Risk Assessment, '
                            'Consumer Impact, Investment Implications, and Recommended Actions. '
                            'Use bullet points where appropriate. Be data-driven.'
                        ),
                    },
                    {'role': 'user', 'content': prompt},
                ],
                'temperature': 0.7,
                'max_tokens': 2048,
            },
            timeout=30,
        )

        if response.status_code != 200:
            return JsonResponse({
                'error': f'Groq API error: {response.status_code} - {response.text}',
            }, status=502)

        result = response.json()
        report_content = result['choices'][0]['message']['content']

        report = CEOReport.objects.create(
            shock_type=shock_type,
            severity=severity,
            report_content=report_content,
        )

        return JsonResponse({
            'id': report.id,
            'report': report_content,
            'shock_type': shock_type,
            'severity': severity,
        })

    except requests.RequestException as exc:
        return JsonResponse({'error': f'API request failed: {exc}'}, status=502)
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)


def _build_ceo_prompt(impact, consumer, sectors):
    """Build the prompt for CEO report generation."""
    consumer_lines = '\n'.join(
        f"- {c['product']}: +{c['price_increase']}% price, {c['shortage_probability']}% shortage risk"
        for c in consumer
    )
    sector_lines = '\n'.join(
        f"- {s['sector']}: {s['recommendation']} (confidence {s['confidence']}%, "
        f"expected return {s['expected_return']:+.1f}%)"
        for s in sectors
    )
    country_lines = '\n'.join(
        f"- {c['name']}: impact score {c['impact']}"
        for c in impact['affected_countries'][:8]
    )

    return f"""Generate an executive intelligence report for the following supply chain shock scenario:

SHOCK TYPE: {impact['shock_name']}
SEVERITY: {impact['severity']}%

KEY METRICS:
- Projected price increase: {impact['price_increase_pct']}%
- Shortage probability: {impact['shortage_probability']}%
- GDP impact estimate: {impact['gdp_impact_pct']}%
- Affected countries: {impact['affected_count']}

TOP AFFECTED COUNTRIES:
{country_lines}

CONSUMER IMPACT:
{consumer_lines}

INVESTMENT RECOMMENDATIONS BY SECTOR:
{sector_lines}

Provide actionable strategic guidance for C-suite leadership."""


@require_GET
def api_impact(request):
    """JSON API for shock impact calculations."""
    shock_type = request.GET.get('shock', 'oil')
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))

    if shock_type not in SHOCK_TYPES:
        return JsonResponse({'error': 'Invalid shock type'}, status=400)

    impact = calculate_shock_impact(shock_type, severity)
    consumer = get_consumer_impacts(shock_type, severity)
    sectors = get_sector_data(shock_type)

    return JsonResponse({
        'impact': impact,
        'consumer': consumer,
        'sectors': sectors,
    })


def scenario_compare(request):
    """Side-by-side comparison of two shock scenarios."""
    shock_a = request.GET.get('shock_a', 'oil')
    shock_b = request.GET.get('shock_b', 'semiconductor')
    severity_a = int(request.GET.get('severity_a', 50))
    severity_b = int(request.GET.get('severity_b', 50))

    for shock in (shock_a, shock_b):
        if shock not in SHOCK_TYPES:
            shock_a, shock_b = 'oil', 'semiconductor'
            break

    severity_a = max(0, min(100, severity_a))
    severity_b = max(0, min(100, severity_b))

    comparison = compare_scenarios(shock_a, severity_a, shock_b, severity_b)

    context = {
        'shock_types': SHOCK_TYPES,
        'shock_a': shock_a,
        'shock_b': shock_b,
        'severity_a': severity_a,
        'severity_b': severity_b,
        'comparison': comparison,
        'comparison_json': json.dumps(comparison),
    }
    return render(request, 'intelligence/scenario_compare.html', context)


@require_GET
def api_compare(request):
    """JSON API for scenario comparison."""
    shock_a = request.GET.get('shock_a', 'oil')
    shock_b = request.GET.get('shock_b', 'semiconductor')
    severity_a = max(0, min(100, int(request.GET.get('severity_a', 50))))
    severity_b = max(0, min(100, int(request.GET.get('severity_b', 50))))

    if shock_a not in SHOCK_TYPES or shock_b not in SHOCK_TYPES:
        return JsonResponse({'error': 'Invalid shock type'}, status=400)

    return JsonResponse(compare_scenarios(shock_a, severity_a, shock_b, severity_b))


def shock_history(request):
    """Shock simulation history with trend charts."""
    shock_filter = request.GET.get('shock', 'all')
    simulations_qs = ShockSimulation.objects.all()

    if shock_filter != 'all' and shock_filter in SHOCK_TYPES:
        simulations_qs = simulations_qs.filter(shock_type=shock_filter)

    chart_data = _build_history_chart_data(simulations_qs.order_by('created_at')[:100])

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_filter': shock_filter,
        'simulations': simulations_qs.order_by('-created_at')[:20],
        'chart_json': json.dumps(chart_data),
        'total_count': simulations_qs.count(),
    }
    return render(request, 'intelligence/shock_history.html', context)


def _build_history_chart_data(simulations):
    """Build Chart.js datasets from simulation queryset."""
    sims = list(simulations)
    labels = [s.created_at.strftime('%b %d %H:%M') for s in sims]

    return {
        'labels': labels,
        'price_increase': [s.price_increase_pct for s in sims],
        'shortage_probability': [s.shortage_probability for s in sims],
        'gdp_impact': [s.gdp_impact_pct for s in sims],
        'severity': [s.severity for s in sims],
        'shock_types': [s.shock_type for s in sims],
        'colors': [SHOCK_TYPES.get(s.shock_type, {}).get('color', '#3b82f6') for s in sims],
    }


def supplier_risk(request):
    """Affected supplier risk analysis."""
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        shock_type = 'oil'
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))

    suppliers = get_affected_suppliers(shock_type, severity)
    critical_count = sum(1 for s in suppliers if s['risk_level'] == 'critical')
    high_count = sum(1 for s in suppliers if s['risk_level'] == 'high')

    context = {
        'shock_types': SHOCK_TYPES,
        'selected_shock': shock_type,
        'severity': severity,
        'suppliers': suppliers,
        'critical_count': critical_count,
        'high_count': high_count,
        'total_suppliers': len(suppliers),
    }
    return render(request, 'intelligence/supplier_risk.html', context)


@require_GET
def api_suppliers(request):
    """JSON API for affected suppliers."""
    shock_type = request.GET.get('shock', 'oil')
    severity = max(0, min(100, int(request.GET.get('severity', 50))))

    if shock_type not in SHOCK_TYPES:
        return JsonResponse({'error': 'Invalid shock type'}, status=400)

    return JsonResponse({
        'suppliers': get_affected_suppliers(shock_type, severity),
    })


def _parse_shock_params(request):
    shock_type = request.GET.get('shock', 'oil')
    if shock_type not in SHOCK_TYPES:
        raise Http404('Invalid shock type')
    severity = int(request.GET.get('severity', 50))
    severity = max(0, min(100, severity))
    return shock_type, severity


@require_GET
def export_simulation_live(request, file_format):
    """Export current simulation scenario as CSV or PDF."""
    if file_format not in ('csv', 'pdf'):
        raise Http404('Invalid export format')

    shock_type, severity = _parse_shock_params(request)
    data = build_simulation_export_data(shock_type, severity)

    if file_format == 'csv':
        return export_simulation_csv(data)
    return export_simulation_pdf(data)


@require_GET
def export_simulation_saved(request, pk, file_format):
    """Export a saved simulation record as CSV or PDF."""
    if file_format not in ('csv', 'pdf'):
        raise Http404('Invalid export format')

    simulation = get_object_or_404(ShockSimulation, pk=pk)
    impact = simulation.results_json or calculate_shock_impact(
        simulation.shock_type, simulation.severity
    )
    data = build_simulation_export_data(
        simulation.shock_type,
        simulation.severity,
        impact=impact,
        simulation_id=simulation.id,
        created_at=simulation.created_at,
    )

    if file_format == 'csv':
        return export_simulation_csv(data)
    return export_simulation_pdf(data)


@require_GET
def export_ceo_report_file(request, pk, file_format):
    """Export a CEO report as CSV or PDF."""
    if file_format not in ('csv', 'pdf'):
        raise Http404('Invalid export format')

    report = get_object_or_404(CEOReport, pk=pk)

    if file_format == 'csv':
        return export_ceo_report_csv(report)
    return export_ceo_report_pdf(report)
