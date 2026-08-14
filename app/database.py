from sqlmodel import create_engine, Session

engine = create_engine("sqlite:///./support_desk.db")

def get_session():
    with Session(engine) as session:
        yield session

