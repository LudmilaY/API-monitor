from connect_db import connect_db
from utils import TimeSeriesValue, calc_inverters_generation

def generate_series(inverter_id, data_start, data_end):
    conn = connect_db()
    with conn.cursor() as curr:
        curr.execute("""
            SELECT date_time, active_power_watt
            FROM metrics
            WHERE inverter_id = %s AND date_time BETWEEN %s AND %s
            ORDER BY date_time
        """, (inverter_id, data_start, data_end))
        rows = curr.fetchall()
    series = [TimeSeriesValue(value=power, date=dt) for dt, power in rows]
    return series

def max_power_per_day(inverter_id, data_start, data_end):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(date_time), MAX(active_power_watt)
        FROM metrics
        WHERE inverter_id = %s AND date_time BETWEEN %s AND %s
        GROUP BY DATE(date_time)
        ORDER BY DATE(date_time)
    """, (inverter_id, data_start, data_end))
    result = cur.fetchall()
    conn.close()
    return result

def medium_temperature_per_day(inverter_id, data_start, data_end):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(date_time), AVG(temperature_celsius)
        FROM metrics
        WHERE inverter_id = %s AND date_time BETWEEN %s AND %s
        GROUP BY DATE(date_time)
        ORDER BY DATE(date_time)
    """, (inverter_id, data_start, data_end))
    result = cur.fetchall()
    conn.close()
    return result

def plant_generation_per_range(plant_id, data_start, data_end):
    conn = connect_db()
    # cur = conn.cursor()
    # cur.execute("""
    #     SELECT DATE(m.date_time), SUM(m.active_power_watt)
    #     FROM metrics m
    #     JOIN inverter i ON m.inverter_id = i.id
    #     WHERE i.plant_id = %s AND m.date_time BETWEEN %s AND %s
    #     GROUP BY DATE(m.date_time)
    #     ORDER BY DATE(m.date_time)
    # """, (plant_id, data_start, data_end))
    # result = cur.fetchall()
    # conn.close()
    # return result
    # The above commented code didn't preserve the calculus of utils.py
    # Correct one below as follows
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM inverter WHERE plant_id = %s
        """, (plant_id,))
        inverter_ids = [row[0] for row in cur.fetchall()]

    series_all = []
    for inverter_id in inverter_ids:
        series_all.append(type("DummyInverter", (), {
            "power": generate_series(inverter_id, data_start, data_end)
        })())

    total = calc_inverters_generation(series_all)
    return [data_start, total]

def inverter_generation_per_range(inverter_id, data_start, data_end):
    # conn = connect_db()
    # cur = conn.cursor()
    # cur.execute("""
    #     SELECT DATE(date_time), SUM(active_power_watt)
    #     FROM metrics
    #     WHERE inverter_id = %s AND date_time BETWEEN %s AND %s
    #     GROUP BY DATE(date_time)
    #     ORDER BY DATE(date_time)
    # """, (inverter_id, data_start, data_end))
    # result = cur.fetchall()
    # conn.close()
    # return result
    # The above commented code didn't preserve the calculus of utils.py
    # Correct one below as follows
    series = generate_series(inverter_id, data_start, data_end)
    if not series:
        return []

    dummy = type("DummyInverter", (), {"power": series})()
    total = calc_inverters_generation([dummy])

    return [data_start, total]
