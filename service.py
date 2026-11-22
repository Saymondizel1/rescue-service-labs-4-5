from dao import CityDAO, VehicleDAO, ProcedureDAO
from dto import CityDTO, AddressDTO, EquipmentDTO


class CityService:
    def __init__(self):
        self.dao = CityDAO()

    def get_all_cities(self):
        data = self.dao.get_all()
        return [CityDTO(id=row['id'], name=row['name']).__dict__ for row in data]

    def create_city(self, name):
        self.dao.create(name)

    def update_city(self, city_id, name):
        self.dao.update(city_id, name)

    def delete_city(self, city_id):
        self.dao.delete(city_id)

    def get_addresses_for_city(self, city_id):
        data = self.dao.get_addresses_by_city(city_id)
        return [AddressDTO(id=r['id'], city_id=r['Cities_id'], street=r['street'], building=r['building']).__dict__ for r in data]


class VehicleService:
    def __init__(self):
        self.dao = VehicleDAO()

    def get_vehicle_equipments(self, vehicle_id):
        data = self.dao.get_equipments_by_vehicle(vehicle_id)
        return [EquipmentDTO(id=row['id'], name=row['name']).__dict__ for row in data]


class ProcedureService:
    def __init__(self):
        self.dao = ProcedureDAO()

    def insert_city(self, name):
        self.dao.call_insert_city(name)

    def link_vehicle_equipment(self, vehicle_brand, equipment_name):
        self.dao.call_link_vehicle_equipment(vehicle_brand, equipment_name)

    def insert_10_cities(self):
        self.dao.call_insert_10_cities()

    def get_avg_rescuers(self):
        return self.dao.call_get_avg_rescuers()

    def split_cities(self):
        self.dao.call_split_cities()