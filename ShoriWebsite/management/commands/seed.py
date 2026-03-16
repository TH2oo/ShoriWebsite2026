from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo
from ShoriWebsite.models import Team, Match

SUPERUSER = [
    ("th-sz", "dkgtheo44@gmail.com", "saez")
]

TEAMS = [
    # (name, logo_name, color)
    ("Shori", "Shori", "#971C22"),
    ("Piccolos", "Piccolos", "#741C97"),
    ("Krakens", "Krakens", "#1C2D97"),
    ("Bluestorm", "Bluestorm", "#1C2D97"),
    ("Cheetah", "Cheetah", "#FBBA22"),
    ("Decap", "Decap", "#971022"),
    ("Nova", "Nova", "#971C78"),
    ("Inaptes", "Inaptes", "#971022"),
    ("FEG", "FEG", "#97471C"),
    ("Archi", "Archi", "#1C2D97"),
    ("Aix", "Aix", "#FBBA22"),
    ("Centre", "Centre", "#FBBA22"),
    ("EtoilePolytech", "EtoilePolytech", "#1C9741"),
    ("Lettres", "Lettres", "#FBBA22"),
    ("LesMarbrés", "LesMarbrés", "#971C78"),
    ("MancheursEmpereurs", "MancheursEmpereurs", "#FBBA22"),
    ("Santé", "Santé", "#1C9741"),
]

tz = ZoneInfo("Europe/Paris")

# (date, heure, home_team, away_team, lieu)
MATCHES = [
    ("2026-03-12", "19:30", "Shori", "Nova", "Halle de Luminy"),
    ("2026-03-16", "19:30", "Shori", "Decap", "Halle de Luminy"),
    ("2026-03-26", "20:45", "Shori", "FEG", "Halle de ST Jerome"),
    ("2026-04-09", "19:30", "Shori", "Piccolos", "Halle de Luminy"),
]

class Command(BaseCommand):
    help = "Seed database with teams and sample matches"

    def handle(self, *args, **options):
        # Create superusers
        for username, email, password in SUPERUSER:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(f"  Superuser {username}: created")
            else:
                self.stdout.write(f"  Superuser {username}: exists")

        # Create teams
        team_objs = {}
        for name, logo, color in TEAMS:
            obj, created = Team.objects.update_or_create(
                name=name,
                defaults={"logo_name": logo, "color": color},
            )
            team_objs[name] = obj
            status = "created" if created else "updated"
            self.stdout.write(f"  Team {name}: {status}")

        # Create matches
        for date_str, time_str, home, away, loc in MATCHES:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            dt = dt.replace(tzinfo=tz)
            obj, created = Match.objects.get_or_create(
                datetime=dt,
                home_team=team_objs[home],
                away_team=team_objs[away],
                defaults={"location": loc},
            )
            status = "created" if created else "exists"
            self.stdout.write(f"  Match {home} vs {away} ({date_str} {time_str}): {status}")

        self.stdout.write(self.style.SUCCESS("\nSeed complete!"))
