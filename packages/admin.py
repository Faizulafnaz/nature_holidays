from django.contrib import admin
from .models import Category, Offer, Package, PackageImage, TeamMember, SiteStats, NewsletterSubscription, CTASection, Itinerary, PackageInclusion, PackageExclusion, BlogCategory, BlogTag, Blog, BlogComment, Contact

class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1

class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1
    fields = ('day_number', 'title', 'description', 'image', 'is_active')

class PackageInclusionInline(admin.TabularInline):
    model = PackageInclusion
    extra = 1
    fields = ('title', 'description', 'icon', 'is_highlighted', 'order', 'is_active')

class PackageExclusionInline(admin.TabularInline):
    model = PackageExclusion
    extra = 1
    fields = ('title', 'description', 'icon', 'order', 'is_active')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'package_type', 'price', 'is_featured', 'is_popular', 'is_active')
    list_filter = ('category', 'package_type', 'is_featured', 'is_popular', 'is_active')
    search_fields = ('name', 'description', 'destinations')
    inlines = [PackageImageInline, ItineraryInline, PackageInclusionInline, PackageExclusionInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_percentage', 'is_seasonal', 'season_name', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_seasonal', 'is_active')
    search_fields = ('title', 'description')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'experience_years', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'bio')

@admin.register(SiteStats)
class SiteStatsAdmin(admin.ModelAdmin):
    list_display = ('featured_projects', 'satisfied_clients', 'years_experience', 'destinations_covered', 'tours_completed', 'updated_at')
    readonly_fields = ('updated_at',)

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(CTASection)
class CTASectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'is_active')
    list_filter = ('is_active',)

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('package', 'day_number', 'title', 'is_active')
    list_filter = ('is_active', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'day_number')

@admin.register(PackageInclusion)
class PackageInclusionAdmin(admin.ModelAdmin):
    list_display = ('package', 'title', 'is_highlighted', 'order', 'is_active')
    list_filter = ('is_active', 'is_highlighted', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'order', 'title')

@admin.register(PackageExclusion)
class PackageExclusionAdmin(admin.ModelAdmin):
    list_display = ('package', 'title', 'order', 'is_active')
    list_filter = ('is_active', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'order', 'title')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('name', 'email', 'comment', 'is_active')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'published_date', 'is_featured', 'views_count', 'is_active')
    list_filter = ('status', 'category', 'is_featured', 'is_active', 'published_date')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [BlogCommentInline]
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Publication', {
            'fields': ('status', 'is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'blog')
    search_fields = ('name', 'email', 'comment', 'blog__title')
    readonly_fields = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'service', 'created_at', 'is_read', 'is_replied')
    list_filter = ('service', 'is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_replied')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'service')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
