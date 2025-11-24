from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

def add_funds(username, amount):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.balance += amount
            db.session.commit()
            print(f"Added ${amount} to {username}. New balance: ${user.balance}")
        else:
            print(f"User {username} not found.")

if __name__ == "__main__":
    add_funds('admin', 10000)
