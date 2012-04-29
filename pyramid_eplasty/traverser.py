from eplasty.object.exc import NotFound
import weakref

class Traverser():
    """Traversers wrap around object classes and allow dictionary-like
    lookup"""
    
    def __init__(self, class_, field, session=None):
        self.class_ = class_
        self.field = getattr(class_, field)
        self.session = session

    def mount(self, parent, name):
        self.__parent__ = weakref.proxy(parent)
        self.__name__ = name
        parent[name] = self

    def __getitem__(self, key):
        try:
            result = self.class_.get(self.field == key, session=self.session)
        except NotFound:
            raise KeyError(key)
        result.__parent__ = self
        result.__name__ = key
        return result
