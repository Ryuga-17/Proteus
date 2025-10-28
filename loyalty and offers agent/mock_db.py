# FILENAME: mock_db.py

# Mock product catalog
PRODUCT_CATALOG = {
    "prod-a": {
        "name": "Classic T-Shirt",
        "price": 25.00,
        "category": "clothing"
    },
    "prod-b": {
        "name": "Wireless Headphones",
        "price": 89.99,
        "category": "electronics"
    },
    "prod-c": {
        "name": "Coffee Mug",
        "price": 12.50,
        "category": "home"
    },
    "prod-d": {
        "name": "Running Shoes",
        "price": 120.00,
        "category": "footwear"
    },
    "prod-e": {
        "name": "Laptop Stand",
        "price": 45.00,
        "category": "electronics"
    }
}

# Mock customer profiles
CUSTOMER_PROFILES = {
    "c123": {
        "name": "Alex Johnson",
        "loyalty_tier": "gold",
        "email": "alex.johnson@email.com",
        "total_spent": 1250.00
    },
    "c456": {
        "name": "Sarah Wilson",
        "loyalty_tier": "silver",
        "email": "sarah.wilson@email.com",
        "total_spent": 450.00
    },
    "c789": {
        "name": "Mike Chen",
        "loyalty_tier": "bronze",
        "email": "mike.chen@email.com",
        "total_spent": 150.00
    },
    "c999": {
        "name": "Emma Davis",
        "loyalty_tier": "platinum",
        "email": "emma.davis@email.com",
        "total_spent": 2500.00
    }
}

# Mock promotions database
PROMOTIONS_DB = {
    "LOYALTY_RULES": {
        "bronze": {
            "name": "Bronze Member Discount",
            "type": "percent_off",
            "value": 0.05  # 5% off
        },
        "silver": {
            "name": "Silver Member Discount",
            "type": "percent_off",
            "value": 0.10  # 10% off
        },
        "gold": {
            "name": "Gold Member Discount",
            "type": "percent_off",
            "value": 0.15  # 15% off
        },
        "platinum": {
            "name": "Platinum Member Discount",
            "type": "percent_off",
            "value": 0.20  # 20% off
        }
    },
    "COUPONS": {
        "SAVE20": {
            "name": "20% Off Coupon",
            "type": "percent_off",
            "value": 0.20,
            "min_spend": 50.00
        },
        "SAVE10": {
            "name": "10% Off Coupon",
            "type": "percent_off",
            "value": 0.10,
            "min_spend": 25.00
        },
        "FLAT5": {
            "name": "$5 Off Coupon",
            "type": "dollar_off",
            "value": 5.00,
            "min_spend": 30.00
        },
        "WELCOME15": {
            "name": "Welcome Discount",
            "type": "percent_off",
            "value": 0.15,
            "min_spend": 40.00
        }
    }
}
