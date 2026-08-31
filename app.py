import os
from pathlib import Path
from dotenv import load_dotenv

# Učitaj .env iz ROOT foldera projekta (gdje je app.py)
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

print("🔧 ENV loaded from:", ENV_PATH)
print("🔧 MAIL_HOST from env:", os.getenv("MAIL_HOST"))
print("🔧 DATABASE_URL from env:", os.getenv("DATABASE_URL"))

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
