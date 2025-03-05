from db.connection import get_db
from db.sample_data import sample_users

def seed_users():
    db = get_db()
    db.users.drop()
    db.users.insert_many(sample_users)
    print("✅ Users seeded successfully!")

if __name__ == "__main__":
    seed_users()