import json
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

            # TODO try to get the perfect number of records
            # stepped_count = results.count()
            # missing_records = max_records - stepped_count
            # if missing_records > 0:
            #     additional_records = results.filter(Record not in stepped_records.all())
            #     return stepped_records.all() + additional_records.all()

            return stepped_records.limit(max_records)

    @staticmethod
    def get_json_for_monitor(monitor: str, hours: int = 1, max_records: int = 1000):
        records = Record.get_recent_for_monitor(monitor, hours, max_records)
        return json.dumps([record.to_json() for record in records])


def initialize_database():
    Base.metadata.create_all(engine)
