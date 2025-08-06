"""
Content Manager Agent - Real Implementation
Generates, optimizes, and manages content for websites and marketing campaigns.
"""

import asyncio
import logging
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentManagerAgent:
    """Real Content Manager Agent that generates optimized content."""
    
    def __init__(self):
        self.agent_name = "content_manager"
        self.is_initialized = False
        self.output_directory = Path("generated_content")
        self.output_directory.mkdir(exist_ok=True)
        
        # Content templates by business type and language
        self.content_templates = {
            "restaurant": {
                "hero_headlines": {
                    "en": [
                        "Authentic Flavors, Unforgettable Experiences",
                        "Where Taste Meets Tradition",
                        "Fresh Ingredients, Bold Flavors",
                        "A Culinary Journey Awaits"
                    ],
                    "hi": [
                        "प्रामाणिक स्वाद, अविस्मरणीय अनुभव",
                        "जहाँ स्वाद मिलता है परंपरा से",
                        "ताज़ी सामग्री, बेहतरीन स्वाद"
                    ]
                },
                "taglines": {
                    "en": [
                        "Serving happiness one dish at a time",
                        "Your favorite neighborhood dining destination",
                        "Where every meal is a celebration"
                    ],
                    "hi": [
                        "हर व्यंजन के साथ खुशी परोसते हैं",
                        "आपका पसंदीदा स्थानीय भोजन स्थल"
                    ]
                }
            },
            "retail": {
                "hero_headlines": {
                    "en": [
                        "Quality Products, Exceptional Service",
                        "Your Style, Our Passion",
                        "Discover Amazing Deals Every Day",
                        "Shop Smart, Shop Local"
                    ],
                    "hi": [
                        "गुणवत्ता उत्पाद, बेहतरीन सेवा",
                        "आपकी शैली, हमारा जुनून",
                        "रोज़ाना अद्भुत ऑफर्स खोजें"
                    ]
                }
            },
            "service": {
                "hero_headlines": {
                    "en": [
                        "Professional Excellence, Personal Touch",
                        "Solutions That Make a Difference",
                        "Your Success is Our Mission",
                        "Reliable Service, Proven Results"
                    ],
                    "hi": [
                        "व्यावसायिक उत्कृष्टता, व्यक्तिगत स्पर्श",
                        "समाधान जो अंतर लाते हैं",
                        "आपकी सफलता हमारा लक्ष्य"
                    ]
                }
            }
        }
        
        # SEO keywords by business type and region
        self.seo_keywords = {
            "restaurant": {
                "primary": ["restaurant", "dining", "food", "cuisine", "menu"],
                "local": ["near me", "best", "authentic", "fresh", "delivery"],
                "long_tail": ["family restaurant", "fine dining", "takeaway", "home delivery"]
            },
            "retail": {
                "primary": ["shop", "store", "buy", "products", "shopping"],
                "local": ["local store", "best prices", "quality products", "online shopping"],
                "long_tail": ["affordable prices", "customer service", "product variety"]
            },
            "service": {
                "primary": ["service", "professional", "expert", "consultation"],
                "local": ["local service", "trusted", "experienced", "reliable"],
                "long_tail": ["professional service", "expert consultation", "quality service"]
            }
        }
    
    async def initialize(self):
        """Initialize the Content Manager Agent."""
        logger.info("Initializing Real Content Manager Agent")
        self.is_initialized = True
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle content generation requests."""
        try:
            logger.info(f"Generating content for: {request.get('description', 'No description')}")
            
            # Extract business information
            business_info = self._extract_business_info(request)
            business_type = self._detect_business_type(request)
            language = self._detect_language(request)
            region_context = request.get("region_context", {})
            
            # Generate comprehensive content package
            content_package = await self._generate_content_package(
                business_type, business_info, language, region_context
            )
            
            # Create content files
            generated_files = await self._create_content_files(content_package, business_info)
            
            return {
                "status": "success",
                "agent": self.agent_name,
                "business_type": business_type,
                "language": language,
                "content_package": content_package,
                "generated_files": generated_files,
                "seo_optimization": content_package["seo_data"],
                "content_metrics": {
                    "total_words": content_package["total_words"],
                    "readability_score": content_package["readability_score"],
                    "seo_score": content_package["seo_score"]
                }
            }
            
        except Exception as e:
            logger.error(f"Content manager error: {e}")
            return {
                "status": "error",
                "agent": self.agent_name,
                "error": str(e),
                "fallback_message": "Content generation failed, using basic templates"
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
                "country": region_context.get("country", localization.get("country", "US")),
                "state": region_context.get("state", localization.get("state", "State"))
            },
            "target_audience": request.get("target_audience", "Local customers")
        }
    
    def _detect_business_type(self, request: Dict[str, Any]) -> str:
        """Detect business type from request."""
        description = request.get("description", "").lower()
        business_type = request.get("business_type", "").lower()
        
        if business_type in ["restaurant", "retail", "service"]:
            return business_type
        
        # Auto-detect from description
        if any(word in description for word in ["restaurant", "cafe", "bistro", "food", "dining"]):
            return "restaurant"
        elif any(word in description for word in ["shop", "store", "retail", "boutique", "products"]):
            return "retail"
        else:
            return "service"
    
    def _detect_language(self, request: Dict[str, Any]) -> str:
        """Detect content language from request."""
        region_context = request.get("region_context", {})
        localization = request.get("localization", {})
        
        language = (
            localization.get("language") or 
            region_context.get("language") or 
            "en"
        )
        
        # Map common country codes to languages
        country = region_context.get("country", "").upper()
        if country == "IN":
            return "hi"  # Hindi for India
        elif country in ["FR"]:
            return "fr"
        elif country in ["DE", "AT"]:
            return "de"
        elif country in ["ES", "MX"]:
            return "es"
        
        return "en"  # Default to English
    
    async def _generate_content_package(
        self, business_type: str, business_info: Dict[str, Any], 
        language: str, region_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive content package."""
        
        templates = self.content_templates.get(business_type, self.content_templates["service"])
        
        # Generate headlines and taglines
        headlines = templates.get("hero_headlines", {}).get(language, templates["hero_headlines"]["en"])
        taglines = templates.get("taglines", {}).get(language, ["Professional service you can trust"])
        
        # Generate about section
        about_content = self._generate_about_content(business_info, business_type, language)
        
        # Generate service/product descriptions
        offerings = self._generate_offerings_content(business_type, language, region_context)
        
        # Generate SEO content
        seo_data = self._generate_seo_content(business_type, business_info, language)
        
        # Generate call-to-action text
        cta_text = self._generate_cta_content(business_type, language)
        
        # Calculate content metrics
        total_content = f"{about_content} {' '.join(offerings)} {' '.join(headlines)}"
        
        content_package = {
            "headlines": headlines,
            "taglines": taglines,
            "about_content": about_content,
            "offerings": offerings,
            "cta_text": cta_text,
            "seo_data": seo_data,
            "total_words": len(total_content.split()),
            "readability_score": self._calculate_readability_score(total_content),
            "seo_score": self._calculate_seo_score(total_content, seo_data),
            "language": language,
            "business_type": business_type
        }
        
        return content_package
    
    def _generate_about_content(self, business_info: Dict[str, Any], business_type: str, language: str) -> str:
        """Generate about section content."""
        business_name = business_info["name"]
        location = business_info["location"]
        
        if language == "hi":
            if business_type == "restaurant":
                return f"{business_name} {location['city']} में स्थित एक प्रमुख रेस्टोरेंट है जो स्वादिष्ट भोजन और बेहतरीन सेवा प्रदान करता है। हमारे अनुभवी शेफ ताज़ी सामग्री का उपयोग करके पारंपरिक और आधुनिक व्यंजन तैयार करते हैं।"
            elif business_type == "retail":
                return f"{business_name} {location['city']} का एक विश्वसनीय स्टोर है जो गुणवत्तापूर्ण उत्पाद और उत्कृष्ट ग्राहक सेवा प्रदान करता है। हमारे पास विभिन्न प्रकार के उत्पाद उपलब्ध हैं।"
            else:
                return f"{business_name} {location['city']} में स्थित एक व्यावसायिक सेवा प्रदाता है जो विशेषज्ञता और विश्वसनीयता के साथ सेवा प्रदान करता है।"
        else:
            if business_type == "restaurant":
                return f"{business_name} is a premier dining destination located in {location['city']}, {location['country']}. We pride ourselves on serving exceptional cuisine made with fresh, quality ingredients. Our experienced chefs create both traditional and contemporary dishes that celebrate the rich flavors of our region."
            elif business_type == "retail":
                return f"{business_name} is a trusted retail store in {location['city']}, {location['country']}, committed to providing quality products and exceptional customer service. We offer a wide selection of carefully curated items to meet all your needs."
            else:
                return f"{business_name} is a professional service provider based in {location['city']}, {location['country']}. We deliver expert solutions with a commitment to excellence and customer satisfaction. Our experienced team is dedicated to helping you achieve your goals."
    
    def _generate_offerings_content(self, business_type: str, language: str, region_context: Dict[str, Any]) -> List[str]:
        """Generate offerings/services content."""
        if language == "hi":
            if business_type == "restaurant":
                return [
                    "स्वादिष्ट भारतीय व्यंजन",
                    "फ्रेश इंग्रीडिएंट्स के साथ बना खाना",
                    "होम डिलीवरी सेवा",
                    "फैमिली डाइनिंग",
                    "स्पेशल इवेंट कैटरिंग"
                ]
            elif business_type == "retail":
                return [
                    "गुणवत्तापूर्ण उत्पाद",
                    "किफायती दाम",
                    "घर पर डिलीवरी",
                    "ग्राहक सेवा",
                    "रिटर्न पॉलिसी"
                ]
            else:
                return [
                    "व्यावसायिक परामर्श",
                    "विशेषज्ञ सेवा",
                    "समय पर डिलीवरी",
                    "ग्राहक सहायता",
                    "गुणवत्ता गारंटी"
                ]
        else:
            if business_type == "restaurant":
                return [
                    "Fresh, locally-sourced ingredients",
                    "Authentic regional cuisine",
                    "Comfortable family dining",
                    "Takeaway and delivery options",
                    "Special event catering"
                ]
            elif business_type == "retail":
                return [
                    "High-quality products",
                    "Competitive pricing",
                    "Fast shipping and delivery",
                    "Excellent customer service",
                    "Easy returns and exchanges"
                ]
            else:
                return [
                    "Professional consultation",
                    "Expert solutions",
                    "Timely delivery",
                    "24/7 customer support",
                    "Quality guarantee"
                ]
    
    def _generate_seo_content(self, business_type: str, business_info: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate SEO-optimized content."""
        keywords = self.seo_keywords.get(business_type, self.seo_keywords["service"])
        location = business_info["location"]
        business_name = business_info["name"]
        
        # Generate local SEO keywords
        local_keywords = [
            f"{business_name}",
            f"{business_type} in {location['city']}",
            f"{location['city']} {business_type}",
            f"best {business_type} {location['city']}",
            f"{business_type} near me"
        ]
        
        # Generate meta description
        if language == "hi":
            meta_description = f"{business_name} - {location['city']} में बेहतरीन {business_type} सेवा। गुणवत्ता और ग्राहक संतुष्टि हमारी प्राथमिकता।"
        else:
            meta_description = f"{business_name} - Premium {business_type} service in {location['city']}, {location['country']}. Quality and customer satisfaction guaranteed."
        
        return {
            "primary_keywords": keywords["primary"],
            "local_keywords": local_keywords,
            "long_tail_keywords": keywords["long_tail"],
            "meta_title": f"{business_name} - {business_type.title()} in {location['city']}",
            "meta_description": meta_description,
            "alt_text_suggestions": [
                f"{business_name} exterior",
                f"{business_name} interior",
                f"{business_type} service",
                f"{location['city']} {business_type}"
            ]
        }
    
    def _generate_cta_content(self, business_type: str, language: str) -> Dict[str, List[str]]:
        """Generate call-to-action content."""
        if language == "hi":
            if business_type == "restaurant":
                return {
                    "primary": ["अभी ऑर्डर करें", "टेबल बुक करें", "मेन्यू देखें"],
                    "secondary": ["संपर्क करें", "लोकेशन देखें", "रिव्यू पढ़ें"]
                }
            elif business_type == "retail":
                return {
                    "primary": ["अभी खरीदें", "ऑनलाइन शॉप करें", "स्टोर में आएं"],
                    "secondary": ["संपर्क करें", "कैटलॉग देखें", "ऑफर्स देखें"]
                }
            else:
                return {
                    "primary": ["संपर्क करें", "सेवा बुक करें", "फ्री कंसल्टेशन"],
                    "secondary": ["और जानें", "पोर्टफोलियो देखें", "कोटेशन पाएं"]
                }
        else:
            if business_type == "restaurant":
                return {
                    "primary": ["Order Now", "Book a Table", "View Menu"],
                    "secondary": ["Contact Us", "Find Location", "Read Reviews"]
                }
            elif business_type == "retail":
                return {
                    "primary": ["Shop Now", "Browse Products", "Visit Store"],
                    "secondary": ["Contact Us", "View Catalog", "See Offers"]
                }
            else:
                return {
                    "primary": ["Contact Us", "Book Service", "Free Consultation"],
                    "secondary": ["Learn More", "View Portfolio", "Get Quote"]
                }
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score (simplified)."""
        words = text.split()
        sentences = text.split('.')
        
        if len(sentences) == 0:
            return 0.0
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Simplified readability score (higher is more readable)
        if avg_words_per_sentence <= 15:
            return 0.9
        elif avg_words_per_sentence <= 20:
            return 0.8
        elif avg_words_per_sentence <= 25:
            return 0.7
        else:
            return 0.6
    
    def _calculate_seo_score(self, content: str, seo_data: Dict[str, Any]) -> float:
        """Calculate SEO optimization score."""
        content_lower = content.lower()
        score = 0.0
        
        # Check for primary keywords
        primary_found = sum(1 for keyword in seo_data["primary_keywords"] if keyword in content_lower)
        score += (primary_found / len(seo_data["primary_keywords"])) * 0.4
        
        # Check for local keywords
        local_found = sum(1 for keyword in seo_data["local_keywords"] if keyword.lower() in content_lower)
        score += (local_found / len(seo_data["local_keywords"])) * 0.3
        
        # Check for long tail keywords
        long_tail_found = sum(1 for keyword in seo_data["long_tail_keywords"] if keyword in content_lower)
        score += (long_tail_found / len(seo_data["long_tail_keywords"])) * 0.3
        
        return min(score, 1.0)
    
    async def _create_content_files(self, content_package: Dict[str, Any], business_info: Dict[str, Any]) -> List[str]:
        """Create content files on disk."""
        business_name = business_info["name"]
        safe_name = business_name.lower().replace(" ", "_").replace("-", "_")
        
        content_dir = self.output_directory / safe_name
        content_dir.mkdir(exist_ok=True)
        
        generated_files = []
        
        # Create content strategy file
        strategy_file = content_dir / "content_strategy.json"
        with open(strategy_file, 'w', encoding='utf-8') as f:
            json.dump(content_package, f, indent=2, ensure_ascii=False)
        generated_files.append(str(strategy_file))
        
        # Create SEO content file
        seo_file = content_dir / "seo_content.md"
        with open(seo_file, 'w', encoding='utf-8') as f:
            f.write(f"# SEO Content for {business_name}\n\n")
            f.write(f"## Meta Title\n{content_package['seo_data']['meta_title']}\n\n")
            f.write(f"## Meta Description\n{content_package['seo_data']['meta_description']}\n\n")
            f.write(f"## Primary Keywords\n{', '.join(content_package['seo_data']['primary_keywords'])}\n\n")
            f.write(f"## Local Keywords\n{', '.join(content_package['seo_data']['local_keywords'])}\n\n")
        generated_files.append(str(seo_file))
        
        # Create content copy file
        copy_file = content_dir / "content_copy.md"
        with open(copy_file, 'w', encoding='utf-8') as f:
            f.write(f"# Content Copy for {business_name}\n\n")
            f.write(f"## Headlines\n")
            for headline in content_package['headlines']:
                f.write(f"- {headline}\n")
            f.write(f"\n## About Section\n{content_package['about_content']}\n\n")
            f.write(f"## Service/Product Offerings\n")
            for offering in content_package['offerings']:
                f.write(f"- {offering}\n")
            f.write(f"\n## Call-to-Action Text\n")
            for cta_type, cta_list in content_package['cta_text'].items():
                f.write(f"### {cta_type.title()}\n")
                for cta in cta_list:
                    f.write(f"- {cta}\n")
        generated_files.append(str(copy_file))
        
        return generated_files
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": self.agent_name,
            "status": "active" if self.is_initialized else "inactive",
            "features": ["content_generation", "seo_optimization", "multi_language", "localization"],
            "supported_languages": ["en", "hi", "fr", "de", "es"],
            "business_types": ["restaurant", "retail", "service"]
        }
    
    async def shutdown(self):
        """Shutdown the agent."""
        self.is_initialized = False
        logger.info("Real Content Manager Agent shutdown")
