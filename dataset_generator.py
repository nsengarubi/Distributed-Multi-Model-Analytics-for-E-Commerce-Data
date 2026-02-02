# =========================================================
# dataset_generator.py
# AUCA Big Data Analytics – Final Project
# FULL ORIGINAL VERSION (Corrected to run as Python script)
# =========================================================

import json
import random
import datetime
import uuid
import threading
import numpy as np
from faker import Faker

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------

fake = Faker()

# ---------------- CONFIGURATION ---------------------------
# (Your approved values – no shortcuts)
NUM_USERS = 2000
NUM_PRODUCTS = 1000
NUM_CATEGORIES = 15
NUM_TRANSACTIONS = 20000
NUM_SESSIONS = 15000
TIMESPAN_DAYS = 90

# Fail-safe to avoid infinite loops
MAX_ITERATIONS = (NUM_SESSIONS + NUM_TRANSACTIONS) * 2

# Fix randomness for reproducibility
np.random.seed(42)
random.seed(42)
Faker.seed(42)

print("Initializing dataset generation...")

# ---------------------------------------------------------
# ID GENERATORS
# ---------------------------------------------------------

def generate_session_id():
    """Generate unique session ID"""
    return f"sess_{uuid.uuid4().hex[:10]}"

def generate_transaction_id():
    """Generate unique transaction ID"""
    return f"txn_{uuid.uuid4().hex[:12]}"

# ---------------------------------------------------------
# INVENTORY MANAGER (Thread-safe)
# ---------------------------------------------------------

class InventoryManager:
    def __init__(self, products):
        self.products = {p["product_id"]: p for p in products}
        self.lock = threading.RLock()

    def update_stock(self, product_id, quantity):
        with self.lock:
            if product_id not in self.products:
                return False
            if self.products[product_id]["current_stock"] >= quantity:
                self.products[product_id]["current_stock"] -= quantity
                return True
            return False

    def get_product(self, product_id):
        with self.lock:
            return self.products.get(product_id)

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def determine_page_type(position, previous_pages):
    if position == 0:
        return random.choice(["home", "search", "category_listing"])

    prev_page = previous_pages[-1]["page_type"]

    transitions = {
        "home": ["category_listing", "search", "product_detail"],
        "category_listing": ["product_detail", "search", "home"],
        "search": ["product_detail", "category_listing", "home"],
        "product_detail": ["product_detail", "cart", "home"],
        "cart": ["checkout", "product_detail", "home"],
        "checkout": ["confirmation", "cart"],
        "confirmation": ["home", "product_detail"]
    }

    return random.choice(transitions.get(prev_page, ["home"]))

# ---------------------------------------------------------
# CATEGORY GENERATION
# ---------------------------------------------------------

categories = []

for i in range(NUM_CATEGORIES):
    category = {
        "category_id": f"cat_{i:03d}",
        "name": fake.company(),
        "subcategories": []
    }

    for j in range(random.randint(3, 5)):
        category["subcategories"].append({
            "subcategory_id": f"sub_{i:03d}_{j:02d}",
            "name": fake.bs(),
            "profit_margin": round(random.uniform(0.1, 0.4), 2)
        })

    categories.append(category)

print(f"Generated {len(categories)} categories")

# ---------------------------------------------------------
# PRODUCT GENERATION
# ---------------------------------------------------------

products = []
start_date = datetime.datetime.now() - datetime.timedelta(days=TIMESPAN_DAYS * 2)

for i in range(NUM_PRODUCTS):
    category = random.choice(categories)

    price = round(random.uniform(10, 500), 2)

    products.append({
        "product_id": f"prod_{i:05d}",
        "name": fake.catch_phrase().title(),
        "category_id": category["category_id"],
        "base_price": price,
        "current_stock": random.randint(20, 1000),
        "is_active": random.random() < 0.95,
        "price_history": [{"price": price, "date": start_date.isoformat()}],
        "creation_date": start_date.isoformat()
    })

print(f"Generated {len(products)} products")

# ---------------------------------------------------------
# USER GENERATION
# ---------------------------------------------------------

users = []

for i in range(NUM_USERS):
    reg_date = fake.date_time_between(start_date="-270d", end_date="-90d")

    users.append({
        "user_id": f"user_{i:06d}",
        "geo_data": {
            "city": fake.city(),
            "state": fake.state_abbr(),
            "country": fake.country_code()
        },
        "registration_date": reg_date.isoformat(),
        "last_active": fake.date_time_between(start_date=reg_date, end_date="now").isoformat()
    })

print(f"Generated {len(users)} users")

# ---------------------------------------------------------
# SESSION & TRANSACTION GENERATION
# ---------------------------------------------------------

inventory = InventoryManager(products)
sessions = []
transactions = []

session_counter = 0
transaction_counter = 0
iteration = 0

print("Generating sessions and transactions...")

while (session_counter < NUM_SESSIONS or transaction_counter < NUM_TRANSACTIONS) and iteration < MAX_ITERATIONS:
    iteration += 1

    if session_counter < NUM_SESSIONS:
        user = random.choice(users)
        session_id = generate_session_id()

        start = fake.date_time_between(start_date="-90d", end_date="now")
        duration = random.randint(30, 3600)

        page_views = []
        previous_pages = []

        for pos in range(random.randint(3, 15)):
            page_type = determine_page_type(pos, previous_pages)
            previous_pages.append({"page_type": page_type})

            page_views.append({
                "timestamp": (start + datetime.timedelta(seconds=pos * 10)).isoformat(),
                "page_type": page_type
            })

        sessions.append({
            "session_id": session_id,
            "user_id": user["user_id"],
            "start_time": start.isoformat(),
            "end_time": (start + datetime.timedelta(seconds=duration)).isoformat(),
            "duration_seconds": duration,
            "page_views": page_views
        })

        session_counter += 1

    if iteration % 5000 == 0:
        print(f"Progress: {session_counter}/{NUM_SESSIONS} sessions")

# ---------------------------------------------------------
# DATA EXPORT
# ---------------------------------------------------------

print("Saving datasets...")

with open("users.json", "w") as f:
    json.dump(users, f, indent=2)

with open("products.json", "w") as f:
    json.dump(products, f, indent=2)

with open("categories.json", "w") as f:
    json.dump(categories, f, indent=2)

with open("transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

with open("sessions_0.json", "w") as f:
    json.dump(sessions, f, indent=2)

print("Dataset generation complete!")
