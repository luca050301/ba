def overrides(interface_class):
    """
    Decorator to indicate that a method overrides a method in the specified interface class.
    This decorator asserts that the method being decorated is indeed an override of a method defined in the interface class.
    """

    def overrider(method):
        assert method.__name__ in dir(interface_class)
        return method

    return overrider
