import ijson
from datetime import datetime
from dataclasses import dataclass
from typing import Protocol
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/apiusinas")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255))

class Inverter(Base):
    __tablename__ = 'inverter'
    id = Column(Integer, primary_key=True)
    model = Column(String(255))
    plant_id = Column(Integer, ForeignKey('plants.id', ondelete='CASCADE'))

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime(timezone=True), nullable=False)
    active_power_watt = Column(Float)
    temperature_celsius = Column(Float)
    inverter_id = Column(Integer, ForeignKey('inverter.id', ondelete='CASCADE'))

@dataclass
class TimeSeriesValue:
    value: float
    date: datetime

class EntityWithPower(Protocol):
    power: list[TimeSeriesValue]

def calc_inverters_generation(entities_with_power: list[EntityWithPower]) -> float:
    if not entities_with_power:
        return 0.0

    total_generation = 0.0

    for entity in entities_with_power:
        if len(entity.power) < 2:
            continue

        for i in range(len(entity.power) - 1):
            try:
                cur_power = entity.power[i].value
                next_power = entity.power[i + 1].value

                if cur_power < 0 or next_power < 0:
                    continue

                delta_time = (
                    entity.power[i + 1].date - entity.power[i].date
                ).total_seconds() / 3600

                if delta_time <= 0 or delta_time > 24:
                    continue

                generation = (cur_power + next_power) / 2 * delta_time
                total_generation += generation

            except (AttributeError, TypeError):
                continue

    return total_generation

def parse_metrics(raw: dict) -> dict | None:
    try:
        return {
            "date_time": datetime.fromisoformat(raw["datetime"]["$date"].replace("Z", "+00:00")),
            "inverter_id": raw["inverter_id"],
            "active_power_watt": raw["active_power_watt"],
            "temperature_celsius": raw["temperature_celsius"]
        }
    except Exception as e:
        print(f"Processing error of metric: {e}")
        return None

def load_metrics_streaming(path: str, batch_size: int = 1000):
    with open(path, "rb") as f:
        metrics = []
        parser = ijson.items(f, "item")

        for raw in parser:
            metric_dict = parse_metrics(raw)
            if metric_dict:
                metrics.append(Metric(**metric_dict))

            if len(metrics) >= batch_size:
                session.bulk_save_objects(metrics)
                session.commit()
                print(f"Batch insertions of {batch_size}")
                metrics = []

        if metrics:
            session.bulk_save_objects(metrics)
            session.commit()
            print(f"Final batch insertion of {len(metrics)}")

def calc_total_generation():
    inverters_ids = session.query(Metric.inverter_id).distinct().all()
    entities = []

    for (inv_id,) in inverters_ids:
        metrics = session.query(Metric).filter(Metric.inverter_id == inv_id).order_by(Metric.date_time).all()
        power_series = [TimeSeriesValue(m.active_power_watt, m.date_time) for m in metrics if m.active_power_watt is not None]
        entities.append(type("InversorEntity", (), {"power": power_series})())

    total = calc_inverters_generation(entities)
    print(f"Total estimated of generation (kWh): {total:.2f}")

# === EXECUÇÃO ===
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    load_metrics_streaming("metrics.json")
    calc_total_generation()
