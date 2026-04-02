from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.widgets import (
    UnfoldAdminTextInputWidget,
    UnfoldAdminTextareaWidget,
    UnfoldAdminSelectWidget,
    UnfoldBooleanSwitchWidget,
)
from .models import Category, Offer, Package, PackageImage, TeamMember, SiteStats, NewsletterSubscription, CTASection, Itinerary, PackageInclusion, PackageExclusion, BlogCategory, BlogTag, Blog, BlogComment, Contact

UNFOLD_FORMFIELD_OVERRIDES = {
    models.CharField: {"widget": UnfoldAdminTextInputWidget},
    models.TextField: {"widget": UnfoldAdminTextareaWidget},
    models.BooleanField: {"widget": UnfoldBooleanSwitchWidget},
    models.ForeignKey: {"widget": UnfoldAdminSelectWidget},
}

class PackageImageInline(TabularInline):
    model = PackageImage
    extra = 1

class ItineraryInline(TabularInline):
    model = Itinerary
    extra = 1
    fields = ('day_number', 'title', 'description', 'image', 'is_active')

class PackageInclusionInline(TabularInline):
    model = PackageInclusion
    extra = 1
    fields = ('title', 'description', 'icon', 'is_highlighted', 'order', 'is_active')

class PackageExclusionInline(TabularInline):
    model = PackageExclusion
    extra = 1
    fields = ('title', 'description', 'icon', 'order', 'is_active')

@admin.register(Package)
class PackageAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'category', 'package_type', 'price', 'is_featured', 'is_popular', 'is_active')
    list_filter = ('category', 'package_type', 'is_featured', 'is_popular', 'is_active')
    search_fields = ('name', 'description', 'destinations')
    inlines = [PackageImageInline, ItineraryInline, PackageInclusionInline, PackageExclusionInline]
    
    fieldsets = (
        ('Package Details', {
            'classes': ('tab',),
            'fields': ('name', 'description', 'category', 'offer', 'package_type', 'location', 'destinations', 'cover_image')
        }),
        ('Pricing & Capacity', {
            'classes': ('tab',),
            'fields': ('price', 'duration', 'max_group_size', 'min_age')
        }),
        ('Toggles & Settings', {
            'classes': ('tab',),
            'fields': ('is_featured', 'is_popular', 'is_active')
        }),
    )

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('title', 'discount_percentage', 'is_seasonal', 'season_name', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_seasonal', 'is_active')
    search_fields = ('title', 'description')

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'position', 'experience_years', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'bio')

@admin.register(SiteStats)
class SiteStatsAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('featured_projects', 'satisfied_clients', 'years_experience', 'destinations_covered', 'tours_completed', 'updated_at')
    readonly_fields = ('updated_at',)

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(CTASection)
class CTASectionAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)

@admin.register(PackageImage)
class PackageImageAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('package', 'is_active')
    list_filter = ('is_active',)

@admin.register(Itinerary)
class ItineraryAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('package', 'day_number', 'title', 'is_active')
    list_filter = ('is_active', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'day_number')

@admin.register(PackageInclusion)
class PackageInclusionAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('package', 'title', 'is_highlighted', 'order', 'is_active')
    list_filter = ('is_active', 'is_highlighted', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'order', 'title')

@admin.register(PackageExclusion)
class PackageExclusionAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('package', 'title', 'order', 'is_active')
    list_filter = ('is_active', 'package')
    search_fields = ('title', 'description', 'package__name')
    ordering = ('package', 'order', 'title')

@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentInline(TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('name', 'email', 'comment', 'is_active')

@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('title', 'category', 'author', 'status', 'published_date', 'is_featured', 'views_count', 'is_active')
    list_filter = ('status', 'category', 'is_featured', 'is_active', 'published_date')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [BlogCommentInline]
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'classes': ('tab',),
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Classification', {
            'classes': ('tab',),
            'fields': ('category', 'tags', 'author')
        }),
        ('Publication', {
            'classes': ('tab',),
            'fields': ('status', 'is_featured', 'is_active')
        }),
        ('Statistics', {
            'classes': ('tab',),
            'fields': ('views_count', 'created_at', 'updated_at'),
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'email', 'blog', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'blog')
    search_fields = ('name', 'email', 'comment', 'blog__title')
    readonly_fields = ('created_at',)

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    formfield_overrides = UNFOLD_FORMFIELD_OVERRIDES
    list_display = ('name', 'email', 'phone', 'service', 'created_at', 'is_read', 'is_replied')
    list_filter = ('service', 'is_read', 'is_replied', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_replied')
    
    fieldsets = (
        ('Contact Information', {
            'classes': ('tab',),
            'fields': ('name', 'email', 'phone', 'service')
        }),
        ('Message', {
            'classes': ('tab',),
            'fields': ('message',)
        }),
        ('Status', {
            'classes': ('tab',),
            'fields': ('is_read', 'is_replied')
        }),
        ('Timestamps', {
            'classes': ('tab',),
            'fields': ('created_at',)
        }),
    )
