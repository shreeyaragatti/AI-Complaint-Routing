import random
from datetime import datetime, timedelta
from app import db, ai

sample_complaints = [
    "Major water pipe leakage near the school since morning. Water is flooding the road.",
    "Power outage in our area for the last 6 hours. Multiple households affected.",
    "Large pothole on the main road near the bus stop. Dangerous for vehicles.",
    "Garbage not collected for 3 days. Stench is unbearable and causing health issues.",
    "Street light not working for a week. Dark area causes safety concerns.",
    "Sewage overflow near the market area. Dirty water flowing into shops.",
    "Theft reported near the residential complex. CCTV footage shows two suspects.",
    "Construction noise early morning near hospital zone. Disturbing patients.",
    "No clean drinking water supply for 2 days in the entire sector.",
    "Fallen tree blocking the road after heavy rains. Traffic is completely stopped.",
    "Electric transformer sparking and making noise. Very dangerous for nearby houses.",
    "Public bus conductor behaving rudely with passengers on route 42.",
    "Drainage system blocked causing waterlogging. Mosquito breeding.",
    "Hospital staff shortage. Patients waiting for hours without proper care.",
    "School building wall cracked and unsafe for children. Structural damage.",
    "Illegal dumping of industrial waste near the river. Pollution spreading.",
    "Tenant harassment by landlord. Threatening to evict without notice.",
    "Train delays for over 2 hours. No information provided to passengers.",
    "No ambulance service available during emergency. Had to wait 45 minutes.",
    "Water supply contaminated with dirt. Brown water coming from taps."
]

print("Seeding database with sample complaints...")
for i, text in enumerate(sample_complaints):
    try:
        result = ai.process_complaint(text)
        print(f"[{i+1}/{len(sample_complaints)}] ID: {result['complaint_id']} | {result['category']} | {result['severity']} | Score: {result['priority_score']}")
    except Exception as e:
        print(f"Error: {e}")

print("\nDatabase seeded successfully!")
