from django.core.management.base import BaseCommand
from packages.models import HeroSlide, SitePageMedia


DEFAULT_SLIDES = [
    {
        'order': 1,
        'subtitle': '18 years of excellence • 4.9★ from 200+ reviews',
        'title': 'Your next holiday',
        'title_line_2': 'starts with a smile',
        'button_text': 'Plan my trip',
        'button_link': '/packages/',
        'stat_1_value': '18+',
        'stat_1_label': 'Years experience',
        'stat_2_value': '4.9★',
        'stat_2_label': 'Customer rating',
        'stat_3_value': '200+',
        'stat_3_label': 'Happy reviews',
    },
    {
        'order': 2,
        'subtitle': 'Thousands of happy travelers • Care on every journey',
        'title': 'Discover India with',
        'title_line_2': 'people who truly care',
        'button_text': 'See our holidays',
        'button_link': '/packages/',
        'stat_1_value': '50+',
        'stat_1_label': 'Destinations',
        'stat_2_value': '1000+',
        'stat_2_label': 'Tours completed',
        'stat_3_value': '5000+',
        'stat_3_label': 'Happy travelers',
    },
    {
        'order': 3,
        'subtitle': 'From college tours to family holidays • Warm local care',
        'title': 'Travel easy. Feel',
        'title_line_2': 'looked after',
        'button_text': 'Start planning',
        'button_link': '/packages/',
        'stat_1_value': '24/7',
        'stat_1_label': 'Support available',
        'stat_2_value': '100%',
        'stat_2_label': 'Personal attention',
        'stat_3_value': '15+',
        'stat_3_label': 'Travel partners',
    },
]


class Command(BaseCommand):
    help = (
        'Create Site Page Media singleton and 3 Hero Slide shells '
        '(no image uploads — templates keep static fallbacks until you upload in admin).'
    )

    def handle(self, *args, **options):
        media, created = SitePageMedia.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Site Page Media (upload images in admin)'))
        else:
            self.stdout.write('Site Page Media already exists')

        if HeroSlide.objects.exists():
            self.stdout.write(f'Hero slides already exist ({HeroSlide.objects.count()}) — skipping slide seed')
            return

        for data in DEFAULT_SLIDES:
            HeroSlide.objects.create(is_active=True, **data)
            self.stdout.write(self.style.SUCCESS(f"Created hero slide: {data['title']}"))

        self.stdout.write(self.style.SUCCESS(
            'Done. In admin: Hero Slides (upload photos) and Site Page Media '
            '(about / choose-us / breadcrumb photos). CTA Section controls the home CTA background.'
        ))
