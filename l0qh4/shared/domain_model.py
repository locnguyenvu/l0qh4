from abc import ABCMeta

class DomainModel(metaclass=ABCMeta):

    @classmethod
    def from_dict(cls, attrdict: dict):
        instance = cls(**attrdict)
        return instance
    

