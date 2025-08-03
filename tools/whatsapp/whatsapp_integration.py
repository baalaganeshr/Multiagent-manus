"""
WhatsApp Business API Integration for Indian Market
Handles customer communication, marketing campaigns, and business automation via WhatsApp.

Features:
- WhatsApp Business Cloud API integration
- Template message management
- Interactive messaging (buttons, lists)
- Media sharing (images, documents, videos)
- Bulk messaging for campaigns
- Hindi/English language support
- Indian business context awareness
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
import json
import aiohttp
from datetime import datetime, timedelta
import base64
import mimetypes

from config.env import settings

logger = logging.getLogger(__name__)

class WhatsAppManager:
    """
    WhatsApp Business API manager for Indian business communication.
    Handles messaging, templates, media, and business automation.
    """
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.business_account_id = settings.WHATSAPP_BUSINESS_ACCOUNT_ID
        self.webhook_verify_token = settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN
        
        self.session = None
        self.is_initialized = False
        self.message_queue = asyncio.Queue()
        self.templates = {}
        
        # Indian business context
        self.business_hours = {
            "start": "09:00",
            "end": "18:00",
            "timezone": "Asia/Kolkata"
        }
        
        self.supported_languages = ["hi", "en"]
        self.currency = "INR"
    
    async def initialize(self):
        """Initialize WhatsApp Business API connection."""
        if self.is_initialized:
            logger.warning("WhatsApp manager already initialized")
            return
        
        logger.info("Initializing WhatsApp Business API...")
        
        try:
            # Create HTTP session
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }
            )
            
            # Verify API connection
            await self._verify_connection()
            
            # Load message templates
            await self._load_templates()
            
            self.is_initialized = True
            logger.info("WhatsApp Business API initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WhatsApp API: {e}")
            raise
    
    async def start_service(self):
        """Start WhatsApp service for processing messages."""
        if not self.is_initialized:
            await self.initialize()
        
        logger.info("Starting WhatsApp Business service...")
        
        # Start message processor
        message_processor = asyncio.create_task(self._process_message_queue())
        
        try:
            await message_processor
        except Exception as e:
            logger.error(f"WhatsApp service error: {e}")
            raise
    
    async def send_text_message(
        self, 
        to: str, 
        message: str, 
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp number.
        
        Args:
            to: Phone number with country code (e.g., "917234567890")
            message: Text message content
            language: Message language ("hi" for Hindi, "en" for English)
        
        Returns:
            Response from WhatsApp API
        """
        if not self.is_initialized:
            raise RuntimeError("WhatsApp manager not initialized")
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    logger.info(f"Message sent successfully to {to}")
                    return {
                        "status": "success",
                        "message_id": result.get("messages", [{}])[0].get("id"),
                        "recipient": to
                    }
                else:
                    logger.error(f"Failed to send message: {result}")
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def send_template_message(
        self, 
        to: str, 
        template_name: str, 
        parameters: List[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Send a template message (for notifications and marketing).
        
        Args:
            to: Phone number with country code
            template_name: Name of the approved template
            parameters: List of parameters for template placeholders
            language: Template language
        
        Returns:
            Response from WhatsApp API
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        template_components = []
        if parameters:
            template_components.append({
                "type": "body",
                "parameters": [{"type": "text", "text": param} for param in parameters]
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language
                },
                "components": template_components
            }
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    logger.info(f"Template message sent to {to}")
                    return {
                        "status": "success",
                        "message_id": result.get("messages", [{}])[0].get("id"),
                        "template": template_name
                    }
                else:
                    logger.error(f"Failed to send template: {result}")
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            logger.error(f"Error sending template message: {e}")
            return {
                "status": "error", "error": str(e)}
    
    async def send_interactive_message(
        self, 
        to: str, 
        message_type: str,
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send interactive message (buttons, lists, etc.).
        
        Args:
            to: Phone number
            message_type: "button" or "list"
            content: Interactive content configuration
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        if message_type == "button":
            interactive_content = {
                "type": "button",
                "body": {"text": content.get("body", "")},
                "action": {
                    "buttons": content.get("buttons", [])
                }
            }
        elif message_type == "list":
            interactive_content = {
                "type": "list",
                "header": {"text": content.get("header", "")},
                "body": {"text": content.get("body", "")},
                "footer": {"text": content.get("footer", "")},
                "action": {
                    "button": content.get("button_text", "Options"),
                    "sections": content.get("sections", [])
                }
            }
        else:
            return {"status": "error", "error": "Invalid message type"}
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": interactive_content
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "status": "success",
                        "message_id": result.get("messages", [{}])[0].get("id")
                    }
                else:
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            logger.error(f"Error sending interactive message: {e}")
            return {"status": "error", "error": str(e)}
    
    async def send_media_message(
        self, 
        to: str, 
        media_type: str,
        media_data: Union[str, bytes],
        caption: str = None
    ) -> Dict[str, Any]:
        """
        Send media message (image, document, video, audio).
        
        Args:
            to: Phone number
            media_type: "image", "document", "video", "audio"
            media_data: URL or base64 encoded data
            caption: Optional caption for media
        """
        # First upload media if it's binary data
        if isinstance(media_data, bytes):
            media_id = await self._upload_media(media_data, media_type)
            if not media_id:
                return {"status": "error", "error": "Failed to upload media"}
        else:
            media_id = media_data  # Assume it's already a URL or media ID
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        media_content = {"id": media_id} if media_id.startswith("http") else {"link": media_id}
        
        if caption and media_type in ["image", "video", "document"]:
            media_content["caption"] = caption
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": media_type,
            media_type: media_content
        }
        
        try:
            async with self.session.post(url, json=payload) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "status": "success",
                        "message_id": result.get("messages", [{}])[0].get("id")
                    }
                else:
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            logger.error(f"Error sending media message: {e}")
            return {"status": "error", "error": str(e)}
    
    async def send_business_template(
        self, 
        to: str, 
        template_type: str,
        business_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send business-specific templates for Indian market.
        
        Args:
            to: Phone number
            template_type: "order_confirmation", "payment_reminder", "festival_greeting", etc.
            business_data: Business-specific data for template
        """
        templates = {
            "order_confirmation": {
                "name": "order_confirmation_hi",
                "parameters": [
                    business_data.get("customer_name", "ग्राहक"),
                    business_data.get("order_id", ""),
                    business_data.get("amount", ""),
                    business_data.get("delivery_date", "")
                ]
            },
            "payment_reminder": {
                "name": "payment_reminder_hi",
                "parameters": [
                    business_data.get("customer_name", "ग्राहक"),
                    business_data.get("amount", ""),
                    business_data.get("due_date", "")
                ]
            },
            "festival_greeting": {
                "name": "festival_greeting_hi",
                "parameters": [
                    business_data.get("customer_name", "ग्राहक"),
                    business_data.get("festival_name", "त्योहार"),
                    business_data.get("offer_details", "")
                ]
            },
            "appointment_reminder": {
                "name": "appointment_reminder_hi",
                "parameters": [
                    business_data.get("customer_name", "ग्राहक"),
                    business_data.get("appointment_date", ""),
                    business_data.get("appointment_time", ""),
                    business_data.get("service_type", "")
                ]
            }
        }
        
        template_config = templates.get(template_type)
        if not template_config:
            return {"status": "error", "error": "Unknown template type"}
        
        return await self.send_template_message(
            to=to,
            template_name=template_config["name"],
            parameters=template_config["parameters"],
            language="hi"
        )
    
    async def send_bulk_messages(
        self, 
        recipients: List[str], 
        message: str,
        template_name: str = None,
        delay_seconds: int = 1
    ) -> Dict[str, Any]:
        """
        Send bulk messages for marketing campaigns.
        
        Args:
            recipients: List of phone numbers
            message: Message content (for text) or template parameters
            template_name: Template name (if using templates)
            delay_seconds: Delay between messages to avoid rate limits
        """
        results = {"successful": [], "failed": []}
        
        for recipient in recipients:
            try:
                if template_name:
                    result = await self.send_template_message(
                        to=recipient,
                        template_name=template_name,
                        parameters=[message] if isinstance(message, str) else message
                    )
                else:
                    result = await self.send_text_message(recipient, message)
                
                if result.get("status") == "success":
                    results["successful"].append(recipient)
                else:
                    results["failed"].append({
                        "recipient": recipient,
                        "error": result.get("error", "Unknown error")
                    })
                
                # Delay to avoid rate limits
                await asyncio.sleep(delay_seconds)
                
            except Exception as e:
                results["failed"].append({
                    "recipient": recipient,
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "summary": {
                "total": len(recipients),
                "successful": len(results["successful"]),
                "failed": len(results["failed"])
            },
            "details": results
        }
    
    async def handle_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook from WhatsApp.
        Process incoming messages, delivery receipts, and status updates.
        """
        try:
            if "entry" not in payload:
                return {"status": "error", "message": "Invalid webhook payload"}
            
            for entry in payload["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change.get("field") == "messages":
                            await self._process_incoming_message(change.get("value", {}))
            
            return {"status": "success"}
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _process_incoming_message(self, message_data: Dict[str, Any]):
        """Process incoming WhatsApp messages."""
        if "messages" in message_data:
            for message in message_data["messages"]:
                sender = message.get("from")
                message_type = message.get("type")
                timestamp = message.get("timestamp")
                
                # Process different message types
                if message_type == "text":
                    text_content = message.get("text", {}).get("body", "")
                    await self._handle_text_message(sender, text_content, timestamp)
                
                elif message_type == "interactive":
                    interactive_data = message.get("interactive", {})
                    await self._handle_interactive_response(sender, interactive_data, timestamp)
                
                elif message_type in ["image", "document", "audio", "video"]:
                    media_data = message.get(message_type, {})
                    await self._handle_media_message(sender, message_type, media_data, timestamp)
    
    async def _handle_text_message(self, sender: str, text: str, timestamp: str):
        """Handle incoming text messages."""
        logger.info(f"Received text message from {sender}: {text}")
        
        # Auto-response logic for Indian business context
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["हैलो", "hello", "hi", "namaste"]):
            response = "नमस्ते! आपका स्वागत है। मैं आपकी कैसे सहायता कर सकता हूं?"
            await self.send_text_message(sender, response, "hi")
        
        elif any(word in text_lower for word in ["price", "कीमत", "rate", "cost"]):
            response = "कृपया हमारी कीमतों के लिए, आप हमारी वेबसाइट देख सकते हैं या हमसे सीधे संपर्क करें।"
            await self.send_text_message(sender, response, "hi")
        
        elif any(word in text_lower for word in ["order", "ऑर्डर", "buy", "खरीदना"]):
            # Send interactive button for order process
            content = {
                "body": "ऑर्डर के लिए धन्यवाद! कृपया अपना विकल्प चुनें:",
                "buttons": [
                    {"type": "reply", "reply": {"id": "new_order", "title": "नया ऑर्डर"}},
                    {"type": "reply", "reply": {"id": "track_order", "title": "ऑर्डर ट्रैक करें"}},
                    {"type": "reply", "reply": {"id": "support", "title": "सहायता"}}
                ]
            }
            await self.send_interactive_message(sender, "button", content)
    
    async def _handle_interactive_response(self, sender: str, interactive_data: Dict[str, Any], timestamp: str):
        """Handle responses from interactive messages."""
        response_type = interactive_data.get("type")
        
        if response_type == "button_reply":
            button_id = interactive_data.get("button_reply", {}).get("id")
            await self._process_button_response(sender, button_id)
        
        elif response_type == "list_reply":
            list_id = interactive_data.get("list_reply", {}).get("id")
            await self._process_list_response(sender, list_id)
    
    async def _process_button_response(self, sender: str, button_id: str):
        """Process button responses."""
        if button_id == "new_order":
            response = "नया ऑर्डर शुरू करने के लिए, कृपया हमारी वेबसाइट पर जाएं या हमारे प्रोडक्ट कैटलॉग देखें।"
        elif button_id == "track_order":
            response = "अपना ऑर्डर ट्रैक करने के लिए, कृपया अपना ऑर्डर नंबर भेजें।"
        elif button_id == "support":
            response = "सहायता के लिए, आप हमसे फोन पर संपर्क कर सकते हैं या अपना प्रश्न यहां लिख सकते हैं।"
        else:
            response = "धन्यवाद! हम जल्द ही आपसे संपर्क करेंगे।"
        
        await self.send_text_message(sender, response, "hi")
    
    async def _handle_media_message(self, sender: str, media_type: str, media_data: Dict[str, Any], timestamp: str):
        """Handle incoming media messages."""
        logger.info(f"Received {media_type} from {sender}")
        
        # Acknowledge media receipt
        response = f"आपका {media_type} प्राप्त हुआ। धन्यवाद!"
        await self.send_text_message(sender, response, "hi")
    
    async def _upload_media(self, media_data: bytes, media_type: str) -> Optional[str]:
        """Upload media to WhatsApp servers."""
        url = f"{self.base_url}/{self.phone_number_id}/media"
        
        # Determine MIME type
        mime_type = mimetypes.guess_type(f"file.{media_type}")[0] or f"{media_type}/*"
        
        files = {
            "file": ("media", media_data, mime_type),
            "type": (None, media_type),
            "messaging_product": (None, "whatsapp")
        }
        
        try:
            # Use different session without JSON headers for file upload
            async with aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.access_token}"}
            ) as upload_session:
                async with upload_session.post(url, data=files) as response:
                    result = await response.json()
                    
                    if response.status == 200:
                        return result.get("id")
                    else:
                        logger.error(f"Media upload failed: {result}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error uploading media: {e}")
            return None
    
    async def _verify_connection(self):
        """Verify WhatsApp API connection."""
        url = f"{self.base_url}/{self.phone_number_id}"
        
        async with self.session.get(url) as response:
            if response.status != 200:
                result = await response.json()
                raise Exception(f"WhatsApp API connection failed: {result}")
    
    async def _load_templates(self):
        """Load available message templates."""
        url = f"{self.base_url}/{self.business_account_id}/message_templates"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    for template in result.get("data", []):
                        self.templates[template.get("name")] = template
                    logger.info(f"Loaded {len(self.templates)} WhatsApp templates")
                else:
                    logger.warning("Could not load WhatsApp templates")
                    
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
    
    async def _process_message_queue(self):
        """Process queued messages asynchronously."""
        while True:
            try:
                # Wait for message in queue
                message_task = await self.message_queue.get()
                
                # Process message
                await self._execute_message_task(message_task)
                
                # Mark task as done
                self.message_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error processing message queue: {e}")
                await asyncio.sleep(1)
    
    async def _execute_message_task(self, task: Dict[str, Any]):
        """Execute a message task."""
        task_type = task.get("type")
        
        if task_type == "text":
            await self.send_text_message(
                task["to"], task["message"], task.get("language", "en")
            )
        elif task_type == "template":
            await self.send_template_message(
                task["to"], task["template"], task.get("parameters", [])
            )
        elif task_type == "interactive":
            await self.send_interactive_message(
                task["to"], task["message_type"], task["content"]
            )
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Get WhatsApp Business analytics."""
        # This would integrate with WhatsApp Business API analytics
        # For now, return placeholder data
        return {
            "messages_sent": 0,
            "messages_received": 0,
            "delivery_rate": 0.0,
            "response_rate": 0.0,
            "active_conversations": 0
        }
    
    async def shutdown(self):
        """Shutdown WhatsApp manager."""
        logger.info("Shutting down WhatsApp manager...")
        
        if self.session:
            await self.session.close()
        
        logger.info("WhatsApp manager shutdown complete")
