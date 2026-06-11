from django.contrib import admin

from .models import CEOReport, CountryRisk, SectorRecommendation, ShockSimulation, ShockType


@admin.register(ShockType)
class ShockTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'base_price_impact', 'base_shortage_prob']


@admin.register(CountryRisk)
class CountryRiskAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'risk_level', 'risk_score']
    list_filter = ['risk_level']


@admin.register(SectorRecommendation)
class SectorRecommendationAdmin(admin.ModelAdmin):
    list_display = ['sector', 'shock_type', 'recommendation', 'confidence', 'expected_return']
    list_filter = ['shock_type', 'recommendation']


@admin.register(ShockSimulation)
class ShockSimulationAdmin(admin.ModelAdmin):
    list_display = ['shock_type', 'severity', 'price_increase_pct', 'shortage_probability', 'created_at']
    list_filter = ['shock_type']


@admin.register(CEOReport)
class CEOReportAdmin(admin.ModelAdmin):
    list_display = ['shock_type', 'severity', 'created_at']
