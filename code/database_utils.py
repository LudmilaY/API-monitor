import psycopg2
from psycopg2 import sql
from datetime import datetime
from connect_db import connect_db

# Plants are "Usinas" (in Portuguese)
def create_plant(name, location):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO plants (name, location) VALUES (%s, %s) RETURNING id;",
            (name, location)
        )
        plant_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return plant_id
    except Exception as e:
        print(f"Error creating plant: {e}")
        return None

# Inverters are "Inversores" (in Portuguese)
def create_inverter(model, plant_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inverter (model, plant_id) VALUES (%s, %s) RETURNING id;",
            (model, plant_id)
        )
        inverter_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return inverter_id
    except Exception as e:
        print(f"Error creating inverter: {e}")
        return None

# Metrics are "Métricas" (in Portuguese)
def add_metrics(inverter_id, active_power_watt, temperature_celsius):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO metrics (date_time, active_power_watt, temperature_celsius, inverter_id) "
            "VALUES (%s, %s, %s, %s) RETURNING id;",
            (datetime.now(), active_power_watt, temperature_celsius, inverter_id)
        )
        metric_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return metric_id
    except Exception as e:
        print(f"Error adding metrics: {e}")
        return None

def search_plants():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plants;")
        plants = cursor.fetchall()
        cursor.close()
        conn.close()
        return plants
    except Exception as e:
        print(f"Error searching plants: {e}")
        return []

def search_inverter(plant_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inverter WHERE plant_id = %s;", (plant_id,))
        inverters = cursor.fetchall()
        cursor.close()
        conn.close()
        return inverters
    except Exception as e:
        print(f"Error searching inverters: {e}")
        return []

def search_metrics(inverter_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM metrics WHERE inverter_id = %s;", (inverter_id,))
        metrics = cursor.fetchall()
        cursor.close()
        conn.close()
        return metrics
    except Exception as e:
        print(f"Error searching metrics: {e}")
        return []

def update_plant(plant_id, name, location):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE plants SET name = %s, location = %s WHERE id = %s;",
            (name, location, plant_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error updating plant: {e}")

def update_inverter(inverter_id, model):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inverter SET model = %s WHERE id = %s;",
            (model, inverter_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error updating inverter: {e}")

def delete_plant(plant_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM plants WHERE id = %s;", (plant_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting plant: {e}")

def delete_inverter(inverter_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inverter WHERE id = %s;", (inverter_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting inverter: {e}")

def delete_metrics(metric_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM metrics WHERE id = %s;", (metric_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting metrics: {e}")

# Testing
if __name__ == "__main__":
    plant_id = create_plant("Solar Plant X", "Location A")

    inverter_id = create_inverter("Model Y", plant_id)

    metric_id = add_metrics(inverter_id, 500.0, 30.0)

    plants = search_plants()
    print(plants)

    inverters = search_inverter(plant_id)
    print(inverters)

    metrics = search_metrics(inverter_id)
    print(metrics)

    update_plant(plant_id, "Solar Plant X Upgrated", "Location B")

    search_inverter(inverter_id)

    delete_metrics(metric_id)

    delete_inverter(inverter_id)

    delete_plant(plant_id)

# CRUD Schema to create tables
def create_tables():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plants (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inverter (
                id SERIAL PRIMARY KEY,
                model VARCHAR(255),
                plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id SERIAL PRIMARY KEY,
                date_time TIMESTAMP WITH TIME ZONE NOT NULL,
                active_power_watt FLOAT,
                temperature_celsius FLOAT,
                inverter_id INTEGER REFERENCES inverter(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_datetime ON metrics(date_time);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_inverter ON metrics(inverter_id);
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Successfully created tables.")
    except Exception as e:
        print(f"Error creating tables: {e}")
