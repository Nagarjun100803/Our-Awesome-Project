from itsdangerous import URLSafeTimedSerializer

from src.settings import settings

verify_email_serializer = URLSafeTimedSerializer(
    secret_key=settings.email_verification.secret_key.get_secret_value(),
    salt=settings.email_verification.salt.get_secret_value(),
)


reset_password_serializer = URLSafeTimedSerializer(
    secret_key=settings.reset_password.secret_key.get_secret_value(),
    salt=settings.reset_password.salt.get_secret_value(),
)


# if __name__ == "__main__":
#     print(verify_email_serializer.dumps({"email": "arulsampathcyr@gmail.com"}))

#     verify_email_serializer.loads(
#         verify_email_serializer.dumps({"email": "arulsampathcyr@gmail.com"}),
#         max_age=800,
#     )
