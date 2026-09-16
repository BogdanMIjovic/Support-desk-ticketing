from sqlmodel import create_engine, Session

engine = create_engine("postgresql://postgres:12345@localhost:5432/support_desk")

def get_session():
    with Session(engine) as session:
        yield session

