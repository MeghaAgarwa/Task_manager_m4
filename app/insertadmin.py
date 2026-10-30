from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password_hash = pwd_context.hash("Admin@123")

print(password_hash)