from app import create_app, db
from app.models.assessment import Assessment
from app.models.vendor import Vendor

app = create_app()

def clear_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Recreate all tables
        db.create_all()
        print("Database has been cleared and tables have been recreated.")

if __name__ == '__main__':
    clear_database() 