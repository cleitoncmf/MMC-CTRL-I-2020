# Class used to verify if a class atribut is from the correct type
class SetterProperty:
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)