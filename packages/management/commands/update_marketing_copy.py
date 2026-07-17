from django.core.management.base import BaseCommand

from packages.models import Category, Offer, Package, CTASection


# Experience-focused descriptions keyed by common package name fragments (case-insensitive contains).
PACKAGE_COPY = [
    (
        ["leh", "ladakh"],
        "Wake among snow-dusted peaks, ride high mountain roads, and watch clear night skies over Ladakh. A journey for travelers ready for altitude, silence, and unforgettable views.",
    ),
    (
        ["agra", "delhi", "amritsar"],
        "Stand before the Taj at soft light, feel Delhi's living history, and share quiet moments at the Golden Temple. A North India path made warm and easy for families.",
    ),
    (
        ["srinagar"],
        "Drift on Dal Lake at dusk, walk through chinar shade, and breathe cool mountain air. Srinagar for couples and families who want calm days and gentle beauty.",
    ),
    (
        ["nepal"],
        "Feel temple bells in Kathmandu, watch Himalayan light change, and meet warm local hospitality. Nepal for travelers seeking culture, nature, and quiet wonder.",
    ),
    (
        ["hyderabad"],
        "Taste Hyderabad's famous flavours, wander old bazaars, and see lakeside evenings glow. A short city break for families and friends who love food and history.",
    ),
    (
        ["andaman"],
        "Swim clear turquoise water, walk soft island beaches, and watch sunsets over the Bay of Bengal. Andaman for honeymooners and families seeking sea and stillness.",
    ),
    (
        ["thailand"],
        "Island-hop turquoise waters, walk soft beaches at dusk, and savor Thai street food. A warm, easy holiday for honeymooners and friends who love sea and sun.",
    ),
    (
        ["bhutan"],
        "Walk quiet monastery paths, watch prayer flags against blue sky, and feel the calm of the hills. Bhutan for travelers seeking peace, culture, and clear mountain air.",
    ),
    (
        ["backwater", "ayurveda"],
        "Drift through Kerala's quiet canals on a houseboat, taste home-style meals, and unwind with gentle Ayurvedic care. A calm escape for couples and families who want rest more than rush.",
    ),
    (
        ["golden triangle"],
        "Watch sunrise at the Taj, stroll Jaipur's courtyards, and feel Delhi's layered history. A classic North India journey made easy for families and first-time visitors.",
    ),
    (
        ["wayanad"],
        "Wake to mist over the hills, trek Chembra, watch wildlife, and stand inside Edakkal's ancient caves. A Wayanad holiday planned by people who live these roads.",
    ),
    (
        ["goa"],
        "Spend mornings by the sea, afternoons in Old Goa's quiet churches, and evenings at an easy pace. Goa for families and friends who want sun without stress.",
    ),
    (
        ["rajasthan"],
        "Walk sandstone forts at golden hour, ride into quiet dunes, and listen to folk music under desert skies. Rajasthan for travelers who love stories and space.",
    ),
    (
        ["dubai"],
        "Watch the city glitter from above, wander spice-scented souks, and feel the desert cool at dusk. Dubai made simple for families and first-time visitors.",
    ),
    (
        ["munnar", "hill station"],
        "Walk between tea bushes in Munnar, spot wildlife near Thekkady, and breathe in Vagamon's open meadows. Cool hill days for families who love green views.",
    ),
    (
        ["phuket", "krabi"],
        "Island-hop turquoise waters, walk soft beaches at dusk, and savor Thai street food. A warm, easy holiday for honeymooners and friends who love sea and sun.",
    ),
]

OFFER_COPY = {
    "Onam Special Discount": "Celebrate Onam with warmer rates on Kerala holidays. A lovely season for backwaters, hills, and family time together.",
    "Christmas & New Year Special": "Welcome the new year somewhere beautiful. Book early for festive-season holidays and keep more for the memories.",
    "Group Booking Discount": "Traveling with 10 or more? Enjoy group-friendly rates suited to reunions, college tours, and office getaways.",
    "Early Bird Discount": "Plan three months ahead and enjoy early-bird savings — more time to look forward to your holiday.",
}

CATEGORY_COPY = {
    "Kerala Packages": "Cruise quiet backwaters, walk tea hills, and unwind on Kerala beaches — holidays shaped for families and slow travelers.",
    "North India Tours": "Stand before the Taj, wander old bazaars, and feel North India's stories unfold on journeys made for first-timers and families.",
    "International Tours": "Beach days in Thailand, city lights in Dubai, and carefully planned international trips without the stress of arranging it all alone.",
    "Wayanad Special": "Wake up to misty hills, walk spice trails, and discover waterfalls near home — Wayanad holidays planned by locals who know every turn.",
    "Beach Holidays": "Soft sand, easy mornings, and seaside evenings — beach holidays for couples, friends, and families who want to slow down.",
    "Cultural Tours": "Walk through forts, temples, and living traditions — cultural trips that help you feel India's history, not just photograph it.",
    "Adventure Tours": "Trek green trails, camp under clear skies, and try outdoor adventures paced for beginners and seasoned explorers alike.",
    "Luxury Escapes": "Quieter stays, thoughtful pacing, and personal attention — holidays for travelers who want comfort without the fuss.",
}


class Command(BaseCommand):
    help = (
        "Update package, offer, category, and CTA marketing copy to the warmer "
        "Nature Holidays voice without changing layout or schema."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without saving.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated_packages = 0
        updated_offers = 0
        updated_categories = 0
        updated_ctas = 0

        for package in Package.objects.all():
            name_l = package.name.lower().replace("–", "-").replace("—", "-")
            new_desc = None
            best_score = 0
            for keywords, description in PACKAGE_COPY:
                if all(k in name_l for k in keywords):
                    score = len(keywords)
                    if score > best_score:
                        best_score = score
                        new_desc = description
            if new_desc and package.description != new_desc:
                self.stdout.write(f"Package: {package.name}")
                if not dry_run:
                    package.description = new_desc
                    package.save(update_fields=["description", "updated_at"])
                updated_packages += 1

        for title, description in OFFER_COPY.items():
            qs = Offer.objects.filter(title=title)
            for offer in qs:
                if offer.description != description:
                    self.stdout.write(f"Offer: {offer.title}")
                    if not dry_run:
                        offer.description = description
                        offer.save(update_fields=["description"])
                    updated_offers += 1

        for name, description in CATEGORY_COPY.items():
            qs = Category.objects.filter(name=name)
            for category in qs:
                if category.description != description:
                    self.stdout.write(f"Category: {category.name}")
                    if not dry_run:
                        category.description = description
                        category.save(update_fields=["description"])
                    updated_categories += 1

        for cta in CTASection.objects.all():
            changed = False
            if "Adventure" in cta.title or cta.title == "Ready to Start Your Adventure?":
                if cta.title != "Ready to Plan Your Holiday?":
                    cta.title = "Ready to Plan Your Holiday?"
                    changed = True
                if cta.subtitle != "We are here when you are ready":
                    cta.subtitle = "We are here when you are ready"
                    changed = True
                new_desc = (
                    "Tell us who is traveling and what you hope to feel. "
                    "Our Wayanad team will shape a clear, warm holiday plan around you."
                )
                if cta.description != new_desc:
                    cta.description = new_desc
                    changed = True
                if cta.button_text != "Start Planning":
                    cta.button_text = "Start Planning"
                    changed = True
            if changed:
                self.stdout.write(f"CTA: {cta.title}")
                if not dry_run:
                    cta.save()
                updated_ctas += 1

        mode = "Would update" if dry_run else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{mode} {updated_packages} packages, {updated_offers} offers, "
                f"{updated_categories} categories, {updated_ctas} CTAs."
            )
        )
