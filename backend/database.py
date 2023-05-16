import json
import random
import time
from datetime import datetime, timedelta
from operator import and_

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
        print(e)
        time.sleep(2)

print("Connected to database")

session_maker = sessionmaker(bind=engine)


def get_session():
    return scoped_session(session_maker)()


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

    def to_json(self):
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def create(monitor: str, temperature: float, humidity: float):
        record = Record(
            monitor=monitor,
            temperature=temperature,
            humidity=humidity,
            timestamp=datetime.now()
        )

        with get_session() as session:
            session.add(record)
            session.commit()

        return record

    @staticmethod
    def get_recent_for_monitor(monitor: str, hours: int = 1, max_records: int = 1000):
        earliest = datetime.now() - timedelta(hours=hours)
        with get_session() as session:
            results = session.query(Record).filter(
                and_(
                    Record.monitor == monitor,
                    Record.timestamp >= earliest
                )
            )

            count = results.count()

            if count <= max_records or max_records == 0:
                return results.all()

            # Too many records, return evenly spaced records
            step = count // max_records
            stepped_records = results.filter(Record.id % step == 0)

            return stepped_records.limit(max_records)

    @staticmethod
    def get_json_for_monitor(monitor: str, hours: int = 1, max_records: int = 1000):
        records = Record.get_recent_for_monitor(monitor, hours, 0)  # Get all records within the time range
        number_of_records = len(records)

        if max_records == 0:
            # Return every record
            return json.dumps([record.to_json() for record in records])

        # Fetch a random sample of number_of_records - 2 records
        indices_to_keep = set(
            random.sample(range(1, number_of_records - 1), max(min(number_of_records, max_records) - 2, 0)))
        # Force the first and last record to be included
        if number_of_records > 0:
            indices_to_keep.add(0)
            indices_to_keep.add(number_of_records - 1)
        return json.dumps([record.to_json() for i, record in enumerate(records) if i in indices_to_keep])


def initialize_database():
    Base.metadata.create_all(engine)
