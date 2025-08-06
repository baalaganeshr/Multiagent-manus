"""
Enterprise Logging Configuration for Windows Console Compatibility
Fixes Unicode encoding errors for Fortune 500-grade production deployment
"""

import logging
import sys
import os
from typing import Optional


class EnterpriseLoggingConfig:
    """
    Production-grade logging configuration for Windows console compatibility.
    Eliminates Unicode encoding errors by using text equivalents for emoji characters.
    """
    
    @staticmethod
    def setup_production_logging(
        log_level: int = logging.INFO,
        log_file: Optional[str] = "enterprise_platform.log",
        console_output: bool = True
    ) -> None:
        """
        Configure UTF-8 compatible logging for Windows production environment.
        
        Args:
            log_level: Logging level (default: INFO)
            log_file: Log file path (default: enterprise_platform.log)
            console_output: Enable console output (default: True)
        """
        
        # Create formatter for production logging
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create handlers list
        handlers = []
        
        # Console handler with UTF-8 encoding
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(log_level)
            
            # Ensure UTF-8 encoding for Windows console
            if hasattr(console_handler.stream, 'reconfigure'):
                try:
                    console_handler.stream.reconfigure(encoding='utf-8')
                except (AttributeError, OSError):
                    # Fallback for older Python versions or restricted environments
                    pass
            
            handlers.append(console_handler)
        
        # File handler with UTF-8 encoding
        if log_file:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else '.'
            os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)
            handlers.append(file_handler)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            handlers=handlers,
            force=True  # Override any existing configuration
        )
        
        # Set specific logger levels for enterprise components
        enterprise_loggers = [
            'agents.core_agents.orchestrator',
            'agents.website_agents',
            'agents.marketing_agents',
            'agents.analytics_agents',
            'config.enterprise_monitoring'
        ]
        
        for logger_name in enterprise_loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)
    
    @staticmethod
    def sanitize_log_message(message: str) -> str:
        """
        Replace emoji characters with Windows console-compatible text equivalents.
        
        Args:
            message: Original log message with potential emoji characters
            
        Returns:
            Sanitized message with text equivalents
        """
        
        # Emoji to text replacements for production logging
        emoji_replacements = {
            '🎯': 'TARGET:',
            '💰': 'PRICING:',
            '🎨': 'CULTURAL:',
            '📊': 'METRICS:',
            '✅': 'SUCCESS:',
            '🔌': 'SHUTDOWN:',
            '🛑': 'STOPPING:',
            '⚠️': 'WARNING:',
            '❌': 'ERROR:',
            '🚀': 'LAUNCH:',
            '🏢': 'ENTERPRISE:',
            '🔧': 'CONFIG:',
            '📈': 'ANALYTICS:',
            '🌍': 'GLOBAL:',
            '⭐': 'FEATURE:',
            '🔥': 'CRITICAL:',
            '💡': 'INSIGHT:',
            '🎉': 'COMPLETE:',
            '🏆': 'ACHIEVEMENT:',
            '📝': 'NOTE:',
            '🔍': 'SEARCH:',
            '📱': 'MOBILE:',
            '💻': 'DESKTOP:',
            '🌐': 'WEB:',
            '📧': 'EMAIL:',
            '📞': 'CALL:',
            '💬': 'CHAT:',
            '📄': 'DOCUMENT:',
            '📊': 'REPORT:',
            '💯': 'PERFECT:',
            '🎪': 'EVENT:',
            '🏪': 'BUSINESS:',
            '🎭': 'SOCIAL:'
        }
        
        # Replace emoji characters with text equivalents
        sanitized_message = message
        for emoji, replacement in emoji_replacements.items():
            sanitized_message = sanitized_message.replace(emoji, replacement)
        
        return sanitized_message


class ProductionLogger:
    """
    Production-grade logger wrapper that automatically sanitizes emoji characters.
    Provides enterprise logging with Windows console compatibility.
    """
    
    def __init__(self, name: str):
        """
        Initialize production logger with emoji sanitization.
        
        Args:
            name: Logger name (typically __name__)
        """
        self._logger = logging.getLogger(name)
        self._config = EnterpriseLoggingConfig()
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Log info message with emoji sanitization."""
        sanitized_message = self._config.sanitize_log_message(message)
        self._logger.info(sanitized_message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Log error message with emoji sanitization."""
        sanitized_message = self._config.sanitize_log_message(message)
        self._logger.error(sanitized_message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning message with emoji sanitization."""
        sanitized_message = self._config.sanitize_log_message(message)
        self._logger.warning(sanitized_message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Log debug message with emoji sanitization."""
        sanitized_message = self._config.sanitize_log_message(message)
        self._logger.debug(sanitized_message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Log critical message with emoji sanitization."""
        sanitized_message = self._config.sanitize_log_message(message)
        self._logger.critical(sanitized_message, *args, **kwargs)


# Production logging setup function
def setup_enterprise_logging() -> None:
    """
    Initialize enterprise logging configuration for production deployment.
    Automatically sets up Windows console-compatible logging.
    """
    EnterpriseLoggingConfig.setup_production_logging(
        log_level=logging.INFO,
        log_file="logs/enterprise_platform.log",
        console_output=True
    )


# Convenience function to get production logger
def get_production_logger(name: str) -> ProductionLogger:
    """
    Get production logger instance with automatic emoji sanitization.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        ProductionLogger instance
    """
    return ProductionLogger(name)
