from app.db.session import engine
from app.db.base import Base

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db_and_tables()
