from app import app, db, User

def create_user(username, password):
    with app.app_context():
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        print(f"User {username} created successfully.")

if __name__ == '__main__':
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_user(username, password)