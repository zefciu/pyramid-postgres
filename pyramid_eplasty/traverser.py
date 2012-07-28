import abc
from eplasty.object.exc import NotFound
import weakref

class Traverser(metaclass=abc.ABCMeta):
    """Traversers wrap around object classes and allow dictionary-like
    lookup"""

    def __init__(self, **kwargs):
        for kwarg in ['class_', 'field', 'session']:
            if kwarg in kwargs:
                setattr(self, kwarg, kwargs[kwarg])
    
    def mount(self, parent, name):
        self.__parent__ = weakref.proxy(parent)
        self.__name__ = name
        parent[name] = self

    def __getitem__(self, key):
        try:
            result = self.class_.get(
                getattr(self.class_, self.field) == key, session=self.session
            )
        except NotFound:
            raise KeyError(key)
        result.__parent__ = self
        result.__name__ = key
        return result
