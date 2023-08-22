from sqlalchemy import create_engine
from app.db.models.models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:[TU_PASSWORD_DE_SUPABASE(BD)]@db.[TU_URL_DE_SUPABASE)]:6543/postgres"  # Replace with your actual database URL

engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created!")
