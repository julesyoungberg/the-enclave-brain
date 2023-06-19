import numpy as np


class Parameter:
    """
    A class that represents a parameter with a given initial value and a lookback window.
    Allows for the addition of new values, updating of the current value, and retrieval of various statistics such as the previous value, the mean, and the standard deviation.

    Args:
        initial_value (float): The initial value of the parameter.
        lookback (int, optional): The size of the lookback window. Defaults to 1.

    Attributes:
        lookback (int): The size of the lookback window.
        _values (list): A list containing the parameter values.

    Methods:
        add_value(value: float) -> None: Adds a new value to the parameter list and updates the lookback window if necessary.
        update_value(value: float) -> None: Updates the current parameter value.
        get_current_value() -> float: Returns the current parameter value.
        get_prev_value() -> float or None: Returns the previous parameter value if it exists, otherwise None.
        get_mean() -> float: Returns the mean of the parameter values.
        get_std() -> float: Returns the standard deviation of the parameter values.
        get_velocity() -> float returns the mean rate of change of the parameter.
    """

    def __init__(self, initial_value: float, lookback=1):
        self.lookback = lookback
        self._values = [initial_value]

    def add_value(self, value=None):
        if value is None:
            self._values.insert(self._values[0])
        else:
            self._values.insert(value)
        if len(self._values) > self.lookback + 1:
            self._values = self._values[: self.lookback + 1]

    def update_value(self, value: float):
        self._values[0] = value

    def get_current_value(self):
        return self._values[0]

    def get_prev_value(self):
        if len(self._values) < 2:
            return None

        return self._values[1]

    def get_mean(self):
        return np.mean(self._values)

    def get_std(self):
        return np.std(self._values)

    def get_velocity(self):
        return np.mean(self._values[:-1] - self._values[1:])
