class SceneObject:
    """
    A base class representing any object that features a `step` method, designed to be updated.
    """

    def __init__(self):
        pass

    def step(self, delta_time):
        """
        Method that should be overriden by subclasses to provide custom behavior for each time step.

        :param delta_time: The time elapsed since the last time step.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")
