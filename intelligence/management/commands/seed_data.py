from django.core.management.base import BaseCommand

from intelligence.data import COUNTRIES, SECTOR_RECOMMENDATIONS, SHOCK_TYPES
from intelligence.models import CountryRisk, SectorRecommendation, ShockType


class Command(BaseCommand):
    help = 'Seed hardcoded supply chain impact data into the database'

    def handle(self, *args, **options):
        for slug, data in SHOCK_TYPES.items():
            ShockType.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'description': data['description'],
                    'base_price_impact': data['base_price_impact'],
                    'base_shortage_prob': data['base_shortage_prob'],
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(SHOCK_TYPES)} shock types'))

        for country in COUNTRIES:
            CountryRisk.objects.update_or_create(
                code=country['code'],
                defaults={
                    'name': country['name'],
                    'latitude': country['lat'],
                    'longitude': country['lng'],
                    'risk_level': country['risk_level'],
                    'risk_score': country['risk_score'],
                    'oil_exposure': country['oil_exposure'],
                    'semiconductor_exposure': country['semiconductor_exposure'],
                    'rare_earth_exposure': country['rare_earth_exposure'],
                    'summary': country['summary'],
                },
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(COUNTRIES)} countries'))

        count = 0
        for shock_type, sectors in SECTOR_RECOMMENDATIONS.items():
            for sector in sectors:
                SectorRecommendation.objects.update_or_create(
                    sector=sector['sector'],
                    shock_type=shock_type,
                    defaults={
                        'recommendation': sector['recommendation'],
                        'confidence': sector['confidence'],
                        'expected_return': sector['expected_return'],
                        'rationale': sector['rationale'],
                    },
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {count} sector recommendations'))
