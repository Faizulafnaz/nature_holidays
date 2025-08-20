from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from packages.models import (
    Category, Offer, Package, PackageImage, TeamMember, SiteStats, 
    NewsletterSubscription, CTASection, Itinerary, PackageInclusion, 
    PackageExclusion, BlogCategory, BlogTag, Blog, BlogComment, Contact
)

class Command(BaseCommand):
    help = 'Populate database with comprehensive sample data for Nature Holidays'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive sample data for Nature Holidays...')
        
        # Create Categories
        categories_data = [
            {
                'name': 'Kerala Packages',
                'description': 'Explore the beauty of God\'s Own Country with our curated Kerala packages including backwaters, hill stations, and beaches.'
            },
            {
                'name': 'North India Tours',
                'description': 'Discover the rich cultural heritage of North India with our Golden Triangle and beyond packages.'
            },
            {
                'name': 'International Tours',
                'description': 'Experience world-class destinations with our international tour packages to Thailand, Dubai, and more.'
            },
            {
                'name': 'Wayanad Special',
                'description': 'Exclusive packages to explore the pristine beauty of Wayanad, Kerala\'s hidden gem.'
            },
            {
                'name': 'Beach Holidays',
                'description': 'Relaxing beach getaways to pristine coastal destinations in India and abroad.'
            },
            {
                'name': 'Cultural Tours',
                'description': 'Explore rich cultural heritage and historical monuments across India.'
            },
            {
                'name': 'Adventure Tours',
                'description': 'Thrilling adventure experiences including trekking, camping, and outdoor activities.'
            },
            {
                'name': 'Luxury Escapes',
                'description': 'Premium travel experiences with luxury accommodations and personalized service.'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create Offers
        offers_data = [
            {
                'title': 'Onam Special Discount',
                'description': 'Celebrate Onam with special discounts on Kerala packages. Perfect time to explore God\'s Own Country!',
                'discount_percentage': 15.00,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=30),
                'is_seasonal': True,
                'season_name': 'Onam'
            },
            {
                'title': 'Christmas & New Year Special',
                'description': 'Ring in the new year with amazing travel deals. Book early and save big on your dream vacation!',
                'discount_percentage': 20.00,
                'valid_from': timezone.now() + timedelta(days=60),
                'valid_to': timezone.now() + timedelta(days=90),
                'is_seasonal': True,
                'season_name': 'Christmas & New Year'
            },
            {
                'title': 'Group Booking Discount',
                'description': 'Special rates for group bookings of 10+ people. Perfect for family reunions and corporate trips!',
                'discount_percentage': 25.00,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=365),
                'is_seasonal': False,
                'season_name': ''
            },
            {
                'title': 'Early Bird Discount',
                'description': 'Book your tour 3 months in advance and get exclusive early bird discounts!',
                'discount_percentage': 10.00,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=180),
                'is_seasonal': False,
                'season_name': ''
            }
        ]
        
        offers = {}
        for offer_data in offers_data:
            offer, created = Offer.objects.get_or_create(
                title=offer_data['title'],
                defaults=offer_data
            )
            offers[offer_data['title']] = offer
            if created:
                self.stdout.write(f'Created offer: {offer.title}')
        
        # Create Sample Packages
        kerala_category = categories['Kerala Packages']
        north_india_category = categories['North India Tours']
        international_category = categories['International Tours']
        wayanad_category = categories['Wayanad Special']
        beach_category = categories['Beach Holidays']
        
        packages_data = [
            {
                'name': 'Kerala Backwaters & Ayurveda Experience',
                'description': 'Experience the serene backwaters of Kerala with traditional Ayurvedic treatments. Perfect for relaxation and rejuvenation. Cruise through the peaceful backwaters on a traditional houseboat while enjoying authentic Kerala cuisine and wellness treatments.',
                'category': kerala_category,
                'offer': offers['Onam Special Discount'],
                'package_type': 'family',
                'price': 15999.00,
                'duration': '4 days, 3 nights',
                'location': 'Kerala',
                'destinations': 'Alleppey, Kumarakom, Thekkady',
                'max_group_size': 8,
                'min_age': 5,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': 'Golden Triangle Tour - Delhi, Agra, Jaipur',
                'description': 'Explore the iconic Golden Triangle covering Delhi, Agra, and Jaipur. Witness the majestic Taj Mahal, explore royal palaces, and experience the rich history of North India. Perfect for history buffs and culture enthusiasts.',
                'category': north_india_category,
                'offer': offers['Group Booking Discount'],
                'package_type': 'group',
                'price': 24999.00,
                'duration': '6 days, 5 nights',
                'location': 'North India',
                'destinations': 'Delhi, Agra, Jaipur',
                'max_group_size': 15,
                'min_age': 8,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': 'Thailand Beach Paradise - Phuket & Krabi',
                'description': 'Discover the beautiful beaches of Phuket and Krabi. Enjoy water sports, island hopping, Thai culture, and delicious cuisine. Experience the perfect blend of adventure and relaxation in Thailand.',
                'category': international_category,
                'offer': offers['Christmas & New Year Special'],
                'package_type': 'honeymoon',
                'price': 45999.00,
                'duration': '7 days, 6 nights',
                'location': 'Thailand',
                'destinations': 'Phuket, Krabi, Bangkok',
                'max_group_size': 6,
                'min_age': 12,
                'is_featured': True,
                'is_popular': True
            },
            {
                'name': 'Wayanad Nature & Adventure Package',
                'description': 'Explore the pristine beauty of Wayanad with trekking, wildlife safaris, and nature walks. Visit Chembra Peak, Banasura Sagar Dam, and ancient Edakkal Caves. Perfect for nature lovers and adventure seekers.',
                'category': wayanad_category,
                'offer': offers['Early Bird Discount'],
                'package_type': 'adventure',
                'price': 12999.00,
                'duration': '5 days, 4 nights',
                'location': 'Wayanad, Kerala',
                'destinations': 'Chembra Peak, Banasura Dam, Edakkal Caves',
                'max_group_size': 12,
                'min_age': 10,
                'is_featured': True,
                'is_popular': False
            },
            {
                'name': 'Goa Beach & Culture Tour',
                'description': 'Experience the best of Goa with beautiful beaches, Portuguese architecture, and vibrant nightlife. Visit Old Goa churches, enjoy water sports, and relax on pristine beaches.',
                'category': beach_category,
                'offer': None,
                'package_type': 'family',
                'price': 18999.00,
                'duration': '5 days, 4 nights',
                'location': 'Goa',
                'destinations': 'Panaji, Old Goa, Calangute, Baga',
                'max_group_size': 10,
                'min_age': 6,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': 'Rajasthan Heritage Tour',
                'description': 'Journey through the royal state of Rajasthan. Visit magnificent forts, palaces, and experience the rich culture of the desert state. Includes camel safari and traditional folk performances.',
                'category': north_india_category,
                'offer': offers['Group Booking Discount'],
                'package_type': 'luxury',
                'price': 32999.00,
                'duration': '8 days, 7 nights',
                'location': 'Rajasthan',
                'destinations': 'Jaipur, Jodhpur, Udaipur, Jaisalmer',
                'max_group_size': 8,
                'min_age': 8,
                'is_featured': True,
                'is_popular': False
            },
            {
                'name': 'Dubai Shopping & Adventure',
                'description': 'Experience the magic of Dubai with desert safaris, Burj Khalifa, shopping at Dubai Mall, and traditional souks. Perfect blend of modern luxury and traditional Arabian culture.',
                'category': international_category,
                'offer': offers['Christmas & New Year Special'],
                'package_type': 'luxury',
                'price': 38999.00,
                'duration': '6 days, 5 nights',
                'location': 'Dubai, UAE',
                'destinations': 'Dubai, Abu Dhabi',
                'max_group_size': 6,
                'min_age': 12,
                'is_featured': False,
                'is_popular': True
            },
            {
                'name': 'Kerala Hill Station Tour',
                'description': 'Escape to the cool hill stations of Kerala. Visit Munnar tea gardens, Thekkady wildlife sanctuary, and Vagamon meadows. Experience the perfect climate and breathtaking views.',
                'category': kerala_category,
                'offer': offers['Onam Special Discount'],
                'package_type': 'family',
                'price': 17999.00,
                'duration': '6 days, 5 nights',
                'location': 'Kerala Hills',
                'destinations': 'Munnar, Thekkady, Vagamon',
                'max_group_size': 10,
                'min_age': 5,
                'is_featured': False,
                'is_popular': True
            }
        ]
        
        packages = {}
        for package_data in packages_data:
            package, created = Package.objects.get_or_create(
                name=package_data['name'],
                defaults=package_data
            )
            packages[package_data['name']] = package
            if created:
                self.stdout.write(f'Created package: {package.name}')
        
        # Create sample inclusions and exclusions for packages
        common_inclusions = [
            ('Hotel Accommodation', 'Comfortable hotel stay with breakfast', 'fa-bed', True),
            ('Transportation', 'AC vehicle with experienced driver', 'fa-car', True),
            ('Professional Guide', 'Experienced local guide for sightseeing', 'fa-user-tie', False),
            ('Sightseeing', 'All mentioned attractions and monuments', 'fa-camera', False),
            ('Mineral Water', 'Daily mineral water during tours', 'fa-tint', False),
            ('All Taxes', 'GST and other applicable taxes included', 'fa-receipt', False),
            ('Welcome Kit', 'Travel essentials and information booklet', 'fa-gift', False),
        ]

        common_exclusions = [
            ('Airfare', 'Flight tickets not included in package', 'fa-plane'),
            ('Lunch & Dinner', 'Meals except breakfast not included', 'fa-utensils'),
            ('Personal Expenses', 'Shopping, tips, laundry, etc.', 'fa-shopping-bag'),
            ('Travel Insurance', 'Travel insurance not included', 'fa-shield-alt'),
            ('Optional Activities', 'Activities not mentioned in itinerary', 'fa-star'),
            ('Camera Charges', 'Camera fees at monuments and attractions', 'fa-camera'),
            ('Visa Fees', 'International visa fees not included', 'fa-passport'),
        ]

        # Add inclusions and exclusions to packages
        for package in packages.values():
            for i, (title, desc, icon, highlighted) in enumerate(common_inclusions):
                PackageInclusion.objects.get_or_create(
                    package=package,
                    title=title,
                    defaults={
                        'description': desc,
                        'icon': icon,
                        'is_highlighted': highlighted,
                        'order': i,
                        'is_active': True
                    }
                )
            
            for i, (title, desc, icon) in enumerate(common_exclusions):
                PackageExclusion.objects.get_or_create(
                    package=package,
                    title=title,
                    defaults={
                        'description': desc,
                        'icon': icon,
                        'order': i,
                        'is_active': True
                    }
                )

        # Create sample itineraries for packages
        itinerary_data = {
            'Kerala Backwaters & Ayurveda Experience': [
                (1, 'Arrival & Houseboat Check-in', 'Arrive in Alleppey, check into traditional houseboat. Evening cruise through backwaters, dinner on board.'),
                (2, 'Backwater Exploration', 'Full day exploring backwaters, visit local villages, traditional fishing methods. Ayurvedic massage in evening.'),
                (3, 'Kumarakom & Thekkady', 'Visit Kumarakom bird sanctuary, then proceed to Thekkady. Evening spice plantation tour.'),
                (4, 'Thekkady Wildlife & Departure', 'Morning wildlife safari in Periyar, visit spice market, departure with memories.')
            ],
            'Golden Triangle Tour - Delhi, Agra, Jaipur': [
                (1, 'Delhi Arrival & City Tour', 'Arrive in Delhi, visit Red Fort, Jama Masjid, Qutub Minar. Evening at India Gate.'),
                (2, 'Delhi Continued', 'Visit Humayun\'s Tomb, Lotus Temple, Akshardham. Evening shopping at Connaught Place.'),
                (3, 'Delhi to Agra', 'Drive to Agra, visit Agra Fort. Evening at Mehtab Bagh for Taj view.'),
                (4, 'Taj Mahal & Fatehpur Sikri', 'Sunrise visit to Taj Mahal, then Fatehpur Sikri. Evening drive to Jaipur.'),
                (5, 'Jaipur City Tour', 'Visit Amber Fort, City Palace, Hawa Mahal. Evening traditional dinner with folk music.'),
                (6, 'Jaipur & Departure', 'Visit Jantar Mantar, local bazaars. Evening departure with unforgettable memories.')
            ],
            'Thailand Beach Paradise - Phuket & Krabi': [
                (1, 'Bangkok Arrival', 'Arrive in Bangkok, visit Grand Palace, Wat Phra Kaew. Evening at Khao San Road.'),
                (2, 'Bangkok to Phuket', 'Flight to Phuket, visit Big Buddha, Patong Beach. Evening at Phuket Night Market.'),
                (3, 'Phuket Island Hopping', 'Full day island hopping to Phi Phi Islands, snorkeling, swimming.'),
                (4, 'Phuket to Krabi', 'Drive to Krabi, visit Railay Beach, Tiger Cave Temple.'),
                (5, 'Krabi Adventure', 'Rock climbing at Railay, visit Emerald Pool, hot springs.'),
                (6, 'Krabi to Bangkok', 'Morning at Krabi beaches, evening flight to Bangkok.'),
                (7, 'Bangkok & Departure', 'Visit Chatuchak Weekend Market, departure with amazing memories.')
            ]
        }

        for package_name, itineraries in itinerary_data.items():
            if package_name in packages:
                package = packages[package_name]
                for day_num, title, description in itineraries:
                    Itinerary.objects.get_or_create(
                        package=package,
                        day_number=day_num,
                        defaults={
                            'title': title,
                            'description': description,
                            'is_active': True
                        }
                    )

        # Create Team Members
        team_data = [
            {
                'name': 'Rajesh Kumar',
                'position': 'Senior Travel Consultant',
                'bio': 'With 15 years of experience in the travel industry, Rajesh specializes in creating perfect itineraries for family and group tours. He has extensive knowledge of domestic and international destinations.',
                'experience_years': 15,
                'facebook_url': 'https://facebook.com/rajesh.kumar',
                'linkedin_url': 'https://linkedin.com/in/rajesh-kumar'
            },
            {
                'name': 'Priya Menon',
                'position': 'Tour Guide & Operations Manager',
                'bio': 'Expert in Kerala tourism with deep knowledge of local culture, history, and hidden gems of Wayanad. She ensures every tour is memorable and authentic.',
                'experience_years': 12,
                'instagram_url': 'https://instagram.com/priya.menon',
                'linkedin_url': 'https://linkedin.com/in/priya-menon'
            },
            {
                'name': 'Amit Singh',
                'position': 'Adventure Tour Specialist',
                'bio': 'Certified adventure guide specializing in trekking, camping, and outdoor activities across India. He ensures safe and thrilling adventure experiences.',
                'experience_years': 10,
                'facebook_url': 'https://facebook.com/amit.singh',
                'twitter_url': 'https://twitter.com/amit_singh'
            },
            {
                'name': 'Sneha Thomas',
                'position': 'Customer Service Manager',
                'bio': 'Dedicated to ensuring exceptional customer experience with 24/7 support for all travel queries. She handles customer satisfaction and feedback.',
                'experience_years': 8,
                'linkedin_url': 'https://linkedin.com/in/sneha-thomas',
                'instagram_url': 'https://instagram.com/sneha.thomas'
            }
        ]
        
        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created team member: {member.name}')
        
        # Create Site Statistics
        stats, created = SiteStats.objects.get_or_create(
            defaults={
                'featured_projects': 150,
                'luxury_houses': 75,
                'satisfied_clients': 2500,
                'years_experience': 18,
                'destinations_covered': 45,
                'tours_completed': 1800
            }
        )
        if created:
            self.stdout.write('Created site statistics')
        
        # Create Newsletter Subscriptions
        newsletter_emails = [
            'john.doe@email.com',
            'jane.smith@email.com',
            'mike.wilson@email.com',
            'sarah.jones@email.com',
            'david.brown@email.com'
        ]
        
        for email in newsletter_emails:
            NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
        
        # Create CTA Section
        cta, created = CTASection.objects.get_or_create(
            title='Ready to Start Your Adventure?',
            defaults={
                'subtitle': 'Let us plan your perfect trip',
                'description': 'Join thousands of satisfied travelers who have experienced the world with Nature Holidays. Our expert team is ready to create your dream vacation.',
                'button_text': 'Start Planning',
                'button_link': '/packages/',
                'is_active': True
            }
        )
        if created:
            self.stdout.write('Created CTA section')
        
        # Create Blog Categories
        blog_categories = [
            {
                'name': 'Travel Tips',
                'slug': 'travel-tips',
                'description': 'Essential travel tips and advice for travelers'
            },
            {
                'name': 'Destination Guides',
                'slug': 'destination-guides',
                'description': 'Comprehensive guides to popular destinations'
            },
            {
                'name': 'Travel Stories',
                'slug': 'travel-stories',
                'description': 'Real travel experiences and stories from our clients'
            },
            {
                'name': 'Travel News',
                'slug': 'travel-news',
                'description': 'Latest travel news and updates'
            },
            {
                'name': 'Kerala Tourism',
                'slug': 'kerala-tourism',
                'description': 'Everything about Kerala - God\'s Own Country'
            }
        ]

        for category_data in blog_categories:
            category, created = BlogCategory.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )
            if created:
                self.stdout.write(f'Created blog category: {category.name}')

        # Create Blog Tags
        blog_tags = [
            'Kerala', 'Wayanad', 'North India', 'Golden Triangle', 'Beach Holidays',
            'Cultural Tours', 'Adventure', 'Luxury Travel', 'Budget Travel', 'Family Travel',
            'Honeymoon', 'Group Tours', 'Photography', 'Food', 'Heritage', 'Backwaters',
            'Hill Stations', 'Wildlife', 'Ayurveda', 'Shopping', 'Nightlife'
        ]

        for tag_name in blog_tags:
            tag, created = BlogTag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created blog tag: {tag.name}')

        # Create Sample Blog Posts
        travel_tips_category = BlogCategory.objects.get(slug='travel-tips')
        destination_guides_category = BlogCategory.objects.get(slug='destination-guides')
        travel_stories_category = BlogCategory.objects.get(slug='travel-stories')
        kerala_tourism_category = BlogCategory.objects.get(slug='kerala-tourism')

        blog_posts = [
            {
                'title': 'Essential Travel Tips for First-Time Travelers to Kerala',
                'slug': 'essential-travel-tips-kerala-first-time-travelers',
                'excerpt': 'Planning your first trip to Kerala? Here are the essential tips you need to know for a memorable experience.',
                'content': '''
                Kerala, often called "God's Own Country," is a paradise for travelers. If you're planning your first trip to this beautiful state, here are some essential tips to make your journey unforgettable.

                **Best Time to Visit**
                The best time to visit Kerala is from October to March when the weather is pleasant and perfect for exploring. The monsoon season (June to September) offers a unique experience with lush greenery, but heavy rains might affect outdoor activities.

                **What to Pack**
                - Light cotton clothes for the tropical climate
                - Comfortable walking shoes
                - Rain gear (especially during monsoon)
                - Sunscreen and mosquito repellent
                - Camera for capturing beautiful moments

                **Must-Visit Places**
                1. **Munnar**: Famous for tea plantations and cool climate
                2. **Alleppey**: Experience the serene backwaters
                3. **Kochi**: Rich in history and culture
                4. **Wayanad**: Perfect for nature lovers and adventure seekers
                5. **Kovalam**: Beautiful beaches and Ayurvedic treatments

                **Local Cuisine**
                Don't miss trying the authentic Kerala cuisine:
                - Appam with stew
                - Kerala fish curry
                - Malabar biryani
                - Fresh coconut water
                - Traditional Kerala sadya

                **Transportation Tips**
                - Book your houseboat in advance for backwater tours
                - Use local buses for budget travel
                - Hire a car with driver for convenience
                - Book train tickets early for long-distance travel

                **Cultural Etiquette**
                - Dress modestly, especially when visiting temples
                - Remove shoes before entering religious places
                - Respect local customs and traditions
                - Learn a few basic Malayalam phrases

                **Safety Tips**
                - Keep emergency numbers handy
                - Stay hydrated in the tropical climate
                - Be cautious with street food
                - Keep your valuables safe

                Remember, Kerala is not just a destination; it's an experience that will stay with you forever. Plan well, pack smart, and get ready for an amazing journey!
                ''',
                'category': travel_tips_category,
                'author': 'Nature Holidays Team',
                'status': 'published',
                'published_date': timezone.now() - timedelta(days=5),
                'is_featured': True,
                'tags': ['Kerala', 'Travel Tips', 'First Time Travel']
            },
            {
                'title': 'Complete Guide to Exploring Wayanad - Kerala\'s Hidden Gem',
                'slug': 'complete-guide-exploring-wayanad-kerala-hidden-gem',
                'excerpt': 'Discover the beauty of Wayanad with our comprehensive guide covering attractions, activities, and travel tips.',
                'content': '''
                Wayanad, nestled in the Western Ghats, is one of Kerala's most beautiful hill stations. Known for its pristine nature, wildlife sanctuaries, and adventure activities, Wayanad offers a perfect blend of tranquility and excitement.

                **Getting to Wayanad**
                - **By Air**: Nearest airport is Calicut International Airport (100 km)
                - **By Train**: Nearest railway station is Kozhikode (75 km)
                - **By Road**: Well-connected by road from major cities

                **Top Attractions**

                **1. Chembra Peak**
                The highest peak in Wayanad, offering breathtaking views of the Western Ghats. The heart-shaped lake on the way is a major attraction.

                **2. Banasura Sagar Dam**
                India's largest earthen dam, surrounded by beautiful landscapes. Perfect for boating and photography.

                **3. Edakkal Caves**
                Ancient caves with prehistoric rock art, offering a glimpse into human history dating back 6000 years.

                **4. Wildlife Sanctuaries**
                - Wayanad Wildlife Sanctuary
                - Muthanga Wildlife Sanctuary
                - Tholpetty Wildlife Sanctuary

                **5. Waterfalls**
                - Soochipara Falls
                - Meenmutty Falls
                - Kanthanpara Falls

                **Adventure Activities**
                - Trekking to various peaks
                - Rock climbing
                - Bird watching
                - Wildlife safari
                - Camping in the wilderness

                **Best Time to Visit**
                - **October to May**: Pleasant weather, perfect for outdoor activities
                - **Monsoon (June-September)**: Heavy rains but lush greenery
                - **Summer (March-May)**: Warm but manageable

                **Where to Stay**
                - Luxury resorts with mountain views
                - Eco-friendly homestays
                - Tree houses for unique experience
                - Budget hotels for economical travel

                **Local Cuisine**
                - Traditional Kerala meals
                - Fresh honey from local farms
                - Organic tea and coffee
                - Tribal cuisine

                **Travel Tips**
                - Book accommodations in advance during peak season
                - Carry warm clothes for evening and early morning
                - Hire local guides for trekking
                - Respect wildlife and nature
                - Carry sufficient water during treks

                Wayanad is not just a destination; it's an experience that connects you with nature in its purest form. Whether you're an adventure seeker or a peace lover, Wayanad has something for everyone.
                ''',
                'category': destination_guides_category,
                'author': 'Nature Holidays Team',
                'status': 'published',
                'published_date': timezone.now() - timedelta(days=10),
                'is_featured': True,
                'tags': ['Wayanad', 'Kerala', 'Adventure', 'Nature']
            },
            {
                'title': 'Amazing Golden Triangle Tour Experience - A Client\'s Story',
                'slug': 'amazing-golden-triangle-tour-experience-client-story',
                'excerpt': 'Read about our client\'s incredible journey through Delhi, Agra, and Jaipur with Nature Holidays.',
                'content': '''
                Last month, we had the pleasure of organizing a Golden Triangle tour for the Sharma family from Kerala. Here's their amazing story that we'd like to share with you.

                **The Journey Begins**

                The Sharma family, consisting of parents and two teenage children, had always dreamed of exploring the rich cultural heritage of North India. They chose Nature Holidays for their 7-day Golden Triangle tour, and what followed was an experience they'll cherish forever.

                **Day 1-2: Delhi - The Heart of India**

                Their journey began in Delhi, where they were greeted by our experienced guide, Rajesh. The family was amazed by the contrast between Old Delhi and New Delhi.

                **Highlights in Delhi:**
                - Red Fort: The magnificent Mughal architecture left them speechless
                - Jama Masjid: One of India's largest mosques
                - Qutub Minar: The tallest brick minaret in the world
                - India Gate: Evening visit with beautiful lighting
                - Humayun's Tomb: UNESCO World Heritage site

                **Day 3-4: Agra - The City of Love**

                The highlight of their trip was undoubtedly the visit to the Taj Mahal. Mrs. Sharma was emotional seeing the monument of love in person.

                **Agra Highlights:**
                - Taj Mahal at sunrise (an experience they'll never forget)
                - Agra Fort: Rich in history and architecture
                - Fatehpur Sikri: The abandoned city
                - Local market shopping for souvenirs

                **Day 5-7: Jaipur - The Pink City**

                Jaipur offered them a royal experience with its palaces and forts.

                **Jaipur Highlights:**
                - Amber Fort: Elephant ride to the fort entrance
                - City Palace: Still the residence of the royal family
                - Hawa Mahal: The Palace of Winds
                - Jantar Mantar: Ancient astronomical observatory
                - Local bazaars for traditional shopping

                **What Made Their Trip Special**

                **1. Expert Guidance**
                Our guide Rajesh was not just knowledgeable but also passionate about sharing India's rich history and culture.

                **2. Comfortable Accommodation**
                Carefully selected hotels that offered both comfort and local charm.

                **3. Authentic Experiences**
                - Traditional Rajasthani dinner with folk music
                - Cooking class in Jaipur
                - Rickshaw ride in Old Delhi
                - Local market exploration

                **4. Safety and Comfort**
                - AC vehicle with experienced driver
                - 24/7 support throughout the journey
                - Flexible itinerary based on their preferences

                **Client's Feedback**

                "We had heard great things about Nature Holidays, and they exceeded our expectations. Every detail was taken care of, from comfortable transportation to knowledgeable guides. The Golden Triangle tour was not just a vacation; it was an educational and cultural experience for our entire family. We highly recommend Nature Holidays to anyone planning to explore India."

                **Why Choose Nature Holidays for Golden Triangle?**

                1. **Experienced Team**: Our guides have years of experience
                2. **Customized Itineraries**: Tailored to your preferences
                3. **Quality Accommodation**: Carefully selected hotels
                4. **24/7 Support**: We're always there when you need us
                5. **Authentic Experiences**: Beyond just sightseeing

                The Golden Triangle tour is perfect for families, couples, and solo travelers who want to experience the essence of North India. Contact us to plan your own unforgettable journey!
                ''',
                'category': travel_stories_category,
                'author': 'Nature Holidays Team',
                'status': 'published',
                'published_date': timezone.now() - timedelta(days=15),
                'is_featured': False,
                'tags': ['Golden Triangle', 'North India', 'Cultural Tours', 'Family Travel']
            },
            {
                'title': 'Top 10 Must-Visit Places in Kerala for 2024',
                'slug': 'top-10-must-visit-places-kerala-2024',
                'excerpt': 'Discover the most beautiful and trending destinations in Kerala that you must visit in 2024.',
                'content': '''
                Kerala, known as "God's Own Country," continues to be one of India's most popular tourist destinations. As we enter 2024, here are the top 10 places you must visit in Kerala for an unforgettable experience.

                **1. Munnar - The Tea Paradise**
                Famous for its sprawling tea plantations, Munnar offers breathtaking views of the Western Ghats. Visit the Tea Museum, take a guided plantation tour, and enjoy the cool climate.

                **2. Alleppey - Venice of the East**
                Experience the magical backwaters on a traditional houseboat. Cruise through the serene waters, visit local villages, and enjoy authentic Kerala cuisine.

                **3. Wayanad - Nature's Wonderland**
                Perfect for adventure seekers, Wayanad offers trekking, wildlife safaris, and ancient caves. Don't miss Chembra Peak and Edakkal Caves.

                **4. Kochi - Historic Port City**
                A blend of Portuguese, Dutch, and British influences. Visit Fort Kochi, Jewish Synagogue, and enjoy the vibrant art scene.

                **5. Thekkady - Wildlife Haven**
                Home to Periyar Wildlife Sanctuary, perfect for wildlife enthusiasts. Enjoy boat rides, nature walks, and spice plantation tours.

                **6. Kovalam - Beach Paradise**
                Famous for its crescent-shaped beaches and Ayurvedic treatments. Perfect for relaxation and wellness.

                **7. Kumarakom - Bird Watcher's Paradise**
                Located on Vembanad Lake, perfect for bird watching and backwater experiences.

                **8. Varkala - Cliff Beach**
                Unique cliff beach with stunning views and spiritual significance. Great for surfing and yoga.

                **9. Bekal - Fort by the Sea**
                Historic fort with beautiful beach views. Perfect for history buffs and beach lovers.

                **10. Vagamon - Hill Station Gem**
                Less crowded than Munnar, offering beautiful meadows, pine forests, and adventure activities.

                **Best Time to Visit**
                - **October to March**: Pleasant weather, perfect for all activities
                - **Monsoon (June-September)**: Lush greenery, unique experiences
                - **Summer (March-May)**: Warm but manageable

                **Travel Tips for 2024**
                - Book accommodations 3-6 months in advance
                - Consider off-season travel for better rates
                - Try local experiences and homestays
                - Respect local culture and environment
                - Support local businesses and artisans

                Kerala in 2024 promises to be more exciting than ever with new experiences, improved infrastructure, and sustainable tourism practices. Start planning your trip today!
                ''',
                'category': kerala_tourism_category,
                'author': 'Nature Holidays Team',
                'status': 'published',
                'published_date': timezone.now() - timedelta(days=20),
                'is_featured': True,
                'tags': ['Kerala', 'Tourism', '2024', 'Destinations', 'Travel Guide']
            }
        ]

        for blog_data in blog_posts:
            blog, created = Blog.objects.get_or_create(
                slug=blog_data['slug'],
                defaults={
                    'title': blog_data['title'],
                    'excerpt': blog_data['excerpt'],
                    'content': blog_data['content'],
                    'category': blog_data['category'],
                    'author': blog_data['author'],
                    'status': blog_data['status'],
                    'published_date': blog_data['published_date'],
                    'is_featured': blog_data['is_featured'],
                    'is_active': True
                }
            )
            if created:
                # Add tags to the blog
                for tag_name in blog_data['tags']:
                    try:
                        tag = BlogTag.objects.get(name=tag_name)
                        blog.tags.add(tag)
                    except BlogTag.DoesNotExist:
                        pass
                self.stdout.write(f'Created blog post: {blog.title}')

        # Create Sample Blog Comments
        comments_data = [
            {
                'blog_title': 'Essential Travel Tips for First-Time Travelers to Kerala',
                'name': 'Priya Sharma',
                'email': 'priya.sharma@email.com',
                'comment': 'Great tips! I\'m planning my first trip to Kerala next month and this article is very helpful. Can\'t wait to experience the backwaters!'
            },
            {
                'blog_title': 'Essential Travel Tips for First-Time Travelers to Kerala',
                'name': 'Rahul Kumar',
                'email': 'rahul.kumar@email.com',
                'comment': 'Thanks for sharing these tips. The monsoon season information is particularly useful. Looking forward to my Kerala adventure!'
            },
            {
                'blog_title': 'Complete Guide to Exploring Wayanad - Kerala\'s Hidden Gem',
                'name': 'Anita Patel',
                'email': 'anita.patel@email.com',
                'comment': 'Wayanad looks absolutely stunning! I\'ve added it to my bucket list. The adventure activities sound amazing.'
            },
            {
                'blog_title': 'Amazing Golden Triangle Tour Experience - A Client\'s Story',
                'name': 'Vikram Singh',
                'email': 'vikram.singh@email.com',
                'comment': 'This story is inspiring! I\'m planning a similar trip with my family. Nature Holidays seems like the perfect choice.'
            }
        ]

        for comment_data in comments_data:
            try:
                blog = Blog.objects.get(title=comment_data['blog_title'])
                BlogComment.objects.get_or_create(
                    blog=blog,
                    email=comment_data['email'],
                    defaults={
                        'name': comment_data['name'],
                        'comment': comment_data['comment'],
                        'is_active': True
                    }
                )
            except Blog.DoesNotExist:
                pass

        # Create Sample Contact Messages
        sample_contacts = [
            {
                'name': 'Rahul Sharma',
                'email': 'rahul.sharma@email.com',
                'phone': '+91-9876543210',
                'service': 'Kerala Packages',
                'message': 'Hi, I am interested in your Kerala backwater packages. Can you please send me the details for a 5-day trip? Looking for something family-friendly.'
            },
            {
                'name': 'Priya Patel',
                'email': 'priya.patel@email.com',
                'phone': '+91-8765432109',
                'service': 'North India Tours',
                'message': 'Looking for Golden Triangle tour packages. Please share the itinerary and pricing details. We are a group of 6 people.'
            },
            {
                'name': 'Amit Kumar',
                'email': 'amit.kumar@email.com',
                'phone': '+91-7654321098',
                'service': 'Custom Packages',
                'message': 'We are a group of 8 people planning a trip to Wayanad. Can you create a custom package for us? We want adventure activities.'
            },
            {
                'name': 'Sneha Thomas',
                'email': 'sneha.thomas@email.com',
                'phone': '+91-6543210987',
                'service': 'International Tours',
                'message': 'Interested in Thailand packages. Can you provide details about Phuket and Krabi tours? Looking for honeymoon packages.'
            },
            {
                'name': 'David Wilson',
                'email': 'david.wilson@email.com',
                'phone': '+1-555-123-4567',
                'service': 'Other',
                'message': 'Planning a trip to India from the US. Looking for a comprehensive tour covering multiple destinations. Please advise on the best options.'
            }
        ]

        for contact_data in sample_contacts:
            contact, created = Contact.objects.get_or_create(
                email=contact_data['email'],
                defaults=contact_data
            )
            if created:
                self.stdout.write(f'Created contact message from: {contact.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated comprehensive sample data for Nature Holidays!'))
        self.stdout.write('Your website is now ready with:')
        self.stdout.write(f'- {Category.objects.count()} Categories')
        self.stdout.write(f'- {Offer.objects.count()} Offers')
        self.stdout.write(f'- {Package.objects.count()} Packages')
        self.stdout.write(f'- {TeamMember.objects.count()} Team Members')
        self.stdout.write(f'- {Blog.objects.count()} Blog Posts')
        self.stdout.write(f'- {Contact.objects.count()} Contact Messages')
        self.stdout.write('Ready for hosting on Render! 🚀') 