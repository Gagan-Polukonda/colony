from db import SessionLocal
from models import Forager
from config import settings

db = SessionLocal()
for key, username in settings.api_keys.items():
    db.add(Forager(username=username, api_key=key))
db.commit()
db.close()
