"""
UPI Payment Gateway Integration for Indian Market
Supports multiple UPI providers and payment methods popular in India.

Supported Payment Methods:
- UPI (Google Pay, PhonePe, Paytm, BHIM, etc.)
- Net Banking
- Credit/Debit Cards
- Digital Wallets
- EMI options

Payment Providers:
- Razorpay
- PayU
- CCAvenue
- Cashfree
- Paytm
- PhonePe
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import json
import hashlib
import hmac
import base64
from decimal import Decimal
import aiohttp

from config.env import settings

logger = logging.getLogger(__name__)

class UPIGateway:
    """
    Unified Payment Interface (UPI) gateway for Indian businesses.
    Handles payments, refunds, settlements, and compliance.
    """
    
    def __init__(self):
        self.provider = settings.UPI_PROVIDER  # razorpay, payu, cashfree, etc.
        self.is_initialized = False
        self.session = None
        
        # Provider configurations
        self.provider_configs = {
            "razorpay": {
                "base_url": "https://api.razorpay.com/v1",
                "key_id": settings.RAZORPAY_KEY_ID,
                "key_secret": settings.RAZORPAY_KEY_SECRET,
                "webhook_secret": settings.RAZORPAY_WEBHOOK_SECRET
            },
            "cashfree": {
                "base_url": "https://api.cashfree.com/pg",
                "app_id": settings.CASHFREE_APP_ID,
                "secret_key": settings.CASHFREE_SECRET_KEY
            },
            "paytm": {
                "base_url": "https://securegw.paytm.in",
                "merchant_id": settings.PAYTM_MERCHANT_ID,
                "merchant_key": settings.PAYTM_MERCHANT_KEY
            },
            "phonepe": {
                "base_url": "https://api.phonepe.com/apis/hermes",
                "merchant_id": settings.PHONEPE_MERCHANT_ID,
                "salt_key": settings.PHONEPE_SALT_KEY,
                "salt_index": settings.PHONEPE_SALT_INDEX
            }
        }
        
        # Indian business context
        self.currency = "INR"
        self.gst_rates = {
            "electronics": 18,
            "clothing": 12,
            "food": 5,
            "services": 18,
            "books": 0,
            "medicines": 12
        }
        
        self.supported_upi_apps = [
            "gpay", "phonepe", "paytm", "bhim", "amazonpay", 
            "mobikwik", "freecharge", "jiomoney", "sbi", "icici"
        ]
    
    async def initialize(self):
        """Initialize UPI payment gateway."""
        if self.is_initialized:
            logger.warning("UPI gateway already initialized")
            return
        
        logger.info(f"Initializing UPI gateway with provider: {self.provider}")
        
        try:
            # Create HTTP session
            self.session = aiohttp.ClientSession()
            
            # Verify provider credentials
            await self._verify_credentials()
            
            self.is_initialized = True
            logger.info("UPI gateway initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize UPI gateway: {e}")
            raise
    
    async def start_service(self):
        """Start UPI payment service."""
        if not self.is_initialized:
            await self.initialize()
        
        logger.info("Starting UPI payment service...")
        
        # Start payment status monitoring
        monitor_task = asyncio.create_task(self._monitor_payments())
        
        try:
            await monitor_task
        except Exception as e:
            logger.error(f"UPI service error: {e}")
            raise
    
    async def create_payment_order(
        self, 
        amount: Union[int, float, Decimal],
        customer_details: Dict[str, Any],
        order_details: Dict[str, Any],
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a payment order for UPI transaction.
        
        Args:
            amount: Payment amount in INR
            customer_details: Customer information (name, email, phone)
            order_details: Order information (id, description, items)
            options: Additional options (payment methods, callbacks)
        
        Returns:
            Payment order details with payment URL/QR code
        """
        if not self.is_initialized:
            raise RuntimeError("UPI gateway not initialized")
        
        try:
            # Convert amount to paisa (smallest currency unit)
            amount_paisa = int(Decimal(str(amount)) * 100)
            
            # Generate unique order ID
            order_id = self._generate_order_id(order_details.get("id", ""))
            
            if self.provider == "razorpay":
                return await self._create_razorpay_order(
                    amount_paisa, customer_details, order_details, order_id, options
                )
            elif self.provider == "cashfree":
                return await self._create_cashfree_order(
                    amount_paisa, customer_details, order_details, order_id, options
                )
            elif self.provider == "paytm":
                return await self._create_paytm_order(
                    amount_paisa, customer_details, order_details, order_id, options
                )
            elif self.provider == "phonepe":
                return await self._create_phonepe_order(
                    amount_paisa, customer_details, order_details, order_id, options
                )
            else:
                raise ValueError(f"Unsupported payment provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error creating payment order: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _create_razorpay_order(
        self, 
        amount: int, 
        customer: Dict[str, Any],
        order: Dict[str, Any],
        order_id: str,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create Razorpay payment order."""
        config = self.provider_configs["razorpay"]
        url = f"{config['base_url']}/orders"
        
        # Calculate GST if applicable
        gst_amount = 0
        if order.get("category"):
            gst_rate = self.gst_rates.get(order["category"], 18)
            gst_amount = int((amount * gst_rate) / (100 + gst_rate))
        
        payload = {
            "amount": amount,
            "currency": self.currency,
            "receipt": order_id,
            "notes": {
                "customer_id": customer.get("id", ""),
                "customer_name": customer.get("name", ""),
                "order_description": order.get("description", ""),
                "gst_amount": gst_amount
            }
        }
        
        # Add UPI specific options
        if options and options.get("upi_only", True):
            payload["method"] = {
                "upi": True,
                "netbanking": False,
                "card": False,
                "wallet": False
            }
        
        auth = aiohttp.BasicAuth(config["key_id"], config["key_secret"])
        
        try:
            async with self.session.post(url, json=payload, auth=auth) as response:
                result = await response.json()
                
                if response.status == 200:
                    # Generate UPI payment link
                    payment_link = await self._create_razorpay_payment_link(result, customer, options)
                    
                    return {
                        "status": "success",
                        "order_id": result["id"],
                        "amount": amount / 100,
                        "currency": self.currency,
                        "payment_link": payment_link,
                        "upi_qr_code": self._generate_upi_qr_data(result, customer),
                        "expires_at": datetime.now() + timedelta(minutes=15),
                        "provider": "razorpay"
                    }
                else:
                    logger.error(f"Razorpay order creation failed: {result}")
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            logger.error(f"Razorpay API error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _create_cashfree_order(
        self, 
        amount: int, 
        customer: Dict[str, Any],
        order: Dict[str, Any],
        order_id: str,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create Cashfree payment order."""
        config = self.provider_configs["cashfree"]
        url = f"{config['base_url']}/orders"
        
        payload = {
            "order_id": order_id,
            "order_amount": amount / 100,
            "order_currency": self.currency,
            "customer_details": {
                "customer_id": customer.get("id", ""),
                "customer_name": customer.get("name", ""),
                "customer_email": customer.get("email", ""),
                "customer_phone": customer.get("phone", "")
            },
            "order_meta": {
                "return_url": options.get("return_url", "") if options else "",
                "notify_url": options.get("notify_url", "") if options else ""
            }
        }
        
        headers = {
            "x-api-version": "2023-08-01",
            "x-client-id": config["app_id"],
            "x-client-secret": config["secret_key"],
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.post(url, json=payload, headers=headers) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "status": "success",
                        "order_id": result["order_id"],
                        "amount": amount / 100,
                        "currency": self.currency,
                        "payment_link": result.get("payment_link", ""),
                        "upi_qr_code": self._generate_cashfree_upi_qr(result),
                        "expires_at": datetime.now() + timedelta(minutes=15),
                        "provider": "cashfree"
                    }
                else:
                    return {
                        "status": "error",
                        "error": result
                    }
                    
        except Exception as e:
            logger.error(f"Cashfree API error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def verify_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify payment status and authenticity.
        
        Args:
            payment_data: Payment callback data from provider
        
        Returns:
            Verification result with payment status
        """
        try:
            if self.provider == "razorpay":
                return await self._verify_razorpay_payment(payment_data)
            elif self.provider == "cashfree":
                return await self._verify_cashfree_payment(payment_data)
            elif self.provider == "paytm":
                return await self._verify_paytm_payment(payment_data)
            elif self.provider == "phonepe":
                return await self._verify_phonepe_payment(payment_data)
            else:
                return {
                    "status": "error",
                    "error": f"Verification not supported for {self.provider}"
                }
                
        except Exception as e:
            logger.error(f"Payment verification error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _verify_razorpay_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Verify Razorpay payment using signature verification."""
        config = self.provider_configs["razorpay"]
        
        # Extract payment details
        razorpay_order_id = payment_data.get("razorpay_order_id")
        razorpay_payment_id = payment_data.get("razorpay_payment_id")
        razorpay_signature = payment_data.get("razorpay_signature")
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return {
                "status": "error",
                "error": "Missing required payment data"
            }
        
        # Verify signature
        expected_signature = hmac.new(
            config["key_secret"].encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if expected_signature != razorpay_signature:
            return {
                "status": "error",
                "error": "Invalid payment signature"
            }
        
        # Fetch payment details from Razorpay
        url = f"{config['base_url']}/payments/{razorpay_payment_id}"
        auth = aiohttp.BasicAuth(config["key_id"], config["key_secret"])
        
        try:
            async with self.session.get(url, auth=auth) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "status": "success",
                        "payment_verified": True,
                        "payment_id": razorpay_payment_id,
                        "order_id": razorpay_order_id,
                        "amount": result.get("amount", 0) / 100,
                        "currency": result.get("currency", "INR"),
                        "payment_status": result.get("status", ""),
                        "payment_method": result.get("method", ""),
                        "payment_details": result
                    }
                else:
                    return {
                        "status": "error",
                        "error": "Failed to fetch payment details"
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "error": f"Payment verification failed: {str(e)}"
            }
    
    async def create_refund(
        self, 
        payment_id: str,
        amount: Union[int, float, Decimal] = None,
        reason: str = "requested_by_customer"
    ) -> Dict[str, Any]:
        """
        Create a refund for a successful payment.
        
        Args:
            payment_id: Original payment ID
            amount: Refund amount (None for full refund)
            reason: Reason for refund
        
        Returns:
            Refund creation result
        """
        try:
            if self.provider == "razorpay":
                return await self._create_razorpay_refund(payment_id, amount, reason)
            elif self.provider == "cashfree":
                return await self._create_cashfree_refund(payment_id, amount, reason)
            else:
                return {
                    "status": "error",
                    "error": f"Refunds not supported for {self.provider}"
                }
                
        except Exception as e:
            logger.error(f"Refund creation error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _create_razorpay_refund(
        self, 
        payment_id: str,
        amount: Union[int, float, Decimal] = None,
        reason: str = "requested_by_customer"
    ) -> Dict[str, Any]:
        """Create Razorpay refund."""
        config = self.provider_configs["razorpay"]
        url = f"{config['base_url']}/payments/{payment_id}/refund"
        
        payload = {
            "notes": {
                "reason": reason,
                "refund_date": datetime.now().isoformat()
            }
        }
        
        if amount is not None:
            payload["amount"] = int(Decimal(str(amount)) * 100)
        
        auth = aiohttp.BasicAuth(config["key_id"], config["key_secret"])
        
        try:
            async with self.session.post(url, json=payload, auth=auth) as response:
                result = await response.json()
                
                if response.status == 200:
                    return {
                        "status": "success",
                        "refund_id": result["id"],
                        "payment_id": payment_id,
                        "amount": result.get("amount", 0) / 100,
                        "currency": result.get("currency", "INR"),
                        "refund_status": result.get("status", ""),
                        "created_at": result.get("created_at", "")
                    }
                else:
                    return {
                        "status": "error",
                        "error": result.get("error", {})
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_payment_status(self, order_id: str) -> Dict[str, Any]:
        """Get current payment status for an order."""
        try:
            if self.provider == "razorpay":
                return await self._get_razorpay_payment_status(order_id)
            elif self.provider == "cashfree":
                return await self._get_cashfree_payment_status(order_id)
            else:
                return {
                    "status": "error",
                    "error": f"Status check not supported for {self.provider}"
                }
                
        except Exception as e:
            logger.error(f"Payment status check error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def generate_upi_qr_code(
        self, 
        upi_id: str,
        amount: Union[int, float, Decimal],
        payee_name: str,
        transaction_note: str = ""
    ) -> Dict[str, Any]:
        """
        Generate UPI QR code for direct payments.
        
        Args:
            upi_id: Merchant UPI ID
            amount: Payment amount
            payee_name: Merchant name
            transaction_note: Transaction description
        
        Returns:
            UPI QR code data and payment string
        """
        try:
            # UPI payment string format
            upi_string = f"upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR"
            
            if transaction_note:
                upi_string += f"&tn={transaction_note}"
            
            # Add transaction reference
            transaction_ref = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            upi_string += f"&tr={transaction_ref}"
            
            return {
                "status": "success",
                "upi_string": upi_string,
                "qr_data": upi_string,
                "transaction_ref": transaction_ref,
                "expires_at": datetime.now() + timedelta(minutes=15)
            }
            
        except Exception as e:
            logger.error(f"UPI QR generation error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def calculate_gst(
        self, 
        amount: Union[int, float, Decimal],
        category: str,
        include_gst: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate GST for Indian business transactions.
        
        Args:
            amount: Base amount
            category: Product/service category
            include_gst: Whether amount includes GST or not
        
        Returns:
            GST calculation breakdown
        """
        try:
            gst_rate = self.gst_rates.get(category, 18)
            amount = Decimal(str(amount))
            
            if include_gst:
                # Amount includes GST, calculate base amount and GST
                base_amount = amount / (1 + Decimal(gst_rate) / 100)
                gst_amount = amount - base_amount
            else:
                # Amount excludes GST, add GST
                base_amount = amount
                gst_amount = amount * Decimal(gst_rate) / 100
                amount = base_amount + gst_amount
            
            # Split GST into CGST and SGST for domestic transactions
            cgst = gst_amount / 2
            sgst = gst_amount / 2
            
            return {
                "status": "success",
                "base_amount": float(base_amount.quantize(Decimal('0.01'))),
                "gst_rate": gst_rate,
                "gst_amount": float(gst_amount.quantize(Decimal('0.01'))),
                "cgst": float(cgst.quantize(Decimal('0.01'))),
                "sgst": float(sgst.quantize(Decimal('0.01'))),
                "total_amount": float(amount.quantize(Decimal('0.01'))),
                "currency": self.currency
            }
            
        except Exception as e:
            logger.error(f"GST calculation error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _generate_order_id(self, base_id: str = "") -> str:
        """Generate unique order ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if base_id:
            return f"{base_id}_{timestamp}"
        else:
            return f"ORDER_{timestamp}"
    
    def _generate_upi_qr_data(self, order_data: Dict[str, Any], customer: Dict[str, Any]) -> str:
        """Generate UPI QR code data."""
        merchant_upi = settings.MERCHANT_UPI_ID
        amount = order_data.get("amount", 0) / 100
        
        return f"upi://pay?pa={merchant_upi}&pn=Merchant&am={amount}&cu=INR&tr={order_data['id']}"
    
    def _generate_cashfree_upi_qr(self, order_data: Dict[str, Any]) -> str:
        """Generate Cashfree UPI QR data."""
        # This would be provided by Cashfree API response
        return order_data.get("upi_qr_data", "")
    
    async def _verify_credentials(self):
        """Verify payment provider credentials."""
        if self.provider == "razorpay":
            await self._verify_razorpay_credentials()
        elif self.provider == "cashfree":
            await self._verify_cashfree_credentials()
        # Add other providers as needed
    
    async def _verify_razorpay_credentials(self):
        """Verify Razorpay API credentials."""
        config = self.provider_configs["razorpay"]
        url = f"{config['base_url']}/orders?count=1"
        auth = aiohttp.BasicAuth(config["key_id"], config["key_secret"])
        
        async with self.session.get(url, auth=auth) as response:
            if response.status != 200:
                result = await response.json()
                raise Exception(f"Razorpay credential verification failed: {result}")
    
    async def _monitor_payments(self):
        """Monitor payment status and handle updates."""
        logger.info("Starting payment status monitoring...")
        
        while True:
            try:
                # This would monitor pending payments and update their status
                # Implementation depends on the specific provider's webhook/polling mechanism
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Payment monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def handle_webhook(self, payload: Dict[str, Any], signature: str = None) -> Dict[str, Any]:
        """
        Handle payment webhook notifications.
        
        Args:
            payload: Webhook payload from payment provider
            signature: Webhook signature for verification
        
        Returns:
            Webhook processing result
        """
        try:
            if self.provider == "razorpay":
                return await self._handle_razorpay_webhook(payload, signature)
            elif self.provider == "cashfree":
                return await self._handle_cashfree_webhook(payload, signature)
            else:
                return {
                    "status": "error",
                    "error": f"Webhooks not supported for {self.provider}"
                }
                
        except Exception as e:
            logger.error(f"Webhook handling error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _handle_razorpay_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """Handle Razorpay webhook notifications."""
        config = self.provider_configs["razorpay"]
        
        # Verify webhook signature
        expected_signature = hmac.new(
            config["webhook_secret"].encode(),
            json.dumps(payload, separators=(',', ':')).encode(),
            hashlib.sha256
        ).hexdigest()
        
        if signature != expected_signature:
            return {
                "status": "error",
                "error": "Invalid webhook signature"
            }
        
        # Process webhook event
        event = payload.get("event", "")
        payment_data = payload.get("payload", {}).get("payment", {})
        
        logger.info(f"Received Razorpay webhook: {event}")
        
        return {
            "status": "success",
            "event": event,
            "payment_id": payment_data.get("entity", {}).get("id", ""),
            "processed": True
        }
    
    async def get_settlement_report(
        self, 
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get settlement report for the specified date range."""
        try:
            if self.provider == "razorpay":
                return await self._get_razorpay_settlements(start_date, end_date)
            else:
                return {
                    "status": "error",
                    "error": f"Settlement reports not supported for {self.provider}"
                }
                
        except Exception as e:
            logger.error(f"Settlement report error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def shutdown(self):
        """Shutdown UPI gateway."""
        logger.info("Shutting down UPI gateway...")
        
        if self.session:
            await self.session.close()
        
        logger.info("UPI gateway shutdown complete")
