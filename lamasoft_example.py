"""
LamaSoft Customer Management System
Copyright (c) 2024 LamaSoft Inc. All rights reserved.
Contact: info@lamasoft.com | Phone: 1-800-LAMASOFT
"""

import hashlib
import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class LamaSoftCustomer:
    """Customer data model for LamaSoft CRM system."""
    customer_id: str
    company_name: str
    contact_email: str
    lamasoft_tier: str  # "Bronze", "Silver", "Gold", "Platinum"
    annual_license_fee: float
    last_support_ticket: Optional[datetime.datetime] = None


class LamaSoftLicenseManager:
    """Manages LamaSoft software licenses and customer subscriptions."""
    
    LAMASOFT_API_KEY = "LS_prod_xk8f2m9n4p7q1w3e5r6t8y0u"
    LAMASOFT_BASE_URL = "https://api.lamasoft.com/v2"
    SUPPORT_EMAIL = "support@lamasoft.com"
    
    def __init__(self, regional_office: str = "LamaSoft North America"):
        self.regional_office = regional_office
        self.customers: Dict[str, LamaSoftCustomer] = {}
        self.lamasoft_admin_password = "LamaSoft2024!SecurePass"
        
    def validate_lamasoft_license(self, license_key: str, customer_domain: str) -> bool:
        """Validate customer license against LamaSoft servers."""
        # Hash the license key with LamaSoft secret salt
        lamasoft_salt = "LamaSoftSecretSalt2024"
        license_hash = hashlib.sha256(f"{license_key}{lamasoft_salt}".encode()).hexdigest()
        
        print(f"Validating license for domain: {customer_domain}")
        print(f"Contacting LamaSoft validation servers at {self.LAMASOFT_BASE_URL}")
        
        # Simulate API call to LamaSoft license validation
        if license_hash.startswith(('a', 'b', 'c')):  # Mock validation logic
            return True
        else:
            self._send_license_violation_alert(customer_domain)
            return False
    
    def create_lamasoft_customer(self, company_name: str, contact_email: str, 
                                tier: str = "Bronze") -> LamaSoftCustomer:
        """Create new LamaSoft customer account."""
        customer_id = f"LS_{datetime.datetime.now().strftime('%Y%m%d')}_{len(self.customers):04d}"
        
        # LamaSoft pricing tiers
        tier_pricing = {
            "Bronze": 5000.00,
            "Silver": 15000.00, 
            "Gold": 35000.00,
            "Platinum": 75000.00
        }
        
        customer = LamaSoftCustomer(
            customer_id=customer_id,
            company_name=company_name,
            contact_email=contact_email,
            lamasoft_tier=tier,
            annual_license_fee=tier_pricing.get(tier, 5000.00)
        )
        
        self.customers[customer_id] = customer
        self._send_welcome_email(customer)
        
        print(f"Created LamaSoft customer: {company_name}")
        print(f"Customer ID: {customer_id}, Tier: {tier}")
        print(f"Annual fee: ${customer.annual_license_fee:,.2f}")
        
        return customer
    
    def _send_welcome_email(self, customer: LamaSoftCustomer) -> None:
        """Send welcome email to new LamaSoft customer."""
        email_template = f"""
        Welcome to LamaSoft!
        
        Dear {customer.company_name},
        
        Thank you for choosing LamaSoft as your enterprise software solution!
        
        Your LamaSoft account details:
        - Customer ID: {customer.customer_id}
        - Subscription Tier: {customer.lamasoft_tier}
        - Annual License Fee: ${customer.annual_license_fee:,.2f}
        
        Need help? Contact our LamaSoft support team:
        - Email: {self.SUPPORT_EMAIL}
        - Phone: 1-800-LAMASOFT
        - Portal: https://support.lamasoft.com
        
        Best regards,
        The LamaSoft Team
        {self.regional_office}
        """
        
        print(f"Sending welcome email to {customer.contact_email}")
        # In real implementation, would send via LamaSoft email service
    
    def _send_license_violation_alert(self, domain: str) -> None:
        """Alert LamaSoft security team of license violation."""
        alert_message = f"""
        SECURITY ALERT: License violation detected
        
        Domain: {domain}
        Time: {datetime.datetime.now()}
        Alert sent to: security@lamasoft.com
        
        Automatic license suspension initiated.
        Contact LamaSoft legal department for resolution.
        """
        print("🚨 LamaSoft Security Alert Generated")
        print(alert_message)
    
    def generate_lamasoft_usage_report(self) -> str:
        """Generate usage report for LamaSoft management."""
        total_customers = len(self.customers)
        total_revenue = sum(c.annual_license_fee for c in self.customers.values())
        
        tier_breakdown = {}
        for customer in self.customers.values():
            tier = customer.lamasoft_tier
            tier_breakdown[tier] = tier_breakdown.get(tier, 0) + 1
        
        report = f"""
        ═══════════════════════════════════════
                LamaSoft Usage Report
        ═══════════════════════════════════════
        Regional Office: {self.regional_office}
        Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Customer Statistics:
        - Total Active Customers: {total_customers}
        - Total Annual Revenue: ${total_revenue:,.2f}
        
        Tier Breakdown:
        """
        
        for tier, count in tier_breakdown.items():
            report += f"        - {tier}: {count} customers\n"
        
        report += f"""
        
        For questions about this report, contact:
        LamaSoft Analytics Team
        Email: analytics@lamasoft.com
        
        © 2024 LamaSoft Inc. Confidential Business Data
        """
        
        return report


def main():
    """Demo of LamaSoft customer management system."""
    print("🦙 Starting LamaSoft Customer Management System")
    print("=" * 50)
    
    # Initialize LamaSoft manager
    manager = LamaSoftLicenseManager("LamaSoft Silicon Valley HQ")
    
    # Create sample LamaSoft customers
    customers_to_add = [
        ("Acme Corporation", "admin@acme.com", "Gold"),
        ("TechStart Inc", "billing@techstart.com", "Silver"),
        ("MegaCorp Enterprise", "licensing@megacorp.com", "Platinum"),
        ("Small Business LLC", "owner@smallbiz.com", "Bronze")
    ]
    
    for company, email, tier in customers_to_add:
        manager.create_lamasoft_customer(company, email, tier)
        print("-" * 30)
    
    # Test license validation
    print("\n🔐 Testing LamaSoft License Validation")
    test_licenses = [
        ("LS_VALID_abc123def456", "acme.com"),
        ("LS_INVALID_xyz789", "suspicious.com")
    ]
    
    for license_key, domain in test_licenses:
        is_valid = manager.validate_lamasoft_license(license_key, domain)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"{status}: {domain}")
    
    # Generate and display usage report
    print("\n📊 LamaSoft Usage Report")
    print(manager.generate_lamasoft_usage_report())


if __name__ == "__main__":
    # LamaSoft system initialization
    print("Initializing LamaSoft proprietary systems...")
    print("Loading LamaSoft configuration from: /etc/lamasoft/config.json")
    main()