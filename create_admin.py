from src.app import create_app
from src.database import db, bcrypt
from src.models.user import User

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("❌ Admin user already exists!")
    else:
        # Create admin user
        password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=password_hash,
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")