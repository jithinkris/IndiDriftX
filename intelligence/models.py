from django.db import models


class ShockType(models.Model):
    """Supply chain shock categories."""

    SHOCK_CHOICES = [
        ('oil', 'Oil'),
        ('semiconductor', 'Semiconductor'),
        ('rare_earth', 'Rare Earth'),
    ]

    slug = models.CharField(max_length=50, choices=SHOCK_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price_impact = models.FloatField(help_text='Base price increase % at severity 50')
    base_shortage_prob = models.FloatField(help_text='Base shortage probability % at severity 50')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CountryRisk(models.Model):
    """Country-level supply chain risk profile."""

    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    risk_score = models.IntegerField(help_text='0-100 risk score')
    oil_exposure = models.FloatField(default=0)
    semiconductor_exposure = models.FloatField(default=0)
    rare_earth_exposure = models.FloatField(default=0)
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-risk_score']
        verbose_name_plural = 'Country risks'

    def __str__(self):
        return f'{self.name} ({self.risk_level})'


class SectorRecommendation(models.Model):
    """Investment recommendation by sector."""

    RECOMMENDATION_CHOICES = [
        ('BUY', 'Buy'),
        ('HOLD', 'Hold'),
        ('SELL', 'Sell'),
    ]

    sector = models.CharField(max_length=100)
    shock_type = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=10, choices=RECOMMENDATION_CHOICES)
    confidence = models.IntegerField(help_text='Confidence score 0-100')
    expected_return = models.FloatField(help_text='Expected 12-month return %')
    rationale = models.TextField()

    class Meta:
        ordering = ['sector']
        unique_together = ['sector', 'shock_type']

    def __str__(self):
        return f'{self.sector} - {self.recommendation}'


class ShockSimulation(models.Model):
    """Persisted shock simulation runs."""

    shock_type = models.CharField(max_length=50)
    severity = models.IntegerField()
    price_increase_pct = models.FloatField()
    shortage_probability = models.FloatField()
    affected_countries = models.IntegerField()
    gdp_impact_pct = models.FloatField()
    results_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.shock_type} @ {self.severity}% - {self.created_at:%Y-%m-%d %H:%M}'


class CEOReport(models.Model):
    """Generated CEO intelligence reports."""

    shock_type = models.CharField(max_length=50)
    severity = models.IntegerField()
    report_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'CEO Report: {self.shock_type} ({self.severity}%)'
