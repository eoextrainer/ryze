from app import app, Club

EMAIL = "contact@parisbball.fr"
PASSWORD = "password123"

with app.app_context():
    club = Club.query.filter_by(email=EMAIL).first()
    if club:
        print(f"Club found: {club.email}")
        if club.check_password(PASSWORD):
            print("Login successful: password is correct.")
        else:
            print("Login failed: password is incorrect.")
    else:
        print("Club not found.")
