from pipr_24z_pgierzat.errors import NegativeMassError


class BaseObject:
    """
    Base class for all objects in the simulation.
    Represent a generic object with mass and position.
    Attributes:
        pos_x (float): x coordinate of the object.
        pos_y (float): y coordinate of the object.
        mass (float): mass of the object
    """
    def __init__(self, pos_x, pos_y, mass):
        """
        Initialize the object with given position and mass.

        Raises:
            NegativeMassError: if mass is less or equal to 0.
        """
        self._pos_x = pos_x
        self._pos_y = pos_y
        if mass <= 0:
            raise NegativeMassError
        self._mass = mass

    def pos_x(self):
        """
        Get x coordinate of the object.
        """
        return self._pos_x

    def set_pos_x(self, value):
        """
        Set x coordinate of the object.
        Its value isnt checked. It can be negative or positive.
        """
        self._pos_x = value

    def pos_y(self):
        """
        Get y coordinate of the object.
        """
        return self._pos_y

    def set_pos_y(self, value):
        """
        Set y coordinate of the object.
        Its value isnt checked. It can be negative or positive.
        """
        self._pos_y = value

    def mass(self):
        """
        Get mass of the object.
        """
        return self._mass
