from django.urls import path

from . import views

app_name = 'intelligence'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('simulator/', views.shock_simulator, name='shock_simulator'),
    path('simulator/run/', views.run_simulation, name='run_simulation'),
    path('simulator/export/<str:file_format>/', views.export_simulation_live, name='export_simulation_live'),
    path('simulator/export/<int:pk>/<str:file_format>/', views.export_simulation_saved, name='export_simulation_saved'),
    path('risk-map/', views.risk_map, name='risk_map'),
    path('consumer-impact/', views.consumer_impact, name='consumer_impact'),
    path('investment/', views.investment_dashboard, name='investment'),
    path('ceo-report/', views.ceo_report, name='ceo_report'),
    path('ceo-report/generate/', views.generate_ceo_report, name='generate_ceo_report'),
    path('ceo-report/export/<int:pk>/<str:file_format>/', views.export_ceo_report_file, name='export_ceo_report'),
    path('api/impact/', views.api_impact, name='api_impact'),
    path('compare/', views.scenario_compare, name='scenario_compare'),
    path('api/compare/', views.api_compare, name='api_compare'),
    path('history/', views.shock_history, name='shock_history'),
    path('suppliers/', views.supplier_risk, name='supplier_risk'),
    path('api/suppliers/', views.api_suppliers, name='api_suppliers'),
]
