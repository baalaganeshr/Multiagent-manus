"""
Social Media Agent - Real Implementation
Manages social media presence, content scheduling, and engagement across multiple platforms.
"""

import asyncio
import logging
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class SocialMediaAgent:
    """Real Social Media Agent that manages multi-platform social media strategies."""
    
    def __init__(self):
        self.agent_name = "social_media"
        self.is_initialized = False
        self.output_directory = Path("generated_social_media")
        self.output_directory.mkdir(exist_ok=True)
        
        # Platform-specific configurations
        self.platforms = {
            "facebook": {
                "max_post_length": 63206,
                "best_posting_times": ["9:00 AM", "1:00 PM", "3:00 PM"],
                "content_types": ["text", "image", "video", "link", "event"],
                "hashtag_limit": 30,
                "engagement_features": ["reactions", "comments", "shares"]
            },
            "instagram": {
                "max_post_length": 2200,
                "best_posting_times": ["11:00 AM", "2:00 PM", "5:00 PM"],
                "content_types": ["image", "video", "story", "reel", "igtv"],
                "hashtag_limit": 30,
                "engagement_features": ["likes", "comments", "shares", "saves"]
            },
            "twitter": {
                "max_post_length": 280,
                "best_posting_times": ["9:00 AM", "12:00 PM", "6:00 PM"],
                "content_types": ["text", "image", "video", "poll", "thread"],
                "hashtag_limit": 10,
                "engagement_features": ["likes", "retweets", "replies"]
            },
            "linkedin": {
                "max_post_length": 3000,
                "best_posting_times": ["8:00 AM", "12:00 PM", "5:00 PM"],
                "content_types": ["text", "image", "video", "article", "poll"],
                "hashtag_limit": 20,
                "engagement_features": ["likes", "comments", "shares"]
            },
            "tiktok": {
                "max_post_length": 300,
                "best_posting_times": ["6:00 AM", "10:00 AM", "7:00 PM"],
                "content_types": ["video", "duet", "stitch"],
                "hashtag_limit": 100,
                "engagement_features": ["likes", "comments", "shares", "follows"]
            },
            "youtube": {
                "max_post_length": 5000,
                "best_posting_times": ["2:00 PM", "3:00 PM", "4:00 PM"],
                "content_types": ["video", "short", "community_post"],
                "hashtag_limit": 15,
                "engagement_features": ["likes", "comments", "subscribes", "shares"]
            }
        }
        
        # Business type specific social media strategies
        self.business_strategies = {
            "restaurant": {
                "primary_platforms": ["instagram", "facebook", "tiktok"],
                "content_themes": ["food_photos", "behind_scenes", "customer_reviews", "menu_highlights", "chef_stories"],
                "posting_frequency": {"daily": ["instagram"], "weekly": ["facebook", "tiktok"]},
                "hashtag_categories": ["food", "restaurant", "local", "cuisine", "dining"]
            },
            "retail": {
                "primary_platforms": ["instagram", "facebook", "pinterest"],
                "content_themes": ["product_showcase", "styling_tips", "customer_photos", "sales_promotions", "brand_story"],
                "posting_frequency": {"daily": ["instagram"], "weekly": ["facebook"], "bi-weekly": ["pinterest"]},
                "hashtag_categories": ["retail", "shopping", "fashion", "lifestyle", "deals"]
            },
            "service": {
                "primary_platforms": ["linkedin", "facebook", "twitter"],
                "content_themes": ["expertise_sharing", "client_testimonials", "industry_insights", "team_highlights", "case_studies"],
                "posting_frequency": {"weekly": ["linkedin", "facebook"], "bi-weekly": ["twitter"]},
                "hashtag_categories": ["professional", "service", "expertise", "business", "consulting"]
            }
        }
        
        # Content templates by type
        self.content_templates = {
            "promotional": {
                "restaurant": [
                    "🍽️ New menu item alert! Try our {dish_name} - made with fresh {ingredients}. Available now at {business_name}!",
                    "👨‍🍳 Chef's special today: {dish_name}! Book your table and taste the magic. #FreshFood #LocalRestaurant",
                    "🌟 Customer favorite: {dish_name}! Join us for an unforgettable dining experience. Reserve now!"
                ],
                "retail": [
                    "✨ New arrival: {product_name}! Perfect for {occasion}. Shop now and get {discount}% off! #NewCollection",
                    "🛍️ Limited time offer: {product_name} at just ${price}! Don't miss out on this amazing deal. #Sale #Shopping",
                    "💎 Spotlight on {product_name} - the must-have item of the season! Available in store and online."
                ],
                "service": [
                    "🚀 Transform your business with our {service_name}. Book a consultation today and see the difference!",
                    "✅ Success story: How we helped {client_type} achieve {result}. Ready to be our next success story?",
                    "💡 Expert tip: {tip}. Contact us to learn how we can help optimize your {business_area}."
                ]
            },
            "educational": {
                "restaurant": [
                    "🍳 Kitchen secrets: Did you know {cooking_tip}? Our chefs share their expertise!",
                    "🥗 Healthy eating tip: {nutrition_fact}. Come try our nutritious options at {business_name}!",
                    "🌱 Ingredient spotlight: {ingredient} - learn about its benefits and taste it in our {dish_name}!"
                ],
                "retail": [
                    "💡 Style tip: {styling_advice}. Shop these pieces to create the perfect look!",
                    "🔍 Product care: Here's how to maintain your {product_type} for years to come.",
                    "✨ Trend alert: {trend_name} is taking over! Here's how to incorporate it into your wardrobe."
                ],
                "service": [
                    "📊 Industry insight: {statistic}. Here's what this means for your business strategy.",
                    "💼 Best practice: {tip} can significantly improve your {business_process}.",
                    "🎯 Strategy spotlight: How {strategy_name} can drive growth in {industry}."
                ]
            },
            "engagement": {
                "restaurant": [
                    "🤔 What's your go-to comfort food? Tell us in the comments! We might feature it on our menu.",
                    "📸 Share your best food photo from {business_name} and tag us! We love seeing your experiences.",
                    "❓ Quiz time: Can you guess the secret ingredient in our signature {dish_name}?"
                ],
                "retail": [
                    "💬 What's your favorite piece from our new collection? Comment below!",
                    "📷 Show us how you style your {product_name}! Tag us for a chance to be featured.",
                    "🎨 Help us decide: Which color should we add to our {product_line} next?"
                ],
                "service": [
                    "🤝 What's your biggest business challenge right now? Share in the comments - we're here to help!",
                    "💭 Industry professionals: What trends are you seeing in {industry}? Let's discuss!",
                    "📈 Poll: What's most important for business growth in 2024? A) Technology B) Team C) Strategy D) All"
                ]
            }
        }
    
    async def initialize(self):
        """Initialize the Social Media Agent."""
        logger.info("Initializing Real Social Media Agent")
        self.is_initialized = True
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle social media management requests."""
        try:
            logger.info(f"Creating social media strategy for: {request.get('description', 'No description')}")
            
            # Extract business information
            business_info = self._extract_business_info(request)
            business_type = self._detect_business_type(request)
            
            # Generate comprehensive social media strategy
            social_strategy = await self._generate_social_strategy(business_type, business_info)
            
            # Create content calendar
            content_calendar = await self._create_content_calendar(business_type, business_info)
            
            # Generate sample content
            sample_content = await self._generate_sample_content(business_type, business_info)
            
            # Create social media files
            generated_files = await self._create_social_media_files(
                social_strategy, content_calendar, sample_content, business_info
            )
            
            return {
                "status": "success",
                "agent": self.agent_name,
                "business_type": business_type,
                "social_strategy": social_strategy,
                "content_calendar": content_calendar,
                "sample_content": sample_content,
                "generated_files": generated_files,
                "engagement_score": social_strategy["engagement_score"],
                "recommended_platforms": social_strategy["recommended_platforms"],
                "next_steps": social_strategy["implementation_steps"]
            }
            
        except Exception as e:
            logger.error(f"Social media agent error: {e}")
            return {
                "status": "error",
                "agent": self.agent_name,
                "error": str(e),
                "fallback_message": "Social media strategy generation failed, using basic recommendations"
            }
    
    def _extract_business_info(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business information from request."""
        region_context = request.get("region_context", {})
        localization = request.get("localization", {})
        
        return {
            "name": request.get("business_name", "Your Business"),
            "description": request.get("description", ""),
            "location": {
                "city": region_context.get("city", localization.get("city", "Your City")),
                "country": region_context.get("country", localization.get("country", "US"))
            },
            "target_audience": request.get("target_audience", "Local customers"),
            "budget": request.get("social_media_budget", "small"),
            "existing_platforms": request.get("existing_social_platforms", [])
        }
    
    def _detect_business_type(self, request: Dict[str, Any]) -> str:
        """Detect business type from request."""
        description = request.get("description", "").lower()
        business_type = request.get("business_type", "").lower()
        
        if business_type in ["restaurant", "retail", "service"]:
            return business_type
        
        # Auto-detect from description
        if any(word in description for word in ["restaurant", "cafe", "food", "dining"]):
            return "restaurant"
        elif any(word in description for word in ["shop", "store", "retail", "products"]):
            return "retail"
        else:
            return "service"
    
    async def _generate_social_strategy(self, business_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive social media strategy."""
        
        strategy = self.business_strategies[business_type]
        
        # Platform selection based on business type and budget
        recommended_platforms = self._select_platforms(business_type, business_info["budget"])
        
        # Content strategy
        content_strategy = self._generate_content_strategy(business_type, strategy)
        
        # Hashtag strategy
        hashtag_strategy = self._generate_hashtag_strategy(business_type, business_info)
        
        # Posting schedule
        posting_schedule = self._generate_posting_schedule(recommended_platforms, strategy)
        
        # Engagement strategy
        engagement_strategy = self._generate_engagement_strategy(business_type)
        
        # Analytics and KPIs
        analytics_strategy = self._generate_analytics_strategy(business_type)
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(content_strategy, posting_schedule)
        
        return {
            "recommended_platforms": recommended_platforms,
            "content_strategy": content_strategy,
            "hashtag_strategy": hashtag_strategy,
            "posting_schedule": posting_schedule,
            "engagement_strategy": engagement_strategy,
            "analytics_strategy": analytics_strategy,
            "engagement_score": engagement_score,
            "budget_allocation": self._generate_budget_allocation(recommended_platforms),
            "implementation_steps": self._generate_implementation_steps(business_type),
            "business_type": business_type
        }
    
    def _select_platforms(self, business_type: str, budget: str) -> List[str]:
        """Select optimal platforms based on business type and budget."""
        strategy = self.business_strategies[business_type]
        primary_platforms = strategy["primary_platforms"]
        
        if budget == "small":
            return primary_platforms[:2]  # Top 2 platforms
        elif budget == "medium":
            return primary_platforms[:3]  # Top 3 platforms
        else:  # large budget
            return primary_platforms  # All recommended platforms
    
    def _generate_content_strategy(self, business_type: str, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content strategy."""
        return {
            "content_themes": strategy["content_themes"],
            "content_mix": {
                "promotional": "30%",
                "educational": "40%",
                "engagement": "20%",
                "user_generated": "10%"
            },
            "visual_guidelines": {
                "brand_colors": "Consistent brand color palette",
                "image_style": "High-quality, professional photos",
                "video_format": "Short-form content (15-60 seconds)",
                "typography": "Readable fonts with brand consistency"
            },
            "content_pillars": strategy["content_themes"][:4]
        }
    
    def _generate_hashtag_strategy(self, business_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hashtag strategy."""
        strategy = self.business_strategies[business_type]
        location = business_info["location"]
        business_name = business_info["name"]
        
        # Generate hashtags by category
        hashtags = {
            "branded": [
                f"#{business_name.replace(' ', '').lower()}",
                f"#{business_name.replace(' ', '').lower()}{location['city'].lower()}"
            ],
            "local": [
                f"#{location['city'].lower()}",
                f"#{location['city'].lower()}{business_type}",
                f"#{location['country'].lower()}{business_type}"
            ],
            "industry": [
                f"#{category}" for category in strategy["hashtag_categories"]
            ],
            "trending": [
                "#smallbusiness",
                "#local",
                "#community",
                "#qualityservice"
            ]
        }
        
        return {
            "hashtag_categories": hashtags,
            "hashtag_mix": "2 branded + 3 local + 5 industry + 2 trending per post",
            "hashtag_research": "Monitor trending hashtags weekly",
            "hashtag_performance": "Track engagement by hashtag monthly"
        }
    
    def _generate_posting_schedule(self, platforms: List[str], strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate posting schedule."""
        schedule = {}
        
        for platform in platforms:
            platform_config = self.platforms[platform]
            frequency = self._get_posting_frequency(platform, strategy)
            
            schedule[platform] = {
                "frequency": frequency,
                "best_times": platform_config["best_posting_times"],
                "content_types": platform_config["content_types"],
                "weekly_posts": self._calculate_weekly_posts(frequency)
            }
        
        return {
            "platform_schedules": schedule,
            "content_calendar": "Plan content 1 month in advance",
            "scheduling_tools": ["Buffer", "Hootsuite", "Later", "Creator Studio"],
            "review_frequency": "Weekly performance review and adjustment"
        }
    
    def _get_posting_frequency(self, platform: str, strategy: Dict[str, Any]) -> str:
        """Get posting frequency for platform."""
        frequency_map = strategy.get("posting_frequency", {})
        
        for freq, platforms in frequency_map.items():
            if platform in platforms:
                return freq
        
        return "weekly"  # default
    
    def _calculate_weekly_posts(self, frequency: str) -> int:
        """Calculate number of posts per week."""
        frequency_map = {
            "daily": 7,
            "weekly": 2,
            "bi-weekly": 1
        }
        return frequency_map.get(frequency, 2)
    
    def _generate_engagement_strategy(self, business_type: str) -> Dict[str, Any]:
        """Generate engagement strategy."""
        return {
            "response_time": "Respond to comments/messages within 2-4 hours",
            "engagement_tactics": [
                "Ask questions in captions",
                "Create polls and interactive content",
                "Share user-generated content",
                "Host live Q&A sessions",
                "Use stories for behind-the-scenes content"
            ],
            "community_building": [
                "Follow and engage with local businesses",
                "Partner with complementary businesses",
                "Participate in local hashtags and events",
                "Create shareable, valuable content"
            ],
            "customer_service": [
                "Monitor mentions and tags",
                "Address complaints professionally",
                "Showcase positive reviews",
                "Provide helpful information"
            ]
        }
    
    def _generate_analytics_strategy(self, business_type: str) -> Dict[str, Any]:
        """Generate analytics and measurement strategy."""
        return {
            "key_metrics": {
                "reach": "Number of unique accounts reached",
                "engagement": "Likes, comments, shares, saves",
                "traffic": "Website clicks from social media",
                "conversions": "Sales/bookings from social media"
            },
            "tracking_tools": [
                "Native platform analytics",
                "Google Analytics (UTM parameters)",
                "Social media management tools",
                "Customer feedback surveys"
            ],
            "reporting_frequency": "Weekly metrics review, monthly detailed report",
            "kpi_targets": {
                "engagement_rate": "> 3%",
                "follower_growth": "10-20% monthly",
                "website_traffic": "5-10% from social media",
                "response_rate": "< 2 hours average"
            }
        }
    
    def _calculate_engagement_score(self, content_strategy: Dict[str, Any], posting_schedule: Dict[str, Any]) -> float:
        """Calculate predicted engagement score."""
        score = 0.0
        
        # Content strategy score
        if len(content_strategy["content_pillars"]) >= 4:
            score += 0.3
        
        # Posting frequency score
        total_weekly_posts = sum(
            schedule["weekly_posts"] for schedule in posting_schedule["platform_schedules"].values()
        )
        if total_weekly_posts >= 5:
            score += 0.3
        elif total_weekly_posts >= 3:
            score += 0.2
        
        # Platform diversity score
        platform_count = len(posting_schedule["platform_schedules"])
        if platform_count >= 3:
            score += 0.4
        elif platform_count >= 2:
            score += 0.3
        
        return min(score, 1.0)
    
    def _generate_budget_allocation(self, platforms: List[str]) -> Dict[str, str]:
        """Generate budget allocation recommendations."""
        if len(platforms) == 1:
            return {platforms[0]: "100%"}
        elif len(platforms) == 2:
            return {platforms[0]: "60%", platforms[1]: "40%"}
        elif len(platforms) == 3:
            return {platforms[0]: "50%", platforms[1]: "30%", platforms[2]: "20%"}
        else:
            equal_share = 100 // len(platforms)
            return {platform: f"{equal_share}%" for platform in platforms}
    
    def _generate_implementation_steps(self, business_type: str) -> List[Dict[str, Any]]:
        """Generate implementation timeline."""
        return [
            {
                "week": "Week 1-2: Setup & Optimization",
                "tasks": [
                    "Set up/optimize business profiles on selected platforms",
                    "Create branded visual templates",
                    "Develop content calendar for first month",
                    "Set up analytics tracking"
                ]
            },
            {
                "week": "Week 3-4: Content Creation",
                "tasks": [
                    "Create and schedule first batch of content",
                    "Develop hashtag strategy and lists",
                    "Set up social media management tools",
                    "Begin consistent posting schedule"
                ]
            },
            {
                "week": "Week 5-8: Engagement & Growth",
                "tasks": [
                    "Actively engage with audience and local community",
                    "Monitor and respond to comments/messages",
                    "Analyze performance and adjust strategy",
                    "Create user-generated content campaigns"
                ]
            },
            {
                "week": "Week 9+: Optimization & Scale",
                "tasks": [
                    "Review analytics and optimize top-performing content",
                    "Expand to additional platforms if budget allows",
                    "Develop advanced strategies (influencer partnerships, ads)",
                    "Create quarterly content strategy reviews"
                ]
            }
        ]
    
    async def _create_content_calendar(self, business_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create content calendar for next 4 weeks."""
        strategy = self.business_strategies[business_type]
        
        calendar = {}
        
        # Generate 4 weeks of content
        start_date = datetime.now()
        for week in range(4):
            week_start = start_date + timedelta(weeks=week)
            week_key = f"Week {week + 1} ({week_start.strftime('%b %d')})"
            
            week_content = []
            for day in range(7):
                post_date = week_start + timedelta(days=day)
                day_name = post_date.strftime('%A')
                
                # Determine content theme for the day
                theme_index = day % len(strategy["content_themes"])
                theme = strategy["content_themes"][theme_index]
                
                # Determine content type (promotional, educational, engagement)
                content_types = ["promotional", "educational", "engagement"]
                content_type = content_types[day % 3]
                
                week_content.append({
                    "date": post_date.strftime('%Y-%m-%d'),
                    "day": day_name,
                    "theme": theme,
                    "content_type": content_type,
                    "platforms": strategy["primary_platforms"][:2]  # Top 2 platforms
                })
            
            calendar[week_key] = week_content
        
        return {
            "calendar": calendar,
            "content_themes_rotation": strategy["content_themes"],
            "posting_guidelines": "Rotate content types daily, maintain visual consistency",
            "approval_process": "Review and approve content 3 days in advance"
        }
    
    async def _generate_sample_content(self, business_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sample social media content."""
        templates = self.content_templates
        business_name = business_info["name"]
        
        sample_content = {}
        
        for content_type in ["promotional", "educational", "engagement"]:
            content_templates = templates[content_type][business_type]
            sample_content[content_type] = []
            
            for template in content_templates[:3]:  # 3 samples per type
                # Customize template with business info
                if business_type == "restaurant":
                    customized = template.format(
                        business_name=business_name,
                        dish_name="Signature Pasta",
                        ingredients="local herbs",
                        cooking_tip="always taste as you cook",
                        nutrition_fact="herbs boost metabolism",
                        ingredient="fresh basil"
                    )
                elif business_type == "retail":
                    customized = template.format(
                        product_name="Summer Collection Dress",
                        occasion="summer events",
                        discount="25",
                        price="79.99",
                        styling_advice="pair with statement accessories",
                        product_type="delicate fabrics",
                        trend_name="sustainable fashion",
                        product_line="eco-friendly basics"
                    )
                else:  # service
                    customized = template.format(
                        service_name="Business Consulting",
                        client_type="small business",
                        result="40% revenue growth",
                        tip="Focus on customer retention over acquisition",
                        business_area="operations",
                        statistic="85% of businesses lack digital strategy",
                        business_process="customer onboarding",
                        strategy_name="digital transformation",
                        industry="professional services"
                    )
                
                sample_content[content_type].append(customized)
        
        return {
            "sample_posts": sample_content,
            "visual_suggestions": self._generate_visual_suggestions(business_type),
            "hashtag_examples": self._generate_hashtag_examples(business_type, business_info),
            "call_to_action_examples": self._generate_cta_examples(business_type)
        }
    
    def _generate_visual_suggestions(self, business_type: str) -> List[str]:
        """Generate visual content suggestions."""
        suggestions = {
            "restaurant": [
                "High-quality food photography with natural lighting",
                "Behind-the-scenes kitchen videos",
                "Customer dining experience photos",
                "Ingredient close-ups and preparation videos",
                "Chef portraits and cooking action shots"
            ],
            "retail": [
                "Product photography with lifestyle settings",
                "Flat lay styling arrangements",
                "Customer wearing/using products",
                "Store interior and product displays",
                "Before/after styling transformations"
            ],
            "service": [
                "Professional team photos",
                "Client testimonial graphics",
                "Industry infographics and charts",
                "Office/workspace photos",
                "Process explanation graphics"
            ]
        }
        return suggestions.get(business_type, suggestions["service"])
    
    def _generate_hashtag_examples(self, business_type: str, business_info: Dict[str, Any]) -> List[str]:
        """Generate hashtag examples."""
        business_name = business_info["name"].replace(" ", "").lower()
        city = business_info["location"]["city"].lower()
        
        base_hashtags = [
            f"#{business_name}",
            f"#{city}{business_type}",
            f"#{city}business",
            "#local",
            "#smallbusiness"
        ]
        
        type_hashtags = {
            "restaurant": ["#food", "#dining", "#restaurant", "#delicious", "#fresh"],
            "retail": ["#shopping", "#style", "#fashion", "#retail", "#boutique"],
            "service": ["#professional", "#expert", "#consulting", "#business", "#service"]
        }
        
        return base_hashtags + type_hashtags.get(business_type, type_hashtags["service"])
    
    def _generate_cta_examples(self, business_type: str) -> List[str]:
        """Generate call-to-action examples."""
        ctas = {
            "restaurant": [
                "Book your table now!",
                "Order online for delivery",
                "Try our chef's special today",
                "Reserve for the weekend",
                "Taste the difference - visit us!"
            ],
            "retail": [
                "Shop the collection now",
                "Visit our store today",
                "Limited time - don't miss out!",
                "Get yours before they're gone",
                "Discover your new favorite"
            ],
            "service": [
                "Schedule your consultation",
                "Contact us for more info",
                "Let's discuss your needs",
                "Book a free assessment",
                "Ready to get started?"
            ]
        }
        return ctas.get(business_type, ctas["service"])
    
    async def _create_social_media_files(
        self, social_strategy: Dict[str, Any], content_calendar: Dict[str, Any], 
        sample_content: Dict[str, Any], business_info: Dict[str, Any]
    ) -> List[str]:
        """Create social media files on disk."""
        business_name = business_info["name"]
        safe_name = business_name.lower().replace(" ", "_").replace("-", "_")
        
        social_dir = self.output_directory / safe_name
        social_dir.mkdir(exist_ok=True)
        
        generated_files = []
        
        # Create social media strategy file
        strategy_file = social_dir / "social_media_strategy.json"
        with open(strategy_file, 'w', encoding='utf-8') as f:
            json.dump(social_strategy, f, indent=2, ensure_ascii=False)
        generated_files.append(str(strategy_file))
        
        # Create content calendar file
        calendar_file = social_dir / "content_calendar.json"
        with open(calendar_file, 'w', encoding='utf-8') as f:
            json.dump(content_calendar, f, indent=2, ensure_ascii=False)
        generated_files.append(str(calendar_file))
        
        # Create sample content file
        content_file = social_dir / "sample_content.md"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(f"# Sample Social Media Content for {business_name}\n\n")
            
            for content_type, posts in sample_content["sample_posts"].items():
                f.write(f"## {content_type.title()} Content\n\n")
                for i, post in enumerate(posts, 1):
                    f.write(f"### Post {i}\n")
                    f.write(f"{post}\n\n")
                    f.write(f"**Hashtags:** {' '.join(sample_content['hashtag_examples'][:10])}\n\n")
                    f.write("---\n\n")
        generated_files.append(str(content_file))
        
        # Create posting schedule file
        schedule_file = social_dir / "posting_schedule.md"
        with open(schedule_file, 'w', encoding='utf-8') as f:
            f.write(f"# Social Media Posting Schedule for {business_name}\n\n")
            f.write(f"## Platform Schedules\n\n")
            
            for platform, schedule in social_strategy["posting_schedule"]["platform_schedules"].items():
                f.write(f"### {platform.title()}\n")
                f.write(f"- **Frequency:** {schedule['frequency']}\n")
                f.write(f"- **Weekly Posts:** {schedule['weekly_posts']}\n")
                f.write(f"- **Best Times:** {', '.join(schedule['best_times'])}\n")
                f.write(f"- **Content Types:** {', '.join(schedule['content_types'])}\n\n")
        generated_files.append(str(schedule_file))
        
        # Create hashtag strategy file
        hashtag_file = social_dir / "hashtag_strategy.md"
        with open(hashtag_file, 'w', encoding='utf-8') as f:
            f.write(f"# Hashtag Strategy for {business_name}\n\n")
            
            for category, tags in social_strategy["hashtag_strategy"]["hashtag_categories"].items():
                f.write(f"## {category.title()} Hashtags\n")
                for tag in tags:
                    f.write(f"- {tag}\n")
                f.write("\n")
            
            f.write(f"## Usage Guidelines\n")
            f.write(f"- {social_strategy['hashtag_strategy']['hashtag_mix']}\n")
            f.write(f"- {social_strategy['hashtag_strategy']['hashtag_research']}\n")
            f.write(f"- {social_strategy['hashtag_strategy']['hashtag_performance']}\n")
        generated_files.append(str(hashtag_file))
        
        return generated_files
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": self.agent_name,
            "status": "active" if self.is_initialized else "inactive",
            "supported_platforms": list(self.platforms.keys()),
            "business_types": ["restaurant", "retail", "service"],
            "features": ["content_creation", "scheduling", "hashtag_strategy", "analytics", "engagement"]
        }
    
    async def shutdown(self):
        """Shutdown the agent."""
        self.is_initialized = False
        logger.info("Real Social Media Agent shutdown")
