from database import get_db_connection


class CityDAO:
    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cities")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def create(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cities (name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()

    def update(self, city_id, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cities SET name = %s WHERE id = %s", (name, city_id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self, city_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cities WHERE id = %s", (city_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_addresses_by_city(self, city_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM addresses WHERE Cities_id = %s", (city_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result


class VehicleDAO:
    def get_equipments_by_vehicle(self, vehicle_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT e.id, e.name 
            FROM equipments e
            JOIN vehicles_has_equipments vhe ON e.id = vhe.equipments_id
            WHERE vhe.vehicles_id = %s
        """
        cursor.execute(query, (vehicle_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result


class ProcedureDAO:
    def call_insert_city(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_insert_city', [name])
        conn.commit()
        cursor.close()
        conn.close()

    def call_link_vehicle_equipment(self, vehicle_brand, equipment_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_link_vehicle_equipment', [vehicle_brand, equipment_name])
        conn.commit()
        cursor.close()
        conn.close()

    def call_insert_10_cities(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_insert_10_cities')
        conn.commit()
        cursor.close()
        conn.close()

    def call_get_avg_rescuers(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('sp_get_avg_rescuers')
        row = None
        for result in cursor.stored_results():
            row = result.fetchone()
        cursor.close()
        conn.close()
        return row

    def call_split_cities(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('sp_split_cities_randomly')
        conn.commit()
        cursor.close()
        conn.close()