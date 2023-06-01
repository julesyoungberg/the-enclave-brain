class SceneManager:
    """
    A class for managing all objects in the scene.
    It maintains a list of objects and calls their `step` method for each time step.
    """

    def __init__(self):
        self._objects = []

    def add_object(self, obj):
        """
        Adds an object to the scene manager's list of objects.

        :param obj: The object to be added.
        """
        self._objects.append(obj)

    def remove_object(self, obj):
        """
        Removes an object from the scene manager's list of objects.

        :param obj: The object to be removed.
        """
        self._objects.remove(obj)

    def step(self, delta_time):
        """
        Calls the `step` method of each object in the scene manager's list of objects.

        :param delta_time: The time elapsed since the last step.
        """
        for obj in self._objects:
            obj.step(delta_time)
