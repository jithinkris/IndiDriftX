"""Export utilities for simulation and CEO report downloads."""

import csv
import io
from datetime import datetime

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .data import SHOCK_TYPES, calculate_shock_impact, get_consumer_impacts, get_sector_data


def _filename(prefix, shock_type, severity, ext):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{prefix}_{shock_type}_{severity}pct_{timestamp}.{ext}'


def _csv_response(filename, rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    for row in rows:
        writer.writerow(row)
    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _pdf_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#0f1f3d'),
        spaceAfter=12,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#1e3a6e'),
        spaceBefore=14,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name='MetaText',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=10,
    ))
    return styles


def _build_pdf_response(filename, story):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54,
    )
    doc.build(story)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _escape_pdf(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _markdown_to_pdf_paragraphs(text, styles):
    paragraphs = []
    for block in text.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        if lines[0].startswith('### '):
            paragraphs.append(Paragraph(_escape_pdf(lines[0][4:]), styles['Heading3']))
            block = '\n'.join(lines[1:]).strip()
        elif lines[0].startswith('## '):
            paragraphs.append(Paragraph(_escape_pdf(lines[0][3:]), styles['SectionHeader']))
            block = '\n'.join(lines[1:]).strip()
        elif lines[0].startswith('# '):
            paragraphs.append(Paragraph(_escape_pdf(lines[0][2:]), styles['ReportTitle']))
            block = '\n'.join(lines[1:]).strip()
        if not block:
            continue
        for line in block.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('- '):
                paragraphs.append(Paragraph(f'&bull; {_escape_pdf(line[2:])}', styles['BodyTextCustom']))
            elif line.startswith('**') and line.endswith('**'):
                paragraphs.append(Paragraph(f'<b>{_escape_pdf(line[2:-2])}</b>', styles['BodyTextCustom']))
            else:
                paragraphs.append(Paragraph(_escape_pdf(line), styles['BodyTextCustom']))
    return paragraphs


def build_simulation_export_data(shock_type, severity, impact=None, simulation_id=None, created_at=None):
    """Gather all data needed for simulation exports."""
    if impact is None:
        impact = calculate_shock_impact(shock_type, severity)
    consumer = get_consumer_impacts(shock_type, severity)
    sectors = get_sector_data(shock_type)
    shock = SHOCK_TYPES[shock_type]
    return {
        'shock_type': shock_type,
        'shock_name': shock['name'],
        'severity': severity,
        'impact': impact,
        'consumer': consumer,
        'sectors': sectors,
        'simulation_id': simulation_id,
        'created_at': created_at or datetime.now(),
    }


def export_simulation_csv(data):
    """Export simulation results as CSV."""
    impact = data['impact']
    filename = _filename('simulation', data['shock_type'], data['severity'], 'csv')
    rows = [
        ['Global Supply Chain Shock Intelligence — Simulation Export'],
        ['Generated', data['created_at'].strftime('%Y-%m-%d %H:%M:%S')],
        [],
        ['Scenario Summary'],
        ['Shock Type', data['shock_name']],
        ['Severity (%)', data['severity']],
        ['Price Increase (%)', impact['price_increase_pct']],
        ['Shortage Probability (%)', impact['shortage_probability']],
        ['GDP Impact (%)', impact['gdp_impact_pct']],
        ['Affected Countries', impact['affected_count']],
    ]
    if data.get('simulation_id'):
        rows.append(['Simulation ID', data['simulation_id']])

    rows.extend([[], ['Affected Countries'], ['Country', 'Impact Score (%)', 'Risk Level']])
    for country in impact.get('affected_countries', []):
        rows.append([country['name'], country['impact'], country['risk_level']])

    rows.extend([[], ['Shock Timeline'], ['Phase', 'Label', 'Description']])
    for phase in impact.get('timeline', []):
        rows.append([phase['phase'], phase['label'], phase['description']])

    rows.extend([[], ['Consumer Impact'], ['Product', 'Category', 'Price Increase (%)', 'Shortage Probability (%)']])
    for item in data['consumer']:
        rows.append([item['product'], item['category'], item['price_increase'], item['shortage_probability']])

    rows.extend([[], ['Investment Recommendations'], ['Sector', 'Recommendation', 'Confidence (%)', 'Expected Return (%)', 'Rationale']])
    for sector in data['sectors']:
        rows.append([
            sector['sector'],
            sector['recommendation'],
            sector['confidence'],
            sector['expected_return'],
            sector['rationale'],
        ])

    return _csv_response(filename, rows)


def export_simulation_pdf(data):
    """Export simulation results as PDF."""
    impact = data['impact']
    styles = _pdf_styles()
    filename = _filename('simulation', data['shock_type'], data['severity'], 'pdf')
    story = [
        Paragraph('Supply Chain Shock Simulation Report', styles['ReportTitle']),
        Paragraph(
            f'{_escape_pdf(data["shock_name"])} &mdash; Severity {data["severity"]}%',
            styles['MetaText'],
        ),
        Paragraph(
            f'Generated: {data["created_at"].strftime("%Y-%m-%d %H:%M:%S")}',
            styles['MetaText'],
        ),
        Spacer(1, 0.2 * inch),
    ]

    summary_data = [
        ['Metric', 'Value'],
        ['Price Increase', f'+{impact["price_increase_pct"]}%'],
        ['Shortage Probability', f'{impact["shortage_probability"]}%'],
        ['GDP Impact', f'{impact["gdp_impact_pct"]}%'],
        ['Countries Affected', str(impact['affected_count'])],
    ]
    summary_table = Table(summary_data, colWidths=[2.5 * inch, 3.5 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a6e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f1f5f9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.extend([
        Paragraph('Key Metrics', styles['SectionHeader']),
        summary_table,
        Spacer(1, 0.15 * inch),
    ])

    if impact.get('affected_countries'):
        country_data = [['Country', 'Impact (%)', 'Risk Level']]
        for country in impact['affected_countries']:
            country_data.append([country['name'], str(country['impact']), country['risk_level'].title()])
        country_table = Table(country_data, colWidths=[2.5 * inch, 1.5 * inch, 2 * inch])
        country_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a6e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.extend([
            Paragraph('Most Affected Countries', styles['SectionHeader']),
            country_table,
            Spacer(1, 0.15 * inch),
        ])

    story.append(Paragraph('Consumer Impact', styles['SectionHeader']))
    consumer_data = [['Product', 'Category', 'Price ↑', 'Shortage %']]
    for item in data['consumer']:
        consumer_data.append([
            item['product'],
            item['category'],
            f'+{item["price_increase"]}%',
            f'{item["shortage_probability"]}%',
        ])
    consumer_table = Table(consumer_data, colWidths=[1.8 * inch, 1.5 * inch, 1 * inch, 1 * inch])
    consumer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a6e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.extend([consumer_table, Spacer(1, 0.15 * inch)])

    story.append(Paragraph('Investment Recommendations', styles['SectionHeader']))
    sector_data = [['Sector', 'Signal', 'Confidence', 'Return']]
    for sector in data['sectors']:
        sector_data.append([
            sector['sector'],
            sector['recommendation'],
            f'{sector["confidence"]}%',
            f'{sector["expected_return"]:+.1f}%',
        ])
    sector_table = Table(sector_data, colWidths=[2.2 * inch, 1 * inch, 1.2 * inch, 1.1 * inch])
    sector_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a6e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(sector_table)

    return _build_pdf_response(filename, story)


def export_ceo_report_csv(report):
    """Export CEO report as CSV."""
    filename = _filename('ceo_report', report.shock_type, report.severity, 'csv')
    rows = [
        ['Global Supply Chain Shock Intelligence — CEO Report Export'],
        ['Report ID', report.id],
        ['Shock Type', report.shock_type.replace('_', ' ').title()],
        ['Severity (%)', report.severity],
        ['Generated', report.created_at.strftime('%Y-%m-%d %H:%M:%S')],
        [],
        ['Report Content'],
        [report.report_content],
    ]
    return _csv_response(filename, rows)


def export_ceo_report_pdf(report):
    """Export CEO report as PDF."""
    styles = _pdf_styles()
    filename = _filename('ceo_report', report.shock_type, report.severity, 'pdf')
    story = [
        Paragraph('Executive Intelligence Report', styles['ReportTitle']),
        Paragraph(
            f'{_escape_pdf(report.shock_type.replace("_", " ").title())} '
            f'&mdash; Severity {report.severity}%',
            styles['MetaText'],
        ),
        Paragraph(
            f'Report #{report.id} &bull; Generated {report.created_at.strftime("%Y-%m-%d %H:%M:%S")}',
            styles['MetaText'],
        ),
        Spacer(1, 0.25 * inch),
    ]
    story.extend(_markdown_to_pdf_paragraphs(report.report_content, styles))
    return _build_pdf_response(filename, story)
