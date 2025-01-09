from classes.base_object import BaseObject


class Object(BaseObject):
    def __init__(self, pos_x, pos_y, mass, velocity_x=0, velocity_y=0):
        super().__init__(pos_x, pos_y, mass)
        self._velocity_x = velocity_x
        self._velocity_y = velocity_y

    def velocity_x(self):
        return self._velocity_x

    def set_vel_x(self, value):
        self._velocity_x = value

    def velocity_y(self):
        return self._velocity_y

    def set_vel_y(self, value):
        self._velocity_y = value
