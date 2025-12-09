import os
from pathlib import Path


class Config:
    # Placeholder secret key — replace in real deployments
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # Project base directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # SQLite file in project root
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Where uploaded PDFs will be stored (used by "Upload & Scan" use case)
    UPLOAD_FOLDER = BASE_DIR / "uploads"