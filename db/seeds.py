from db.users import seed_users
from db.priorities import seed_priorities
from db.tasks import seed_tasks

def seed_all():
    print("🚀 Seeding database...")
    seed_users()
    seed_priorities()
    seed_tasks()
    print("✅ Database seeding complete!")

if __name__ == "__main__":
    seed_all()