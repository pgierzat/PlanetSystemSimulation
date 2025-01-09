from classes.base_object import BaseObject
from pipr_24z_pgierzat.errors import NegativeRadiusError, NegativeMassError


class CentralObject(BaseObject):
    def __init__(self, mass, radius, pos_x=0, pos_y=0):
        super().__init__(pos_x, pos_y, mass)
        if radius <= 0:
            raise NegativeRadiusError
        self._radius = radius

    def radius(self):
        return self._radius

    def set_mass(self, mass):
        if mass <= 0:
            raise NegativeMassError
        self._mass = mass

    def set_radius(self, value):
        if value <= 0:
            raise NegativeRadiusError
        self._radius = value
