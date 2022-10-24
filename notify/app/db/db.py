from sqlmodel import create_engine, SQLModel, Session

from app.core.config import get_app_settings

config = get_app_settings()
engine = create_engine(config.DATABASE_URI, echo=config.DEBUG)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
