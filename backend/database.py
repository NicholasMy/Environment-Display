import time
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session

import login_secrets as secrets

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{secrets.MYSQL_USER}:{secrets.MYSQL_PASSWORD}@{secrets.MYSQL_HOST}/{secrets.MYSQL_DATABASE}"
)
connection = None

while not connection:
    try:
        connection = engine.connect()
    except Exception as e:
        print("Waiting for database to start...")
        time.sleep(2)

print("Connected to database")

session = scoped_session(sessionmaker(bind=engine))


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = "history"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    monitor = sqlalchemy.Column(sqlalchemy.String(45))
    temperature = sqlalchemy.Column(sqlalchemy.Float)
    humidity = sqlalchemy.Column(sqlalchemy.Float)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return f"<Record {self.id} {self.monitor} {self.temperature} {self.humidity} {self.timestamp}>"

    @staticmethod
    def create(monitor, temperature, humidity):
        record = Record(
            monitor=monitor,
            temperature=temperature,
            humidity=humidity,
            timestamp=datetime.now()
        )

        session.add(record)
        session.commit()


def initialize_database():
    Base.metadata.create_all(engine)
