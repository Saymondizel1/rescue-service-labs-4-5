from dataclasses import dataclass

@dataclass
class CityDTO:
    id: int
    name: str

@dataclass
class AddressDTO:
    id: int
    city_id: int
    street: str
    building: str

@dataclass
class EquipmentDTO:
    id: int
    name: str