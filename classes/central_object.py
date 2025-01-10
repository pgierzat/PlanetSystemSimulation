from classes.base_object import BaseObject
from pipr_24z_pgierzat.errors import NegativeRadiusError, NegativeMassError


class CentralObject(BaseObject):
    """
    Class representing a central object in the simulation.
    It inherits from BaseObject.
    Attributes:
        radius (float): radius of the object.
    """
    def __init__(self, mass, radius, pos_x=0, pos_y=0):
        """
        Initialize the object with given mass, radius and position = 0, 0.
        Raises:
            NegativeRadiusError: if radius is less or equal to 0.
        """
        super().__init__(pos_x, pos_y, mass)
        if radius <= 0:
            raise NegativeRadiusError
        self._radius = radius

    def radius(self):
        """
        Get radius of the object.
        """
        return self._radius

    def set_mass(self, mass):
        """
        Set mass of the object.
        Raises:
            NegativeMassError: if mass is less or equal to 0.
        """
        if mass <= 0:
            raise NegativeMassError
        self._mass = mass

    def set_radius(self, radius):
        """
        Set radius of the object.
        Raises:
            NegativeRadiusError: if radius is less or equal to 0.
        """
        if radius <= 0:
            raise NegativeRadiusError
        self._radius = radius
