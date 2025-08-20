from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Max
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Package, Category, Offer, TeamMember, SiteStats, Itinerary, BlogCategory, BlogTag, Blog, BlogComment, Contact

def home(request):
    """Home page view with dynamic content"""
    # Get featured packages for hero slider
    featured_packages = Package.objects.filter(
        is_active=True, 
        is_featured=True
    )[:3]
    
    # Get popular packages for destination section
    popular_packages = Package.objects.filter(
        is_active=True,
        is_popular=True
    )[:8]
    
    # Get all categories with package counts
    categories = Category.objects.filter(is_active=True)
    for category in categories:
        category.package_count = Package.objects.filter(
            category=category, 
            is_active=True
        ).count()
    
    # Get active offers - show the one with highest discount first
    active_offers = Offer.objects.filter(
        is_active=True
    ).order_by('-discount_percentage', 'valid_to')[:3]
    
    # Calculate highest discount percentage
    highest_discount = 0
    if active_offers.exists():
        highest_discount = active_offers.aggregate(
            max_discount=Max('discount_percentage')
        )['max_discount'] or 0
    
    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    
    # Get site statistics
    try:
        site_stats = SiteStats.objects.first()
    except:
        site_stats = None
    
    context = {
        'featured_packages': featured_packages,
        'popular_packages': popular_packages,
        'categories': categories,
        'active_offers': active_offers,
        'highest_discount': highest_discount,
        'team_members': team_members,
        'site_stats': site_stats,
    }
    return render(request, 'index.html', context)

class PackageListView(ListView):
    model = Package
    template_name = 'packages.html'
    context_object_name = 'packages'
    paginate_by =8
    
    def get_queryset(self):
        queryset = Package.objects.filter(is_active=True)
        
        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by package type
        package_type = self.request.GET.get('type')
        if package_type:
            queryset = queryset.filter(package_type=package_type)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(destinations__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['package_types'] = Package.PACKAGE_TYPE_CHOICES
        return context

class PackageDetailView(DetailView):
    model = Package
    template_name = 'package_details.html'
    context_object_name = 'package'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_packages'] = Package.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        context['package_images'] = self.object.packageimage_set.filter(is_active=True)
        context['itineraries'] = self.object.itineraries.filter(is_active=True)
        context['inclusions'] = self.object.inclusions.filter(is_active=True)
        context['exclusions'] = self.object.exclusions.filter(is_active=True)
        return context

def search_packages(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    package_type = request.GET.get('type', '')
    
    packages = Package.objects.filter(is_active=True)
    
    if query:
        packages = packages.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(destinations__icontains=query) |
            Q(location__icontains=query)
        )
    
    if category:
        packages = packages.filter(category_id=category)
    
    if package_type:
        packages = packages.filter(package_type=package_type)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'packages': packages,
        'categories': categories,
        'package_types': Package.PACKAGE_TYPE_CHOICES,
        'query': query,
        'selected_category': category,
        'selected_type': package_type,
    }
    
    return render(request, 'packages/search_results.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    """Contact page with form submission handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        service = request.POST.get('service', '')
        message = request.POST.get('message')
        
        if name and email and message:
            # Save contact to database
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                service=service,
                message=message
            )
            
            # Send email notification to admin
            try:
                # Email to admin using HTML template
                admin_subject = f'New Contact Form Submission from {name}'
                admin_html_message = render_to_string('emails/contact_notification.html', {
                    'contact': contact
                })
                
                admin_email = EmailMessage(
                    subject=admin_subject,
                    body=admin_html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@natureholidays.com']
                )
                admin_email.content_subtype = "html"
                admin_email.send()
                
                # Email confirmation to customer using HTML template
                customer_subject = 'Thank you for contacting Nature Holidays'
                customer_html_message = render_to_string('emails/contact_confirmation.html', {
                    'contact': contact
                })
                
                customer_email = EmailMessage(
                    subject=customer_subject,
                    body=customer_html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                customer_email.content_subtype = "html"
                customer_email.send()
                
                return JsonResponse({'success': True})
                
            except Exception as e:
                # If email fails, still save the contact but log the error
                print(f"Email sending failed: {e}")
                return JsonResponse({'success': True, 'email_error': 'Message saved but email notification failed'})
        else:
            return JsonResponse({'success': False, 'error': 'Please fill all required fields'})
    
    return render(request, 'contact.html')

def blog(request):
    """Blog listing page with search and filtering"""
    blogs = Blog.objects.filter(status='published', is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    
    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = BlogCategory.objects.filter(is_active=True)
    recent_blogs = Blog.objects.filter(status='published', is_active=True)[:3]
    popular_tags = BlogTag.objects.filter(is_active=True, blogs__isnull=False).distinct()[:10]
    
    context = {
        'page_obj': page_obj,
        'blogs': page_obj,
        'categories': categories,
        'recent_blogs': recent_blogs,
        'popular_tags': popular_tags,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    """Blog detail page with comments"""
    blog = get_object_or_404(Blog, slug=slug, status='published', is_active=True)
    
    # Get related blogs
    related_blogs = Blog.objects.filter(
        category=blog.category,
        status='published',
        is_active=True
    ).exclude(id=blog.id)[:3]
    
    # Get comments
    comments = blog.comments.filter(is_active=True)
    categories = BlogCategory.objects.filter(is_active=True)
    
    # Handle comment submission
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_text = request.POST.get('message')
        
        if name and email and comment_text:
            BlogComment.objects.create(
                blog=blog,
                name=name,
                email=email,
                comment=comment_text
            )
            return JsonResponse({'success': True})
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
        'comments': comments,       
        'categories': categories,
    }
    return render(request, 'blog_detail.html', context)