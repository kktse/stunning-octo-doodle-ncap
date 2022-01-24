from enum import Enum


class VehicleDrivetrainTypes:
    UNKNOWN = "UNKNOWN"
    AWD = "AWD"
    FWD = "FWD"
    RWD = "RWD"
    FOUR_WD = "4WD"

    KEYS = (UNKNOWN, AWD, FWD, RWD, FOUR_WD)
    CHOICES = ((key, key) for key in KEYS)


class VehicleBodyStyles:
    UNKNOWN = "UNKNOWN"
    CONVERTIBLE = "Convertible"
    HATCHBACK = "Hatchback"
    PICKUP = "Pickup"
    SEDAN = "Sedan"
    SUV = "SUV"
    VAN = "Van"
    WAGON = "Wagon"

    KEYS = (UNKNOWN, CONVERTIBLE, HATCHBACK, PICKUP, SEDAN, SUV, VAN, WAGON)
    CHOICES = ((key, key) for key in KEYS)


class VehicleListOrderBy(str, Enum):
    ID = "id"
