from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_seasonal = models.BooleanField(default=False)
    season_name = models.CharField(max_length=100, blank=True)  # Onam, Christmas, New Year
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Package(models.Model):
    PACKAGE_TYPE_CHOICES = [
        ('family', 'Family'),
        ('group', 'Group'),
        ('fit', 'FIT'),
        ('honeymoon', 'Honeymoon'),
        ('luxury', 'Luxury'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES, default='family')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # e.g., "5 days, 4 nights"
    location = models.CharField(max_length=200)
    destinations = models.TextField()  # e.g., "Agra, Delhi, Amritsar"
    max_group_size = models.IntegerField(null=True, blank=True)
    min_age = models.IntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='packages/')
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_offer_price(self):
        if self.offer:
            return float(self.price - (self.price * self.offer.discount_percentage / 100))
        return self.price
    
    def get_offer_percentage(self):
        if self.offer:
            return self.offer.discount_percentage
        return 0

class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.package.name + " - " + str(self.id)

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    bio = models.TextField()
    experience_years = models.IntegerField(default=0)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SiteStats(models.Model):
    featured_projects = models.IntegerField(default=0)
    luxury_houses = models.IntegerField(default=0)
    satisfied_clients = models.IntegerField(default=0)
    years_experience = models.IntegerField(default=18)
    destinations_covered = models.IntegerField(default=0)
    tours_completed = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Site Statistics - {self.updated_at.strftime('%Y-%m-%d')}"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class CTASection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.URLField()
    background_image = models.ImageField(upload_to='cta/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Itinerary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='itineraries/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_number']
        unique_together = ['package', 'day_number']

    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}: {self.title}"

class PackageInclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='inclusions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fa-check")
    is_highlighted = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.package.name} - {self.title}"

class PackageExclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='exclusions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fa-times")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.package.name} - {self.title}"

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs')
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='blogs')
    author = models.CharField(max_length=100, default='Admin')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/blog/{self.slug}/'

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.blog.title}'

class Contact(models.Model):
    SERVICE_CHOICES = [
        ('Kerala Packages', 'Kerala Packages'),
        ('North India Tours', 'North India Tours'),
        ('International Tours', 'International Tours'),
        ('Custom Packages', 'Custom Packages'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Contact from {self.name} - {self.created_at.strftime("%Y-%m-%d")}'


class InstagramPost(models.Model):
    title = models.CharField(max_length=150, blank=True, help_text="Optional label for admin / image alt text")
    image = models.ImageField(upload_to='instagram/')
    link = models.URLField(
        blank=True,
        default='https://www.instagram.com/natureholidayskerala/',
        help_text="Instagram post or profile URL opened when the icon is clicked",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Instagram Post'
        verbose_name_plural = 'Instagram Posts'

    def __str__(self):
        return self.title or f'Instagram image #{self.pk}'


class HeroSlide(models.Model):
    """Homepage hero carousel slide — image + copy managed in admin."""
    image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text='Background photo for this slide. If empty, the site uses the default static hero image.',
    )
    subtitle = models.CharField(max_length=255, blank=True)
    title = models.CharField(
        max_length=255,
        help_text='Main headline. Use a line break in the template via title_line_2 if set.',
    )
    title_line_2 = models.CharField(
        max_length=255,
        blank=True,
        help_text='Optional second line of the headline (renders under the first line).',
    )
    button_text = models.CharField(max_length=80, default='Plan my trip')
    button_link = models.CharField(
        max_length=255,
        default='/packages/',
        help_text='URL or path for the CTA button (e.g. /packages/ or a full URL).',
    )
    stat_1_value = models.CharField(max_length=40, blank=True, default='18+')
    stat_1_label = models.CharField(max_length=80, blank=True, default='Years experience')
    stat_2_value = models.CharField(max_length=40, blank=True, default='4.9★')
    stat_2_label = models.CharField(max_length=80, blank=True, default='Customer rating')
    stat_3_value = models.CharField(max_length=40, blank=True, default='200+')
    stat_3_label = models.CharField(max_length=80, blank=True, default='Happy reviews')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title or f'Hero slide #{self.pk}'


class SitePageMedia(models.Model):
    """
    Singleton row for site-wide photographic media (about, choose-us, breadcrumb).
    Decorative icons/SVGs stay in static files.
    """
    # Home about collage
    about_bg = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Background behind the home About section',
        verbose_name='Home about background',
    )
    about_main = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Primary photo in the home About collage',
        verbose_name='Home about main image',
    )
    about_secondary = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Secondary overlapping photo in the home About collage',
        verbose_name='Home about secondary image',
    )
    about_badge_title = models.CharField(
        max_length=80,
        blank=True,
        default='Care you can feel',
        help_text='Blue badge title on the home About collage',
    )
    about_badge_subtitle = models.CharField(
        max_length=120,
        blank=True,
        default='18 years of experience',
        help_text='Blue badge subtitle (e.g. years of experience)',
    )

    # Why choose us
    choose_us_bg = models.ImageField(
        upload_to='site/choose-us/',
        blank=True,
        null=True,
        help_text='Full-section background for Why Choose Us',
        verbose_name='Choose us background',
    )
    choose_us_image = models.ImageField(
        upload_to='site/choose-us/',
        blank=True,
        null=True,
        help_text='Side photograph for Why Choose Us',
        verbose_name='Choose us side image',
    )

    # About page collage
    about_page_main = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Primary photo on the About page collage',
        verbose_name='About page main image',
    )
    about_page_secondary = models.ImageField(
        upload_to='site/about/',
        blank=True,
        null=True,
        help_text='Secondary photo on the About page collage',
        verbose_name='About page secondary image',
    )

    # Shared
    breadcrumb_bg = models.ImageField(
        upload_to='site/breadcrumb/',
        blank=True,
        null=True,
        help_text='Background used on inner-page breadcrumb banners',
        verbose_name='Breadcrumb background',
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Page Media'
        verbose_name_plural = 'Site Page Media'

    def __str__(self):
        return 'Site Page Media'

    def save(self, *args, **kwargs):
        # Enforce a single row
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
