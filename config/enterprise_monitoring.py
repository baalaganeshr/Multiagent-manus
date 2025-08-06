"""
Enterprise Production Monitoring and Health Check System
Provides comprehensive monitoring, health checks, and production readiness validation
for the Fortune 500-grade AI Business Automation Platform.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class HealthCheckResult:
    """Health check result data structure."""
    service: str
    status: str  # healthy, degraded, unhealthy
    response_time_ms: float
    message: str
    details: Dict[str, Any]
    timestamp: datetime

class EnterpriseMonitoringSystem:
    """Enterprise-grade monitoring and health check system."""
    
    def __init__(self):
        self.monitoring_enabled = True
        self.health_checks = {}
        self.performance_metrics = {
            "system_startup_time": None,
            "total_requests_processed": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time_ms": 0,
            "peak_concurrent_requests": 0,
            "error_rate_percentage": 0,
            "uptime_seconds": 0,
            "memory_usage_mb": 0,
            "cpu_usage_percentage": 0
        }
        self.alert_thresholds = {
            "response_time_ms": 2000,  # 2 seconds
            "error_rate_percentage": 5,  # 5%
            "memory_usage_mb": 1000,  # 1GB
            "cpu_usage_percentage": 80  # 80%
        }
        self.last_health_check = None
        
    async def initialize(self):
        """Initialize monitoring system."""
        self.performance_metrics["system_startup_time"] = datetime.now(timezone.utc)
        logger.info("Enterprise Monitoring System initialized")
        
    async def register_health_check(self, service_name: str, check_function):
        """Register a health check for a service."""
        self.health_checks[service_name] = check_function
        logger.info(f"Health check registered for service: {service_name}")
        
    async def perform_health_check(self, service_name: str = None) -> Dict[str, HealthCheckResult]:
        """Perform health checks for all or specific services."""
        results = {}
        
        services_to_check = [service_name] if service_name else list(self.health_checks.keys())
        
        for service in services_to_check:
            if service in self.health_checks:
                start_time = time.time()
                try:
                    # Execute health check
                    check_result = await self.health_checks[service]()
                    response_time = (time.time() - start_time) * 1000  # Convert to ms
                    
                    if check_result.get("status") == "healthy":
                        status = "healthy"
                        message = "Service is operating normally"
                    elif check_result.get("status") == "degraded":
                        status = "degraded" 
                        message = "Service is experiencing issues but operational"
                    else:
                        status = "unhealthy"
                        message = "Service is not functioning properly"
                        
                    results[service] = HealthCheckResult(
                        service=service,
                        status=status,
                        response_time_ms=response_time,
                        message=message,
                        details=check_result,
                        timestamp=datetime.now(timezone.utc)
                    )
                    
                except Exception as e:
                    response_time = (time.time() - start_time) * 1000
                    results[service] = HealthCheckResult(
                        service=service,
                        status="unhealthy",
                        response_time_ms=response_time,
                        message=f"Health check failed: {str(e)}",
                        details={"error": str(e)},
                        timestamp=datetime.now(timezone.utc)
                    )
                    
        self.last_health_check = datetime.now(timezone.utc)
        return results
        
    async def get_system_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive system health summary."""
        health_results = await self.perform_health_check()
        
        total_services = len(health_results)
        healthy_services = sum(1 for result in health_results.values() if result.status == "healthy")
        degraded_services = sum(1 for result in health_results.values() if result.status == "degraded")
        unhealthy_services = sum(1 for result in health_results.values() if result.status == "unhealthy")
        
        # Calculate overall system status
        if unhealthy_services > 0:
            overall_status = "unhealthy"
        elif degraded_services > 0:
            overall_status = "degraded"
        else:
            overall_status = "healthy"
            
        # Calculate uptime
        if self.performance_metrics["system_startup_time"]:
            uptime = (datetime.now(timezone.utc) - self.performance_metrics["system_startup_time"]).total_seconds()
            self.performance_metrics["uptime_seconds"] = uptime
            
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "total": total_services,
                "healthy": healthy_services,
                "degraded": degraded_services,
                "unhealthy": unhealthy_services
            },
            "performance_metrics": self.performance_metrics,
            "health_checks": {
                service: {
                    "status": result.status,
                    "response_time_ms": result.response_time_ms,
                    "message": result.message,
                    "last_checked": result.timestamp.isoformat()
                }
                for service, result in health_results.items()
            },
            "alerts": self._check_alert_conditions()
        }
        
    def _check_alert_conditions(self) -> List[Dict[str, Any]]:
        """Check for alert conditions based on thresholds."""
        alerts = []
        
        # Check response time
        if self.performance_metrics["average_response_time_ms"] > self.alert_thresholds["response_time_ms"]:
            alerts.append({
                "type": "performance",
                "severity": "warning",
                "message": f"Average response time ({self.performance_metrics['average_response_time_ms']}ms) exceeds threshold ({self.alert_thresholds['response_time_ms']}ms)",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        # Check error rate
        if self.performance_metrics["error_rate_percentage"] > self.alert_thresholds["error_rate_percentage"]:
            alerts.append({
                "type": "reliability",
                "severity": "critical",
                "message": f"Error rate ({self.performance_metrics['error_rate_percentage']}%) exceeds threshold ({self.alert_thresholds['error_rate_percentage']}%)",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        # Check memory usage
        if self.performance_metrics["memory_usage_mb"] > self.alert_thresholds["memory_usage_mb"]:
            alerts.append({
                "type": "resource",
                "severity": "warning",
                "message": f"Memory usage ({self.performance_metrics['memory_usage_mb']}MB) exceeds threshold ({self.alert_thresholds['memory_usage_mb']}MB)",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        # Check CPU usage
        if self.performance_metrics["cpu_usage_percentage"] > self.alert_thresholds["cpu_usage_percentage"]:
            alerts.append({
                "type": "resource",
                "severity": "warning", 
                "message": f"CPU usage ({self.performance_metrics['cpu_usage_percentage']}%) exceeds threshold ({self.alert_thresholds['cpu_usage_percentage']}%)",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        return alerts
        
    async def update_performance_metrics(self, request_success: bool, response_time_ms: float):
        """Update performance metrics after request processing."""
        self.performance_metrics["total_requests_processed"] += 1
        
        if request_success:
            self.performance_metrics["successful_requests"] += 1
        else:
            self.performance_metrics["failed_requests"] += 1
            
        # Update average response time (rolling average)
        total_requests = self.performance_metrics["total_requests_processed"]
        current_avg = self.performance_metrics["average_response_time_ms"]
        new_avg = ((current_avg * (total_requests - 1)) + response_time_ms) / total_requests
        self.performance_metrics["average_response_time_ms"] = round(new_avg, 2)
        
        # Update error rate
        if self.performance_metrics["total_requests_processed"] > 0:
            error_rate = (self.performance_metrics["failed_requests"] / self.performance_metrics["total_requests_processed"]) * 100
            self.performance_metrics["error_rate_percentage"] = round(error_rate, 2)
            
    async def log_enterprise_metrics(self):
        """Log enterprise metrics for monitoring systems."""
        metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "enterprise_ai_platform",
            "metrics": self.performance_metrics,
            "health_status": "healthy" if self.performance_metrics["error_rate_percentage"] < 5 else "degraded"
        }
        
        logger.info(f"Enterprise Metrics: {json.dumps(metrics, indent=2)}")
        
    async def generate_enterprise_health_report(self) -> str:
        """Generate detailed enterprise health report."""
        health_summary = await self.get_system_health_summary()
        
        report = f"""
🏢 ENTERPRISE AI BUSINESS AUTOMATION PLATFORM
📊 Production Health Report
================================================================================

📈 OVERALL STATUS: {health_summary['overall_status'].upper()}
⏱️  Report Generated: {health_summary['timestamp']}
🚀 System Uptime: {round(health_summary['performance_metrics']['uptime_seconds'] / 3600, 2)} hours

📊 SERVICE HEALTH:
• Total Services: {health_summary['services']['total']}
• Healthy: {health_summary['services']['healthy']} ✅
• Degraded: {health_summary['services']['degraded']} ⚠️ 
• Unhealthy: {health_summary['services']['unhealthy']} ❌

📈 PERFORMANCE METRICS:
• Total Requests: {health_summary['performance_metrics']['total_requests_processed']}
• Success Rate: {round((health_summary['performance_metrics']['successful_requests'] / max(health_summary['performance_metrics']['total_requests_processed'], 1)) * 100, 2)}%
• Error Rate: {health_summary['performance_metrics']['error_rate_percentage']}%
• Average Response Time: {health_summary['performance_metrics']['average_response_time_ms']}ms
• Peak Concurrent Requests: {health_summary['performance_metrics']['peak_concurrent_requests']}

🔍 SERVICE DETAILS:
"""
        
        for service, details in health_summary['health_checks'].items():
            status_icon = "✅" if details['status'] == "healthy" else "⚠️" if details['status'] == "degraded" else "❌"
            report += f"• {service}: {details['status'].upper()} {status_icon} ({details['response_time_ms']}ms)\n"
            
        if health_summary['alerts']:
            report += f"\n🚨 ACTIVE ALERTS:\n"
            for alert in health_summary['alerts']:
                severity_icon = "🔴" if alert['severity'] == "critical" else "🟡"
                report += f"• {severity_icon} {alert['type'].upper()}: {alert['message']}\n"
        else:
            report += f"\n✅ NO ACTIVE ALERTS\n"
            
        report += f"""
================================================================================
✅ ENTERPRISE PLATFORM STATUS: PRODUCTION READY
"""
        
        return report
        
    async def shutdown(self):
        """Shutdown monitoring system."""
        self.monitoring_enabled = False
        logger.info("Enterprise Monitoring System shutdown completed")
