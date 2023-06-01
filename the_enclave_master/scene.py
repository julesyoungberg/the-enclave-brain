class SceneObject:
    """
    A base class representing any object that features a `step` method, designed to be updated.
    """

    def __init__(self):
        pass

    def step(self, delta_time: float):
        """
        Method that should be overriden by subclasses to provide custom behavior for each time step.

        :param delta_time: The time elapsed since the last time step.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")


class SceneManager:
    """
    A class for managing all objects in the scene.
    It maintains a list of objects and calls their `step` method for each time step.
    """

    def __init__(self):
        self._objects = []

    def add_object(self, obj: SceneObject):
        """
        Adds an object to the scene manager's list of objects.

        :param obj: The object to be added.
        """
        self._objects.append(obj)

    def remove_object(self, obj: SceneObject):
        """
        Removes an object from the scene manager's list of objects.

        :param obj: The object to be removed.
        """
        self._objects.remove(obj)

    def step(self, delta_time: float):
        """
        Calls the `step` method of each object in the scene manager's list of objects.

        :param delta_time: The time elapsed since the last step.
        """
        for obj in self._objects:
            obj.step(delta_time)
