from passlib.hash import argon2  # type: ignore[reportAttributeAccessIssue]


class PasswordHasher:
    "Helper class to perfrom the password hashing and verifying."

    def hash_password(self, raw_password: str) -> str:
        return argon2.hash(raw_password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return argon2.verify(raw_password, hashed_password)


if __name__ == "__main__":
    password_hasher = PasswordHasher()
    hashed_password = password_hasher.hash_password("123")
    print(hashed_password)

    verified = password_hasher.verify_password("1223", hashed_password)
    print(verified)
