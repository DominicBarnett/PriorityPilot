from db.connection import get_db
from db.sample_data import sample_priorities

def seed_priorities():
    db = get_db()
    db.priorities.drop()
    db.priorities.insert_many(sample_priorities)
    print("✅ Priorities seeded successfully!")

if __name__ == "__main__":
    seed_priorities()
