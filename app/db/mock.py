from app.schemas.user import UserInDB


fake_users_db: dict[str, UserInDB] = {
    "johndoe": UserInDB(
        username="johndoe",
        full_name="John Doe",
        email="johndoe@example.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$yAZZD04wEdS0C+F16WpcHA$p3sSkRXSUWLflQs9IIzQU4L5ce83XSj7ttW5w/+K0hg",
        disabled=False,
    ),
    "alice": UserInDB(
        username="alice",
        full_name="Alice Wonderson",
        email="alice@example.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$kL57ieJQtU5+qoSncAbYow$a6iSP4Cm6n4OCGntr66+NTGJctXsxTRW7JgvNX9mwU8",
        disabled=True,
    ),
}
