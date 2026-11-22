from flask import Flask, jsonify, request
from service import CityService, VehicleService, ProcedureService

app = Flask(__name__)
city_service = CityService()
vehicle_service = VehicleService()
proc_service = ProcedureService()

# --- CRUD ДЛЯ CITIES (Лабораторна №4) ---

@app.route('/api/cities', methods=['GET'])
def get_cities():
    return jsonify(city_service.get_all_cities()), 200

@app.route('/api/cities', methods=['POST'])
def add_city():
    data = request.json
    city_service.create_city(data['name'])
    return jsonify({"message": "Місто успішно додано"}), 201

@app.route('/api/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.json
    city_service.update_city(city_id, data['name'])
    return jsonify({"message": "Місто успішно оновлено"}), 200

@app.route('/api/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    city_service.delete_city(city_id)
    return jsonify({"message": "Місто успішно видалено"}), 200

# --- ЗВ'ЯЗКИ 1:M ТА M:M (Лабораторна №4) ---

@app.route('/api/cities/<int:city_id>/addresses', methods=['GET'])
def get_city_addresses(city_id):
    return jsonify(city_service.get_addresses_for_city(city_id)), 200

@app.route('/api/vehicles/<int:vehicle_id>/equipments', methods=['GET'])
def get_vehicle_equipments(vehicle_id):
    return jsonify(vehicle_service.get_vehicle_equipments(vehicle_id)), 200

# --- ВИКЛИК ЗБЕРЕЖЕНИХ ПРОЦЕДУР (Лабораторна №5) ---

@app.route('/api/procedures/insert-city', methods=['POST'])
def proc_insert_city():
    data = request.json
    proc_service.insert_city(data['name'])
    return jsonify({"message": "Місто додано через збережену процедуру"}), 201

@app.route('/api/procedures/link-vehicle-equipment', methods=['POST'])
def proc_link_vehicle_equipment():
    data = request.json
    proc_service.link_vehicle_equipment(data['vehicle_brand'], data['equipment_name'])
    return jsonify({"message": "Зв'язок M:M успішно створено через процедуру"}), 200

@app.route('/api/procedures/insert-10-cities', methods=['POST'])
def proc_insert_10_cities():
    proc_service.insert_10_cities()
    return jsonify({"message": "Пакет із 10 міст (Noname1..10) додано"}), 201

@app.route('/api/procedures/avg-rescuers', methods=['GET'])
def proc_avg_rescuers():
    res = proc_service.get_avg_rescuers()
    return jsonify(res), 200

@app.route('/api/procedures/split-cities', methods=['POST'])
def proc_split_cities():
    proc_service.split_cities()
    return jsonify({"message": "Дві таблиці зі штампом часу створено та заповнено курсором"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)