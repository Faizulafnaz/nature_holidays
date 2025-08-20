# Nature Holidays - Travel & Tourism Website

A comprehensive travel and tourism website built with Django, featuring package management, blog system, contact forms, and email notifications.

## 🌟 Features

### Core Features
- **Package Management**: Create and manage travel packages with categories, offers, and detailed information
- **Dynamic Content**: Hero sliders, featured packages, team members, and site statistics
- **Blog System**: Complete blog with categories, tags, comments, and search functionality
- **Contact System**: Contact forms with email notifications to admin and customer confirmations
- **Admin Panel**: Comprehensive Django admin with inline editing for related objects
- **Responsive Design**: Mobile-friendly templates with modern UI/UX

### Travel Packages
- **8 Package Categories**: Kerala, North India, International, Wayanad Special, Beach Holidays, Cultural Tours, Adventure, Luxury
- **Package Details**: Itineraries, inclusions/exclusions, pricing, duration, group size, age restrictions
- **Offers & Discounts**: Seasonal offers (Onam, Christmas), group discounts, early bird specials
- **Search & Filter**: Package search by location, category, price range, and package type

### Content Management
- **Team Members**: Professional team profiles with social media links
- **Site Statistics**: Dynamic counters for tours, clients, experience, and destinations
- **Newsletter System**: Email subscription management
- **CTA Sections**: Call-to-action sections for lead generation

## ⚙️ Settings Configuration

### How Settings Work

The project uses a **smart settings system** that automatically switches between development and production configurations:

1. **Main Settings** (`settings.py`): Contains all common settings and development defaults
2. **Production Settings** (`settings_production.py`): Contains only production-specific overrides
3. **Environment Variable**: `DJANGO_ENV` controls which settings are used

### Settings Flow

```
settings.py (main file)
    ↓
Checks DJANGO_ENV environment variable
    ↓
If DJANGO_ENV=production:
    → Imports settings_production.py
    → Overrides development settings with production values
If DJANGO_ENV=development (or not set):
    → Uses development settings (SQLite, local files, etc.)
```

### Environment Variables

Create a `.env` file in your project root:

```bash
# Development (.env file)
DJANGO_ENV=development
SECRET_KEY=your-dev-secret-key
DEBUG=True

# Production (Render environment variables)
DJANGO_ENV=production
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://...
```

## 🚀 Deployment on Render

### Prerequisites
- Render account (free tier available)
- Cloudinary account for media storage
- Gmail account for email functionality

### Step 1: Prepare Your Project

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Populate Sample Data**
   ```bash
   python manage.py populate_sample_data
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Step 2: Render Setup

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `nature-holidays` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn nature_holidays.wsgi:application`

3. **Environment Variables**
   Add these environment variables in Render:
   ```
   DJANGO_ENV=production
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=your-postgresql-url-from-render
   CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
   CLOUDINARY_API_KEY=your-cloudinary-api-key
   CLOUDINARY_API_SECRET=your-cloudinary-api-secret
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   DEFAULT_FROM_EMAIL=Nature Holidays <info@natureholidays.com>
   ADMIN_EMAIL=admin@natureholidays.com
   ```

### Step 3: Database Setup

1. **Create PostgreSQL Database**
   - In Render Dashboard, go to "New +" → "PostgreSQL"
   - Choose free tier
   - Copy the database URL

2. **Update Environment Variables**
   - Set `DATABASE_URL` to your PostgreSQL connection string

### Step 4: Cloudinary Setup

1. **Create Cloudinary Account**
   - Sign up at [Cloudinary](https://cloudinary.com/)
   - Get your cloud name, API key, and secret

2. **Update Environment Variables**
   - Set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

### Step 5: Email Setup (Gmail)

1. **Enable 2-Factor Authentication**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to Google Account → Security → App Passwords
   - Generate password for "Mail"
   - Use this password as `EMAIL_HOST_PASSWORD`

### Step 6: Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Monitor Deployment**
   - Render will automatically build and deploy
   - Check build logs for any errors
   - Your site will be available at `https://your-app-name.onrender.com`

## 📁 Project Structure

```
nature-holidays/
├── packages/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── admin.py             # Admin interface
│   ├── urls.py              # URL routing
│   └── management/          # Management commands
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── packages.html        # Package listing
│   ├── package_details.html # Package details
│   ├── blog.html            # Blog listing
│   ├── blog_detail.html     # Blog details
│   ├── contact.html         # Contact page
│   └── emails/              # Email templates
├── static/                   # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript
│   └── img/                 # Images
├── nature_holidays/          # Project settings
│   ├── settings.py          # Main settings (development + production logic)
│   ├── settings_production.py # Production overrides only
│   ├── urls.py              # Main URL config
│   └── wsgi.py              # WSGI config
├── requirements.txt          # Python dependencies
├── build.sh                 # Render build script
├── env_template.txt         # Environment variables template
└── README.md                # This file
```

## 🗄️ Database Models

### Core Models
- **Category**: Travel package categories
- **Package**: Main travel packages with details
- **Offer**: Discounts and special offers
- **TeamMember**: Company team information
- **SiteStats**: Website statistics and counters

### Package Details
- **PackageImage**: Multiple images per package
- **Itinerary**: Day-wise tour plans
- **PackageInclusion**: What's included in packages
- **PackageExclusion**: What's not included

### Blog System
- **BlogCategory**: Blog post categories
- **BlogTag**: Blog post tags
- **Blog**: Blog posts with content
- **BlogComment**: User comments on blog posts

### Communication
- **Contact**: Contact form submissions
- **NewsletterSubscription**: Email subscriptions
- **CTASection**: Call-to-action sections

## 🎨 Frontend Features

### Templates
- **Responsive Design**: Mobile-first approach
- **Modern UI**: Clean, professional travel website design
- **Dynamic Content**: All content pulled from database
- **Interactive Elements**: Hero sliders, contact forms, search functionality

### CSS & JavaScript
- **Bootstrap**: Responsive framework
- **Custom CSS**: Offers, inclusions/exclusions styling
- **JavaScript**: Hero slider, sticky elements, form handling

## 📧 Email System

### Email Templates
- **Admin Notifications**: Professional contact form notifications
- **Customer Confirmations**: Welcome emails with company information
- **HTML Formatting**: Beautiful, branded email templates

### Email Features
- **SMTP Configuration**: Gmail SMTP support
- **Error Handling**: Graceful failure handling
- **Template Rendering**: Dynamic content in emails

## 🔧 Management Commands

### populate_sample_data
```bash
python manage.py populate_sample_data
```
Creates comprehensive sample data for all models:
- 8 Package Categories
- 4 Special Offers
- 8 Travel Packages
- 4 Team Members
- 4 Blog Posts with Comments
- 5 Contact Messages
- Complete package details (itineraries, inclusions/exclusions)

## 🚀 Performance & Security

### Production Optimizations
- **Static Files**: Whitenoise for efficient static file serving
- **Database**: PostgreSQL with connection pooling
- **Security**: HTTPS, HSTS, XSS protection, CSRF protection
- **Logging**: Comprehensive logging configuration

### Render Free Tier Considerations
- **Build Time**: 15 minutes limit
- **Sleep Mode**: Service sleeps after 15 minutes of inactivity
- **Database**: 1GB PostgreSQL storage
- **Bandwidth**: 750GB/month

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Render dashboard
   - Verify requirements.txt dependencies
   - Ensure build.sh has execute permissions

2. **Database Connection**
   - Verify DATABASE_URL environment variable
   - Check PostgreSQL service status
   - Ensure database is accessible

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATICFILES_DIRS
   - Verify whitenoise configuration

4. **Email Not Working**
   - Check Gmail app password
   - Verify SMTP settings
   - Check environment variables

5. **Settings Not Working**
   - Verify `DJANGO_ENV` environment variable
   - Check if `.env` file exists and is readable
   - Ensure environment variables are set in Render

### Debug Mode
For debugging, temporarily set `DEBUG=True` in production settings (not recommended for live sites).

## 📱 Mobile Optimization

- **Responsive Design**: All templates are mobile-friendly
- **Touch-Friendly**: Optimized for touch devices
- **Fast Loading**: Optimized images and assets
- **SEO Ready**: Meta tags and structured data

## 🔍 SEO Features

- **Meta Tags**: Dynamic title and description
- **Structured Data**: Proper HTML semantics
- **URL Structure**: Clean, SEO-friendly URLs
- **Image Optimization**: Alt tags and proper sizing

## 📊 Analytics Ready

- **Google Analytics**: Easy to integrate
- **Conversion Tracking**: Contact form tracking
- **Performance Monitoring**: Built-in logging
- **User Behavior**: Page views and interactions

## 🎯 Future Enhancements

- **Booking System**: Online package booking
- **Payment Integration**: Stripe/PayPal integration
- **Multi-language**: International language support
- **API Development**: REST API for mobile apps
- **Advanced Search**: Elasticsearch integration
- **Real-time Chat**: Customer support chat

## 📞 Support

For deployment support or questions:
- Check Render documentation
- Review Django deployment guides
- Check build logs for specific errors

## 📄 License

This project is for Nature Holidays travel company. All rights reserved.

---

**Ready to deploy?** 🚀 Your Nature Holidays website is now fully prepared for Render hosting with comprehensive sample data and production-ready configuration!
