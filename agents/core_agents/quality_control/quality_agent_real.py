"""
Quality Control Agent - Real Implementation
Validates outputs, performs quality checks, and ensures enterprise-grade standards.
"""

import asyncio
import logging
import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

class QualityControlAgent:
    """Real Quality Control Agent that validates and scores all agent outputs."""
    
    def __init__(self):
        self.agent_name = "quality_control"
        self.is_initialized = False
        self.output_directory = Path("quality_reports")
        self.output_directory.mkdir(exist_ok=True)
        
        # Quality scoring weights
        self.quality_weights = {
            "content_completeness": 0.25,
            "technical_accuracy": 0.20,
            "business_relevance": 0.20,
            "language_quality": 0.15,
            "format_compliance": 0.10,
            "actionability": 0.10
        }
        
        # Content validation rules
        self.validation_rules = {
            "content_manager": {
                "required_sections": ["strategy", "content", "seo_keywords"],
                "min_content_length": 500,
                "max_content_length": 5000,
                "required_languages": ["english"],
                "seo_requirements": ["keywords", "meta_description", "readability_score"]
            },
            "seo_optimizer": {
                "required_sections": ["keyword_strategy", "technical_seo", "local_seo"],
                "min_keywords": 10,
                "required_schema_types": ["LocalBusiness"],
                "technical_checks": ["https", "mobile_optimization", "page_speed"],
                "local_seo_elements": ["google_my_business", "local_citations"]
            },
            "social_media": {
                "required_platforms": 2,
                "min_content_samples": 3,
                "hashtag_requirements": ["branded", "local", "industry"],
                "content_types": ["promotional", "educational", "engagement"],
                "posting_frequency": ["daily", "weekly", "bi-weekly"]
            }
        }
        
        # Business type specific quality standards
        self.business_standards = {
            "restaurant": {
                "required_elements": ["menu", "location", "hours", "contact"],
                "content_themes": ["food", "ambiance", "service", "local"],
                "seo_focus": ["local_search", "food_keywords", "review_management"],
                "social_platforms": ["instagram", "facebook", "tiktok"]
            },
            "retail": {
                "required_elements": ["products", "pricing", "shipping", "returns"],
                "content_themes": ["products", "lifestyle", "brand", "customer"],
                "seo_focus": ["product_keywords", "ecommerce_seo", "local_inventory"],
                "social_platforms": ["instagram", "facebook", "pinterest"]
            },
            "service": {
                "required_elements": ["services", "expertise", "testimonials", "contact"],
                "content_themes": ["expertise", "results", "process", "industry"],
                "seo_focus": ["service_keywords", "local_seo", "authority_building"],
                "social_platforms": ["linkedin", "facebook", "twitter"]
            }
        }
        
        # Language quality patterns
        self.language_patterns = {
            "professional_tone": r"(\bwe\b|\bour\b|\bprofessional\b|\bexpertise\b|\bquality\b)",
            "action_words": r"(\bbook\b|\bcall\b|\bcontact\b|\bvisit\b|\bexplore\b|\bdiscover\b)",
            "local_references": r"(\blocal\b|\bcommunity\b|\bneighborhood\b|\bcity\b|\barea\b)",
            "business_keywords": r"(\bservice\b|\bcustomer\b|\bexperience\b|\bsolution\b)"
        }
        
        # Common quality issues to detect
        self.quality_issues = {
            "placeholder_text": [r"\[.*\]", r"\{.*\}", r"TODO", r"PLACEHOLDER", r"XXX"],
            "poor_formatting": [r"^\s*$", r"^.{1,10}$", r"\.{3,}"],
            "generic_content": [r"\bYour Business\b", r"\bSample.*\b", r"\bExample.*\b"],
            "incomplete_sentences": [r"[A-Z][^.!?]*$", r"^[^A-Z]"],
            "missing_contact_info": [r"contact", r"phone", r"email", r"address"]
        }
    
    async def initialize(self):
        """Initialize the Quality Control Agent."""
        logger.info("Initializing Real Quality Control Agent")
        self.is_initialized = True
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle quality control validation requests."""
        try:
            logger.info(f"Performing quality control on: {request.get('validation_target', 'Unknown')}")
            
            # Extract validation targets
            validation_data = self._extract_validation_data(request)
            business_type = request.get("business_type", "service")
            
            # Perform comprehensive quality check
            quality_report = await self._perform_quality_check(validation_data, business_type)
            
            # Generate improvement recommendations
            recommendations = self._generate_recommendations(quality_report)
            
            # Create quality report files
            generated_files = await self._create_quality_files(quality_report, recommendations, validation_data)
            
            return {
                "status": "success",
                "agent": self.agent_name,
                "overall_score": quality_report["overall_score"],
                "quality_grade": quality_report["quality_grade"],
                "validation_results": quality_report["validation_results"],
                "recommendations": recommendations,
                "generated_files": generated_files,
                "compliance_status": quality_report["compliance_status"],
                "next_actions": quality_report["next_actions"]
            }
            
        except Exception as e:
            logger.error(f"Quality control error: {e}")
            return {
                "status": "error",
                "agent": self.agent_name,
                "error": str(e),
                "fallback_message": "Quality control validation failed, manual review recommended"
            }
    
    def _extract_validation_data(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data to be validated from request."""
        return {
            "content_manager_output": request.get("content_manager_output", {}),
            "seo_optimizer_output": request.get("seo_optimizer_output", {}),
            "social_media_output": request.get("social_media_output", {}),
            "business_info": request.get("business_info", {}),
            "generated_files": request.get("generated_files", []),
            "agent_responses": request.get("agent_responses", {})
        }
    
    async def _perform_quality_check(self, validation_data: Dict[str, Any], business_type: str) -> Dict[str, Any]:
        """Perform comprehensive quality validation."""
        
        validation_results = {}
        
        # Validate Content Manager output
        if validation_data.get("content_manager_output"):
            validation_results["content_manager"] = self._validate_content_manager(
                validation_data["content_manager_output"], business_type
            )
        
        # Validate SEO Optimizer output
        if validation_data.get("seo_optimizer_output"):
            validation_results["seo_optimizer"] = self._validate_seo_optimizer(
                validation_data["seo_optimizer_output"], business_type
            )
        
        # Validate Social Media output
        if validation_data.get("social_media_output"):
            validation_results["social_media"] = self._validate_social_media(
                validation_data["social_media_output"], business_type
            )
        
        # Cross-agent consistency check
        consistency_check = self._validate_cross_agent_consistency(validation_data)
        
        # Calculate overall scores
        overall_score = self._calculate_overall_score(validation_results)
        quality_grade = self._determine_quality_grade(overall_score)
        compliance_status = self._determine_compliance_status(validation_results)
        
        return {
            "validation_results": validation_results,
            "consistency_check": consistency_check,
            "overall_score": overall_score,
            "quality_grade": quality_grade,
            "compliance_status": compliance_status,
            "next_actions": self._generate_next_actions(overall_score, validation_results),
            "validation_timestamp": datetime.now().isoformat()
        }
    
    def _validate_content_manager(self, output: Dict[str, Any], business_type: str) -> Dict[str, Any]:
        """Validate Content Manager agent output."""
        rules = self.validation_rules["content_manager"]
        standards = self.business_standards[business_type]
        
        validation_result = {
            "agent": "content_manager",
            "score": 0.0,
            "issues": [],
            "passed_checks": [],
            "failed_checks": []
        }
        
        # Check required sections
        content_strategy = output.get("content_strategy", {})
        required_sections = rules["required_sections"]
        
        for section in required_sections:
            if section in content_strategy:
                validation_result["passed_checks"].append(f"Required section '{section}' present")
            else:
                validation_result["failed_checks"].append(f"Missing required section '{section}'")
                validation_result["issues"].append(f"Content strategy missing '{section}' section")
        
        # Check content quality
        generated_content = output.get("generated_content", {})
        if generated_content:
            content_length = len(str(generated_content))
            if rules["min_content_length"] <= content_length <= rules["max_content_length"]:
                validation_result["passed_checks"].append("Content length within acceptable range")
            else:
                validation_result["failed_checks"].append(f"Content length {content_length} outside range {rules['min_content_length']}-{rules['max_content_length']}")
        
        # Check language quality
        language_score = self._assess_language_quality(str(generated_content))
        if language_score >= 0.7:
            validation_result["passed_checks"].append("Language quality acceptable")
        else:
            validation_result["failed_checks"].append("Language quality below threshold")
            validation_result["issues"].append("Content may contain generic or placeholder text")
        
        # Check business type alignment
        content_themes = content_strategy.get("content_themes", [])
        expected_themes = standards["content_themes"]
        theme_overlap = len(set(content_themes) & set(expected_themes))
        
        if theme_overlap >= 2:
            validation_result["passed_checks"].append("Content themes align with business type")
        else:
            validation_result["failed_checks"].append("Content themes don't align well with business type")
        
        # Calculate score
        total_checks = len(validation_result["passed_checks"]) + len(validation_result["failed_checks"])
        if total_checks > 0:
            validation_result["score"] = len(validation_result["passed_checks"]) / total_checks
        
        return validation_result
    
    def _validate_seo_optimizer(self, output: Dict[str, Any], business_type: str) -> Dict[str, Any]:
        """Validate SEO Optimizer agent output."""
        rules = self.validation_rules["seo_optimizer"]
        standards = self.business_standards[business_type]
        
        validation_result = {
            "agent": "seo_optimizer",
            "score": 0.0,
            "issues": [],
            "passed_checks": [],
            "failed_checks": []
        }
        
        seo_strategy = output.get("seo_strategy", {})
        
        # Check required sections
        for section in rules["required_sections"]:
            if section in seo_strategy:
                validation_result["passed_checks"].append(f"Required section '{section}' present")
            else:
                validation_result["failed_checks"].append(f"Missing required section '{section}'")
        
        # Check keyword strategy
        keyword_strategy = seo_strategy.get("keyword_strategy", {})
        primary_keywords = keyword_strategy.get("primary_keywords", [])
        
        if len(primary_keywords) >= rules["min_keywords"]:
            validation_result["passed_checks"].append("Sufficient number of keywords")
        else:
            validation_result["failed_checks"].append(f"Only {len(primary_keywords)} keywords, need {rules['min_keywords']}")
        
        # Check technical SEO elements
        technical_seo = seo_strategy.get("technical_seo", {})
        for check in rules["technical_checks"]:
            if check in str(technical_seo).lower():
                validation_result["passed_checks"].append(f"Technical SEO includes {check}")
            else:
                validation_result["failed_checks"].append(f"Missing technical SEO element: {check}")
        
        # Check local SEO
        local_seo = seo_strategy.get("local_seo", {})
        for element in rules["local_seo_elements"]:
            if element in str(local_seo).lower():
                validation_result["passed_checks"].append(f"Local SEO includes {element}")
            else:
                validation_result["failed_checks"].append(f"Missing local SEO element: {element}")
        
        # Check optimization score
        optimization_score = output.get("optimization_score", 0)
        if optimization_score >= 0.7:
            validation_result["passed_checks"].append("High optimization score")
        elif optimization_score >= 0.5:
            validation_result["passed_checks"].append("Moderate optimization score")
        else:
            validation_result["failed_checks"].append("Low optimization score")
            validation_result["issues"].append("SEO strategy may need improvement")
        
        # Calculate score
        total_checks = len(validation_result["passed_checks"]) + len(validation_result["failed_checks"])
        if total_checks > 0:
            validation_result["score"] = len(validation_result["passed_checks"]) / total_checks
        
        return validation_result
    
    def _validate_social_media(self, output: Dict[str, Any], business_type: str) -> Dict[str, Any]:
        """Validate Social Media agent output."""
        rules = self.validation_rules["social_media"]
        standards = self.business_standards[business_type]
        
        validation_result = {
            "agent": "social_media",
            "score": 0.0,
            "issues": [],
            "passed_checks": [],
            "failed_checks": []
        }
        
        social_strategy = output.get("social_strategy", {})
        
        # Check platform selection
        recommended_platforms = social_strategy.get("recommended_platforms", [])
        if len(recommended_platforms) >= rules["required_platforms"]:
            validation_result["passed_checks"].append("Sufficient number of platforms selected")
        else:
            validation_result["failed_checks"].append(f"Only {len(recommended_platforms)} platforms, need {rules['required_platforms']}")
        
        # Check platform alignment with business type
        expected_platforms = standards["social_platforms"]
        platform_overlap = len(set(recommended_platforms) & set(expected_platforms))
        
        if platform_overlap >= 2:
            validation_result["passed_checks"].append("Platform selection aligns with business type")
        else:
            validation_result["failed_checks"].append("Platform selection doesn't align well with business type")
        
        # Check content samples
        sample_content = output.get("sample_content", {})
        content_samples = sample_content.get("sample_posts", {})
        
        total_samples = sum(len(posts) for posts in content_samples.values())
        if total_samples >= rules["min_content_samples"]:
            validation_result["passed_checks"].append("Sufficient content samples provided")
        else:
            validation_result["failed_checks"].append(f"Only {total_samples} content samples, need {rules['min_content_samples']}")
        
        # Check content type coverage
        content_types = list(content_samples.keys())
        required_types = rules["content_types"]
        type_coverage = len(set(content_types) & set(required_types))
        
        if type_coverage >= 3:
            validation_result["passed_checks"].append("Good content type coverage")
        else:
            validation_result["failed_checks"].append("Limited content type coverage")
        
        # Check hashtag strategy
        hashtag_strategy = social_strategy.get("hashtag_strategy", {})
        hashtag_categories = hashtag_strategy.get("hashtag_categories", {})
        
        for category in rules["hashtag_requirements"]:
            if category in hashtag_categories:
                validation_result["passed_checks"].append(f"Hashtag strategy includes {category} hashtags")
            else:
                validation_result["failed_checks"].append(f"Missing {category} hashtags in strategy")
        
        # Check engagement score
        engagement_score = output.get("engagement_score", 0)
        if engagement_score >= 0.7:
            validation_result["passed_checks"].append("High predicted engagement score")
        elif engagement_score >= 0.5:
            validation_result["passed_checks"].append("Moderate predicted engagement score")
        else:
            validation_result["failed_checks"].append("Low predicted engagement score")
        
        # Calculate score
        total_checks = len(validation_result["passed_checks"]) + len(validation_result["failed_checks"])
        if total_checks > 0:
            validation_result["score"] = len(validation_result["passed_checks"]) / total_checks
        
        return validation_result
    
    def _validate_cross_agent_consistency(self, validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consistency across agent outputs."""
        consistency_result = {
            "score": 0.0,
            "issues": [],
            "passed_checks": [],
            "failed_checks": []
        }
        
        # Extract business information from different agents
        content_business = validation_data.get("content_manager_output", {}).get("business_info", {})
        seo_business = validation_data.get("seo_optimizer_output", {}).get("business_info", {})
        social_business = validation_data.get("social_media_output", {}).get("business_info", {})
        
        # Check business name consistency
        names = [
            content_business.get("name", ""),
            seo_business.get("name", ""),
            social_business.get("name", "")
        ]
        unique_names = set(filter(None, names))
        
        if len(unique_names) <= 1:
            consistency_result["passed_checks"].append("Business name consistent across agents")
        else:
            consistency_result["failed_checks"].append("Business name inconsistent across agents")
            consistency_result["issues"].append(f"Multiple business names found: {list(unique_names)}")
        
        # Check target audience alignment
        content_audience = content_business.get("target_audience", "")
        seo_keywords = validation_data.get("seo_optimizer_output", {}).get("seo_strategy", {}).get("keyword_strategy", {})
        social_platforms = validation_data.get("social_media_output", {}).get("social_strategy", {}).get("recommended_platforms", [])
        
        # Check if SEO keywords and social platforms align
        if seo_keywords and social_platforms:
            consistency_result["passed_checks"].append("SEO and social media strategies present")
        else:
            consistency_result["failed_checks"].append("Missing SEO or social media strategy alignment")
        
        # Check content theme consistency
        content_themes = validation_data.get("content_manager_output", {}).get("content_strategy", {}).get("content_themes", [])
        social_themes = validation_data.get("social_media_output", {}).get("social_strategy", {}).get("content_strategy", {}).get("content_themes", [])
        
        if content_themes and social_themes:
            theme_overlap = len(set(content_themes) & set(social_themes))
            if theme_overlap >= 2:
                consistency_result["passed_checks"].append("Content themes consistent between content and social media")
            else:
                consistency_result["failed_checks"].append("Content themes not well aligned between agents")
        
        # Calculate consistency score
        total_checks = len(consistency_result["passed_checks"]) + len(consistency_result["failed_checks"])
        if total_checks > 0:
            consistency_result["score"] = len(consistency_result["passed_checks"]) / total_checks
        
        return consistency_result
    
    def _assess_language_quality(self, content: str) -> float:
        """Assess language quality of content."""
        if not content:
            return 0.0
        
        quality_score = 0.0
        checks_performed = 0
        
        # Check for professional tone
        professional_matches = len(re.findall(self.language_patterns["professional_tone"], content, re.IGNORECASE))
        if professional_matches > 0:
            quality_score += 0.25
        checks_performed += 1
        
        # Check for action words
        action_matches = len(re.findall(self.language_patterns["action_words"], content, re.IGNORECASE))
        if action_matches > 0:
            quality_score += 0.25
        checks_performed += 1
        
        # Check for local references
        local_matches = len(re.findall(self.language_patterns["local_references"], content, re.IGNORECASE))
        if local_matches > 0:
            quality_score += 0.25
        checks_performed += 1
        
        # Check for business keywords
        business_matches = len(re.findall(self.language_patterns["business_keywords"], content, re.IGNORECASE))
        if business_matches > 0:
            quality_score += 0.25
        checks_performed += 1
        
        # Check for quality issues
        issue_penalty = 0.0
        for issue_type, patterns in self.quality_issues.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issue_penalty += 0.1
        
        final_score = max(0.0, (quality_score / checks_performed) - issue_penalty)
        return min(1.0, final_score)
    
    def _calculate_overall_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall quality score."""
        if not validation_results:
            return 0.0
        
        total_score = 0.0
        agent_count = 0
        
        for agent_name, result in validation_results.items():
            if isinstance(result, dict) and "score" in result:
                total_score += result["score"]
                agent_count += 1
        
        return total_score / agent_count if agent_count > 0 else 0.0
    
    def _determine_quality_grade(self, score: float) -> str:
        """Determine quality grade based on score."""
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B+ (Good)"
        elif score >= 0.6:
            return "B (Acceptable)"
        elif score >= 0.5:
            return "C (Needs Improvement)"
        else:
            return "D (Poor - Requires Revision)"
    
    def _determine_compliance_status(self, validation_results: Dict[str, Any]) -> str:
        """Determine overall compliance status."""
        if not validation_results:
            return "Unknown"
        
        total_failed = sum(
            len(result.get("failed_checks", [])) 
            for result in validation_results.values()
            if isinstance(result, dict)
        )
        
        total_passed = sum(
            len(result.get("passed_checks", []))
            for result in validation_results.values()
            if isinstance(result, dict)
        )
        
        if total_failed == 0:
            return "Fully Compliant"
        elif total_passed > total_failed:
            return "Mostly Compliant"
        elif total_passed == total_failed:
            return "Partially Compliant"
        else:
            return "Non-Compliant"
    
    def _generate_next_actions(self, overall_score: float, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommended next actions."""
        actions = []
        
        if overall_score < 0.6:
            actions.append("Requires immediate attention - major revisions needed")
            actions.append("Review all failed checks and address issues")
            actions.append("Consider re-running agents with improved inputs")
        elif overall_score < 0.8:
            actions.append("Address identified issues to improve quality")
            actions.append("Review failed checks and implement fixes")
            actions.append("Consider additional content or strategy refinements")
        else:
            actions.append("Quality is acceptable - proceed with minor refinements")
            actions.append("Address any remaining failed checks")
            actions.append("Ready for production deployment")
        
        # Add specific actions based on validation results
        for agent_name, result in validation_results.items():
            if isinstance(result, dict) and result.get("failed_checks"):
                actions.append(f"Fix {agent_name} issues: {len(result['failed_checks'])} checks failed")
        
        return actions[:5]  # Limit to top 5 actions
    
    def _generate_recommendations(self, quality_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement recommendations."""
        recommendations = []
        
        overall_score = quality_report["overall_score"]
        validation_results = quality_report["validation_results"]
        
        # Overall recommendations
        if overall_score < 0.5:
            recommendations.append({
                "priority": "High",
                "category": "Overall Quality",
                "issue": "Low overall quality score",
                "recommendation": "Review all agent outputs and re-generate content with better inputs",
                "impact": "Critical for business credibility"
            })
        
        # Agent-specific recommendations
        for agent_name, result in validation_results.items():
            if isinstance(result, dict):
                score = result.get("score", 0)
                failed_checks = result.get("failed_checks", [])
                issues = result.get("issues", [])
                
                if score < 0.7:
                    recommendations.append({
                        "priority": "High" if score < 0.5 else "Medium",
                        "category": f"{agent_name.replace('_', ' ').title()} Agent",
                        "issue": f"Quality score below threshold ({score:.2f})",
                        "recommendation": f"Address {len(failed_checks)} failed checks for {agent_name}",
                        "impact": "Affects overall deliverable quality"
                    })
                
                # Add specific issue recommendations
                for issue in issues[:2]:  # Top 2 issues per agent
                    recommendations.append({
                        "priority": "Medium",
                        "category": f"{agent_name.replace('_', ' ').title()} Content",
                        "issue": issue,
                        "recommendation": "Review and improve content quality",
                        "impact": "Improves professional appearance"
                    })
        
        # Consistency recommendations
        consistency_result = quality_report.get("consistency_check", {})
        if consistency_result.get("score", 1.0) < 0.8:
            recommendations.append({
                "priority": "High",
                "category": "Cross-Agent Consistency",
                "issue": "Inconsistencies found between agent outputs",
                "recommendation": "Ensure business information is consistent across all agents",
                "impact": "Critical for cohesive business presentation"
            })
        
        return sorted(recommendations, key=lambda x: {"High": 3, "Medium": 2, "Low": 1}[x["priority"]], reverse=True)
    
    async def _create_quality_files(
        self, quality_report: Dict[str, Any], recommendations: List[Dict[str, Any]], 
        validation_data: Dict[str, Any]
    ) -> List[str]:
        """Create quality control files on disk."""
        
        # Create unique report directory
        report_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        report_dir = self.output_directory / f"quality_report_{report_id}"
        report_dir.mkdir(exist_ok=True)
        
        generated_files = []
        
        # Create quality report file
        report_file = report_dir / "quality_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(quality_report, f, indent=2, ensure_ascii=False)
        generated_files.append(str(report_file))
        
        # Create recommendations file
        recommendations_file = report_dir / "recommendations.md"
        with open(recommendations_file, 'w', encoding='utf-8') as f:
            f.write(f"# Quality Control Recommendations\n\n")
            f.write(f"**Overall Score:** {quality_report['overall_score']:.2f} ({quality_report['quality_grade']})\n")
            f.write(f"**Compliance Status:** {quality_report['compliance_status']}\n\n")
            
            f.write(f"## Priority Recommendations\n\n")
            for rec in recommendations:
                f.write(f"### {rec['category']}\n")
                f.write(f"- **Priority:** {rec['priority']}\n")
                f.write(f"- **Issue:** {rec['issue']}\n")
                f.write(f"- **Recommendation:** {rec['recommendation']}\n")
                f.write(f"- **Impact:** {rec['impact']}\n\n")
        generated_files.append(str(recommendations_file))
        
        # Create validation summary
        summary_file = report_dir / "validation_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Quality Validation Summary\n\n")
            
            for agent_name, result in quality_report["validation_results"].items():
                if isinstance(result, dict):
                    f.write(f"## {agent_name.replace('_', ' ').title()} Agent\n")
                    f.write(f"**Score:** {result.get('score', 0):.2f}\n\n")
                    
                    if result.get('passed_checks'):
                        f.write(f"### ✅ Passed Checks ({len(result['passed_checks'])})\n")
                        for check in result['passed_checks']:
                            f.write(f"- {check}\n")
                        f.write("\n")
                    
                    if result.get('failed_checks'):
                        f.write(f"### ❌ Failed Checks ({len(result['failed_checks'])})\n")
                        for check in result['failed_checks']:
                            f.write(f"- {check}\n")
                        f.write("\n")
                    
                    if result.get('issues'):
                        f.write(f"### ⚠️ Issues Identified\n")
                        for issue in result['issues']:
                            f.write(f"- {issue}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")
        generated_files.append(str(summary_file))
        
        # Create action plan
        action_plan_file = report_dir / "action_plan.md"
        with open(action_plan_file, 'w', encoding='utf-8') as f:
            f.write(f"# Quality Improvement Action Plan\n\n")
            f.write(f"## Immediate Actions Required\n\n")
            
            for i, action in enumerate(quality_report["next_actions"], 1):
                f.write(f"{i}. {action}\n")
            
            f.write(f"\n## Detailed Recommendations\n\n")
            f.write(f"See `recommendations.md` for detailed improvement suggestions.\n\n")
            
            f.write(f"## Success Criteria\n\n")
            f.write(f"- Overall score > 0.8\n")
            f.write(f"- All high-priority issues resolved\n")
            f.write(f"- Cross-agent consistency > 0.9\n")
            f.write(f"- All business-critical elements present\n")
        generated_files.append(str(action_plan_file))
        
        return generated_files
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": self.agent_name,
            "status": "active" if self.is_initialized else "inactive",
            "validation_capabilities": ["content_validation", "seo_validation", "social_media_validation", "consistency_check"],
            "quality_standards": ["completeness", "accuracy", "relevance", "language_quality", "format_compliance"],
            "supported_business_types": ["restaurant", "retail", "service"]
        }
    
    async def shutdown(self):
        """Shutdown the agent."""
        self.is_initialized = False
        logger.info("Real Quality Control Agent shutdown")
