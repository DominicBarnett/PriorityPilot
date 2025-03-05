from db.connection import get_db
from db.sample_data import sample_tasks

def seed_tasks():
    db = get_db()
    db.tasks.drop()
    db.tasks.insert_many(sample_tasks)
    print("✅ Tasks seeded successfully!")

if __name__ == "__main__":
    seed_tasks()