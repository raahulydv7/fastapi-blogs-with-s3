from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import pg_url
from db_schemas import Base
engine = create_engine(pg_url, echo=True)
local_session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def pg_session():
    return local_session()
