import json
from datetime import datetime
from connect_db import connect_db

# Create a plant if it doesn't exist
def create_plant_if_not_exists(name, location):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM plants WHERE name = %s", (name,))
    result = cursor.fetchone()

    if result:
        plant_id = result[0]
    else:
        cursor.execute("INSERT INTO plants (name, location) VALUES (%s, %s) RETURNING id", (name, location))
        plant_id = cursor.fetchone()[0]
        conn.commit()

    cursor.close()
    conn.close()
    return plant_id

# Create an inverter if it doesn't exist
def create_inverter(plant_id, amount=10):
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(1, amount + 1):
        cursor.execute("SELECT id FROM inverter WHERE id = %s", (i,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO inverter (id, model, plant_id) VALUES (%s, %s, %s)", (i, f"Modelo-{i}", plant_id))
    conn.commit()
    cursor.close()
    conn.close()

def inverter_exists(inverter_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM inverter WHERE id = %s", (inverter_id,))
    exist = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exist

def add_metrics(inverter_id, active_power_watt, temperature_celsius, date_time):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO metrics (date_time, active_power_watt, temperature_celsius, inverter_id)
            VALUES (%s, %s, %s, %s)
        """, (date_time, active_power_watt, temperature_celsius, inverter_id))
        conn.commit()
        print(f"Inserted entry: inversor_id={inverter_id}, power = {active_power_watt}, temperature = {temperature_celsius}, date = {date_time}")
    except Exception as e:
        conn.rollback()
        print(f"Error adding metrics: {e}")
    finally:
        cursor.close()
        conn.close()

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def populate_metrics_with_data(data):
    for item in data:
        try:
            data_iso = item["datetime"]["$date"]
            data_convert = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))

            inverter_id = item["inverter_id"]
            power = item["active_power_watt"]
            temperature = item["temperature_celsius"]

            if inverter_exists(inverter_id):
                add_metrics(inverter_id, power, temperature, data_convert)
            else:
                print(f"Inverter ID {inverter_id} doesn't exist. Ignoring entry.")

        except Exception as e:
            print(f"Item processing error: {e}")

# Testing
if __name__ == "__main__":
    plant_name = "Usina Principal"
    location = "São Paulo"

    file_path = "metrics.json"

    plant_id = create_plant_if_not_exists(plant_name, location)

    create_inverter(plant_id, amount=10)

    json_data = load_json(file_path)

    populate_metrics_with_data(json_data)
