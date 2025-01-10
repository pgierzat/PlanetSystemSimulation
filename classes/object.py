from classes.base_object import BaseObject


class Object(BaseObject):
    """
    Class representing object in space.
    It inherits from BaseObject class.
    Attributes:
        velocity_x (float): velocity in x axis.
        velocity_y (float): velocity in y axis.
    """
    def __init__(self, pos_x, pos_y, mass, velocity_x=0, velocity_y=0):
        """
        Initialize the object with given mass, position and velocity,
        default velocity = 0, 0.
        """
        super().__init__(pos_x, pos_y, mass)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

    def velocity_x(self):
        """
        Return velocity in x axis.
        """
        return self._velocity_x

    def set_vel_x(self, velocity):
        """
        Set velocity in x axis.
        Value for velocity can be negative or positive.
        """
        self._velocity_x = velocity

    def velocity_y(self):
        """
        Return velocity in y axis.
        """
        return self._velocity_y

    def set_vel_y(self, velocity):
        """
        Set velocity in y axis.
        Value for velocity can be negative or positive.
        """
        self._velocity_y = velocity
