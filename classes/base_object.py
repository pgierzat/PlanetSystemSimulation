from pipr_24z_pgierzat.errors import NegativeMassError


class BaseObject:
    def __init__(self, pos_x, pos_y, mass):
        self._pos_x = pos_x
        self._pos_y = pos_y
        if mass <= 0:
            raise NegativeMassError
        self._mass = mass

    def pos_x(self):
        return self._pos_x

    def set_pos_x(self, value):
        self._pos_x = value

    def pos_y(self):
        return self._pos_y

    def set_pos_y(self, value):
        self._pos_y = value

    def mass(self):
        return self._mass
