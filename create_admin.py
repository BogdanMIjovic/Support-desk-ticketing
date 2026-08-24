from sqlmodel import Session
from app.models import User, UserRole
from app.auth import get_hashed_password
from app.database import engine


def create_admin():
    with Session(engine) as session:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        email = input("(This field is optional) Enter your email: ") or None
        full_name = input("(This field is optional) Enter your full name: ") or None
        hashed_password = get_hashed_password(password)

        user_data_validation = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "role": UserRole.admin,
            "hashed_password": hashed_password

        }

        user = User.model_validate(user_data_validation)
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Admin '{user.username}' successfully created!")
        return user

if __name__ == "__main__":
    create_admin()