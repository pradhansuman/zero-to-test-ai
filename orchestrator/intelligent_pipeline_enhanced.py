#!/usr/bin/env python3
"""Enhanced Intelligent Pipeline with Application-Type Detection"""

from enum import Enum

class ApplicationType(Enum):
    ECOMMERCE = "ecommerce"
    SAAS_PLATFORM = "saas_platform"
    SOCIAL_NETWORK = "social_network"
    MOBILE_APP = "mobile_app"
    API = "api"
    FORMS_PLATFORM = "forms_platform"
    CONTENT_SITE = "content_site"


class ApplicationTypeDetector:
    """Detect application type from feature story"""

    KEYWORDS = {
        ApplicationType.ECOMMERCE: ["product", "catalog", "shop", "cart", "checkout", "payment", "order", "inventory"],
        ApplicationType.SAAS_PLATFORM: ["dashboard", "admin", "billing", "user", "settings", "report", "analytics"],
        ApplicationType.SOCIAL_NETWORK: ["post", "comment", "feed", "like", "share", "follow", "profile"],
        ApplicationType.MOBILE_APP: ["mobile", "app", "ios", "android", "touch", "gesture", "offline"],
        ApplicationType.API: ["api", "endpoint", "rest", "graphql", "json", "webhook"],
        ApplicationType.FORMS_PLATFORM: ["form", "input", "validation", "submit", "field"],
        ApplicationType.CONTENT_SITE: ["article", "blog", "news", "page", "content"],
    }

    @staticmethod
    def detect(title, description):
        text = f"{title} {description}".lower()
        scores = {at: sum(1 for kw in kws if kw in text) for at, kws in ApplicationTypeDetector.KEYWORDS.items()}
        return max(scores, key=scores.get)


APP_CONFIGS = {
    ApplicationType.ECOMMERCE: {
        "test_count": 18,
        "guardrails": ["REQ-5", "REQ-8", "REQ-9", "REQ-10", "REQ-11", "REQ-13"],
        "scenarios": ["Product Search", "Filtering", "Cart Mgmt", "Checkout", "Orders", "Payment", "Inventory"],
        "risks": ["Payment security", "Inventory accuracy", "Cart integrity", "Search perf", "Order reliability"],
        "complexity": "Very High"
    },
    ApplicationType.SAAS_PLATFORM: {
        "test_count": 22,
        "guardrails": ["REQ-5", "REQ-8", "REQ-9", "REQ-10", "REQ-11", "REQ-24"],
        "scenarios": ["Dashboard", "Users", "CRUD", "Reports", "Billing", "Collaboration"],
        "risks": ["Data security", "Isolation", "Scale", "Audit", "Backup"],
        "complexity": "Very High"
    },
    ApplicationType.SOCIAL_NETWORK: {
        "test_count": 20,
        "guardrails": ["REQ-5", "REQ-8", "REQ-9", "REQ-27", "REQ-28"],
        "scenarios": ["Profiles", "Posts", "Feeds", "Notifications", "Messaging"],
        "risks": ["Real-time sync", "Privacy", "Moderation", "Load"],
        "complexity": "Very High"
    },
    ApplicationType.MOBILE_APP: {
        "test_count": 15,
        "guardrails": ["REQ-5", "REQ-8", "REQ-9", "REQ-13", "REQ-15"],
        "scenarios": ["Startup", "Touch", "Offline", "Sync", "Permissions"],
        "risks": ["Memory", "Battery", "Network", "Crashes"],
        "complexity": "High"
    },
    ApplicationType.API: {
        "test_count": 12,
        "guardrails": ["REQ-5", "REQ-8", "REQ-9", "REQ-10"],
        "scenarios": ["Auth", "Methods", "Validation", "Errors"],
        "risks": ["Security", "Validation", "Rate limiting"],
        "complexity": "Medium"
    },
    ApplicationType.FORMS_PLATFORM: {
        "test_count": 8,
        "guardrails": ["REQ-5", "REQ-6", "REQ-7", "REQ-13"],
        "scenarios": ["Inputs", "Validation", "Submit", "Errors"],
        "risks": ["Validation", "Clarity", "Accessibility"],
        "complexity": "Low"
    },
    ApplicationType.CONTENT_SITE: {
        "test_count": 10,
        "guardrails": ["REQ-5", "REQ-9", "REQ-13"],
        "scenarios": ["Discovery", "Search", "Display"],
        "risks": ["Performance", "SEO", "Consistency"],
        "complexity": "Low-Medium"
    },
}


def demo():
    print("\n" + "="*80)
    print("🤖 ENHANCED INTELLIGENT PIPELINE - APPLICATION TYPE DETECTION")
    print("="*80 + "\n")

    print("📋 TEST CASE 1: DEMOQA (FORMS PLATFORM)")
    print("-" * 80)
    app1 = ApplicationTypeDetector.detect("DemoQA Testing Platform", "Practice testing with form inputs")
    cfg1 = APP_CONFIGS[app1]
    print(f"✅ Detected: {app1.value.upper()}")
    print(f"📊 Tests: {cfg1['test_count']} | Guardrails: {cfg1['guardrails']}")
    print(f"⚙️  Complexity: {cfg1['complexity']}\n")

    print("🛍️  TEST CASE 2: TRICENTIS DEMO WEB SHOP (ECOMMERCE)")
    print("-" * 80)
    app2 = ApplicationTypeDetector.detect("Tricentis Demo Web Shop", "Full ecommerce with cart and checkout")
    cfg2 = APP_CONFIGS[app2]
    print(f"✅ Detected: {app2.value.upper()}")
    print(f"📊 Tests: {cfg2['test_count']} | Guardrails: {cfg2['guardrails']}")
    print(f"⚙️  Complexity: {cfg2['complexity']}")
    print(f"📌 Scenarios: {', '.join(cfg2['scenarios'][:4])}...")
    print(f"⚠️  Risks: {', '.join(cfg2['risks'][:3])}...\n")

    print("="*80)
    print("📊 INTELLIGENT ADAPTATION")
    print("="*80)
    print(f"\n{'Application':<20} {'Type':<18} {'Tests':<8} {'Guardrails':<12} {'Complexity':<15}")
    print("-" * 80)
    print(f"{'DemoQA':<20} {app1.value:<18} {cfg1['test_count']:<8} {len(cfg1['guardrails']):<12} {cfg1['complexity']:<15}")
    print(f"{'Demo Web Shop':<20} {app2.value:<18} {cfg2['test_count']:<8} {len(cfg2['guardrails']):<12} {cfg2['complexity']:<15}")
    print(f"\n✨ Difference: {cfg2['test_count'] - cfg1['test_count']}% MORE TESTS for ecommerce (18 vs 8)")
    print(f"✨ 2 additional guardrails for ecommerce (6 vs 4)")
    print(f"✨ Custom scenarios and risk focus for each type\n")


if __name__ == "__main__":
    demo()
