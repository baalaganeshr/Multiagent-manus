"""
Enterprise Production Configuration
Fortune 500-grade production settings for enterprise deployment
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class SecurityConfig:
    """Enterprise security configuration"""
    api_rate_limit: int = 100  # requests per minute per user
    max_concurrent_requests: int = 50
    request_timeout: int = 30  # seconds
    encryption_standard: str = "AES-256"
    ssl_required: bool = True
    api_key_rotation_days: int = 30
    session_timeout_minutes: int = 120

@dataclass
class PerformanceConfig:
    """Enterprise performance configuration"""
    agent_response_timeout: int = 10  # seconds
    max_retry_attempts: int = 3
    circuit_breaker_threshold: int = 5
    connection_pool_size: int = 20
    cache_ttl_seconds: int = 300
    batch_processing_size: int = 100

@dataclass
class MonitoringConfig:
    """Enterprise monitoring configuration"""
    performance_monitoring: bool = True
    error_tracking: bool = True
    usage_analytics: bool = True
    real_time_alerts: bool = True
    log_retention_days: int = 90
    metrics_collection_interval: int = 60  # seconds

@dataclass
class ComplianceConfig:
    """Enterprise compliance configuration"""
    gdpr_compliance: bool = True
    hipaa_compliance: bool = True
    sox_compliance: bool = True
    audit_logging: bool = True
    data_encryption_at_rest: bool = True
    data_encryption_in_transit: bool = True

class ProductionConfig:
    """Enterprise production configuration management"""
    
    def __init__(self, environment: str = "production"):
        self.environment = environment
        self.security = SecurityConfig()
        self.performance = PerformanceConfig()
        self.monitoring = MonitoringConfig()
        self.compliance = ComplianceConfig()
        
        # Environment-specific overrides
        if environment == "development":
            self._apply_development_overrides()
        elif environment == "staging":
            self._apply_staging_overrides()
        elif environment == "production":
            self._apply_production_overrides()
    
    def _apply_development_overrides(self):
        """Development environment configuration"""
        self.security.api_rate_limit = 1000
        self.security.request_timeout = 60
        self.performance.agent_response_timeout = 30
        self.monitoring.real_time_alerts = False
        self.compliance.audit_logging = False
    
    def _apply_staging_overrides(self):
        """Staging environment configuration"""
        self.security.api_rate_limit = 200
        self.monitoring.log_retention_days = 30
        self.performance.circuit_breaker_threshold = 3
    
    def _apply_production_overrides(self):
        """Production environment configuration (most restrictive)"""
        self.security.api_rate_limit = 100
        self.security.request_timeout = 30
        self.performance.agent_response_timeout = 10
        self.monitoring.real_time_alerts = True
        self.compliance.audit_logging = True
    
    @property
    def database_config(self) -> Dict[str, Any]:
        """Database configuration for enterprise deployment"""
        return {
            "connection_pool_size": 20,
            "connection_timeout": 30,
            "query_timeout": 15,
            "ssl_mode": "require",
            "backup_retention_days": 30,
            "encryption_at_rest": True,
            "auto_scaling": True,
            "read_replicas": 2 if self.environment == "production" else 0
        }
    
    @property
    def cache_config(self) -> Dict[str, Any]:
        """Cache configuration for performance optimization"""
        return {
            "redis_cluster": True if self.environment == "production" else False,
            "ttl_default": self.performance.cache_ttl_seconds,
            "max_memory": "2gb",
            "eviction_policy": "allkeys-lru",
            "persistence": True,
            "encryption": True
        }
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Comprehensive logging configuration"""
        return {
            "level": "INFO" if self.environment == "production" else "DEBUG",
            "format": "json",
            "include_request_id": True,
            "include_user_context": True,
            "include_performance_metrics": True,
            "retention_days": self.monitoring.log_retention_days,
            "structured_logging": True,
            "log_sampling": 0.1 if self.environment == "production" else 1.0
        }
    
    @property
    def api_config(self) -> Dict[str, Any]:
        """API configuration for enterprise standards"""
        return {
            "rate_limiting": {
                "requests_per_minute": self.security.api_rate_limit,
                "burst_capacity": self.security.api_rate_limit * 2,
                "rate_limit_headers": True
            },
            "cors": {
                "allowed_origins": self._get_allowed_origins(),
                "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allowed_headers": ["Content-Type", "Authorization", "X-Request-ID"],
                "expose_headers": ["X-Rate-Limit-Remaining", "X-Rate-Limit-Reset"]
            },
            "security_headers": {
                "strict_transport_security": True,
                "content_security_policy": True,
                "x_frame_options": "DENY",
                "x_content_type_options": "nosniff"
            }
        }
    
    def _get_allowed_origins(self) -> List[str]:
        """Get allowed origins based on environment"""
        if self.environment == "production":
            return [
                "https://platform.enterprise-ai.com",
                "https://app.enterprise-ai.com",
                "https://admin.enterprise-ai.com"
            ]
        elif self.environment == "staging":
            return [
                "https://staging.enterprise-ai.com",
                "https://staging-app.enterprise-ai.com"
            ]
        else:
            return [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000"
            ]
    
    @property
    def enterprise_features(self) -> Dict[str, Any]:
        """Enterprise feature configuration"""
        return {
            "white_labeling": True,
            "custom_branding": True,
            "api_access": "full",
            "webhook_support": True,
            "custom_integrations": True,
            "dedicated_support": True,
            "sla_guarantees": {
                "uptime": 99.9,
                "response_time": 2.0,
                "support_response": 4  # hours
            },
            "advanced_analytics": True,
            "custom_reporting": True,
            "data_export": True,
            "audit_trails": True
        }
    
    @property
    def scaling_config(self) -> Dict[str, Any]:
        """Auto-scaling configuration for enterprise loads"""
        return {
            "auto_scaling": True,
            "min_instances": 2 if self.environment == "production" else 1,
            "max_instances": 20 if self.environment == "production" else 5,
            "target_cpu_utilization": 70,
            "scale_up_cooldown": 300,  # seconds
            "scale_down_cooldown": 600,  # seconds
            "health_check_path": "/health",
            "health_check_interval": 30
        }
    
    @property
    def backup_config(self) -> Dict[str, Any]:
        """Backup and disaster recovery configuration"""
        return {
            "automated_backups": True,
            "backup_frequency": "hourly" if self.environment == "production" else "daily",
            "backup_retention": 30,  # days
            "cross_region_replication": True if self.environment == "production" else False,
            "point_in_time_recovery": True,
            "disaster_recovery_rto": 4,  # hours
            "disaster_recovery_rpo": 1   # hour
        }
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get complete configuration for the environment"""
        return {
            "environment": self.environment,
            "security": self.security.__dict__,
            "performance": self.performance.__dict__,
            "monitoring": self.monitoring.__dict__,
            "compliance": self.compliance.__dict__,
            "database": self.database_config,
            "cache": self.cache_config,
            "logging": self.logging_config,
            "api": self.api_config,
            "enterprise_features": self.enterprise_features,
            "scaling": self.scaling_config,
            "backup": self.backup_config
        }
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate configuration for production readiness"""
        issues = []
        warnings = []
        
        # Security validations
        if self.security.api_rate_limit > 1000:
            warnings.append("High API rate limit may impact security")
        
        if not self.security.ssl_required and self.environment == "production":
            issues.append("SSL is required for production environment")
        
        # Performance validations
        if self.performance.agent_response_timeout > 30:
            warnings.append("High agent timeout may impact user experience")
        
        # Compliance validations
        if not self.compliance.audit_logging and self.environment == "production":
            issues.append("Audit logging is required for production compliance")
        
        if not self.compliance.data_encryption_at_rest:
            issues.append("Data encryption at rest is required for enterprise compliance")
        
        # Monitoring validations
        if not self.monitoring.error_tracking:
            warnings.append("Error tracking should be enabled for production monitoring")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "production_ready": len(issues) == 0 and self.environment == "production"
        }

# Global configuration instance
def get_production_config(environment: str = None) -> ProductionConfig:
    """Get production configuration instance"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "production")
    
    return ProductionConfig(environment)

# Configuration constants for enterprise deployment
ENTERPRISE_CONSTANTS = {
    "PLATFORM_NAME": "Enterprise AI Business Automation Platform",
    "VERSION": "1.0.0",
    "API_VERSION": "v1",
    "SUPPORT_EMAIL": "enterprise-support@platform.com",
    "DOCUMENTATION_URL": "https://docs.enterprise-ai.com",
    "STATUS_PAGE_URL": "https://status.enterprise-ai.com",
    "TERMS_URL": "https://enterprise-ai.com/terms",
    "PRIVACY_URL": "https://enterprise-ai.com/privacy",
    "SLA_URL": "https://enterprise-ai.com/sla"
}
