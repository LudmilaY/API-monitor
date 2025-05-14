from connect_db import connect_db

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
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(m.date_time), SUM(m.active_power_watt)
        FROM metrics m
        JOIN inverter i ON m.inverter_id = i.id
        WHERE i.plant_id = %s AND m.date_time BETWEEN %s AND %s
        GROUP BY DATE(m.date_time)
        ORDER BY DATE(m.date_time)
    """, (plant_id, data_start, data_end))
    result = cur.fetchall()
    conn.close()
    return result

def inverter_generation_per_range(inverter_id, data_start, data_end):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(date_time), SUM(active_power_watt)
        FROM metrics
        WHERE inverter_id = %s AND date_time BETWEEN %s AND %s
        GROUP BY DATE(date_time)
        ORDER BY DATE(date_time)
    """, (inverter_id, data_start, data_end))
    result = cur.fetchall()
    conn.close()
    return result
