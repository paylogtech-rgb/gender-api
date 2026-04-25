import json
from django.core.management.base import BaseCommand
from api.models import Profile

class Command(BaseCommand):
    help = "Seed profiles data"

    def handle(self, *args, **kwargs):
        with open('seed_profiles.json', encoding='utf-8') as f:
            data = json.load(f)

        profiles = data.get("profiles", [])

        for item in profiles:
            Profile.objects.update_or_create(
                name=item["name"],  # prevents duplicates
                defaults={
                    "gender": item["gender"],
                    "gender_probability": item["gender_probability"],
                    "age": item["age"],
                    "age_group": item["age_group"],
                    "country_id": item["country_id"],
                    "country_name": item["country_name"],
                    "country_probability": item["country_probability"],
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete"))