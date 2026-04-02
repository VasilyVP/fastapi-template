from sqlmodel import Session, select

from app.models.item import UserItem
from app.models.user import User


def seed_demo_data(session: Session) -> None:
    existing_user = session.exec(select(User).limit(1)).first()
    if existing_user is not None:
        return

    users: list[User] = [
        User(
            username="johndoe",
            full_name="John Doe",
            email="johndoe@example.com",
            hashed_password="$argon2id$v=19$m=65536,t=3,p=4$yAZZD04wEdS0C+F16WpcHA$p3sSkRXSUWLflQs9IIzQU4L5ce83XSj7ttW5w/+K0hg",
            disabled=False,
            items=[
                UserItem(name="Wireless Mouse", price=29.99, owner_username="johndoe"),
                UserItem(name="Mechanical Keyboard", price=89.0, owner_username="johndoe"),
            ],
        ),
        User(
            username="alice",
            full_name="Alice Wonderson",
            email="alice@example.com",
            hashed_password="$argon2id$v=19$m=65536,t=3,p=4$kL57ieJQtU5+qoSncAbYow$a6iSP4Cm6n4OCGntr66+NTGJctXsxTRW7JgvNX9mwU8",
            disabled=True,
            items=[
                UserItem(name="USB-C Hub", price=49.5, owner_username="alice"),
                UserItem(name="Notebook Stand", price=39.99, owner_username="alice"),
            ],
        ),
    ]

    session.add_all(users)
    session.commit()
