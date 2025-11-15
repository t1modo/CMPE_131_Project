import os
from pathlib import Path

class Config:
    # Placeholder secret key — replace in real deployments
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    # SQLite file in project root
    BASE_DIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
