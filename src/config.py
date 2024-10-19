import os

from fastapi.security import OAuth2PasswordBearer

class Settings:
    # Authentication
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXP_MINUTES: int = 60 * 24 * 7
    JWT_KEY: str = os.getenv('JWT_KEY')
    OAUTH2_SCHEME: str = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    # Database
    MONGO_HOSTNAME: str = os.getenv('MONGO_HOSTNAME')
    MONGO_PORT: int = os.getenv('MONGO_PORT')
    MONGO_AUTH_SOURCE: str = os.getenv('MONGO_AUTH_SOURCE')
    MONGO_DATABASE: str = os.getenv('MONGO_DATABASE')
    MONGO_USERNAME: str = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD')

    # Testing
    TEST_EMAIL: str = "test@example.com"
    TEST_USERNAME: str = "test_user"
    TEST_PASSWORD: str = "unsafe_password"

settings = Settings()