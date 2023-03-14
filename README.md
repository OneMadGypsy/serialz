# serialz
A tiny python package for serializing class data as `json`, `pkl` or in a `shelve` database


### info:
You can extend `JSONClass`, `PKLClass` or `DBClass` to save/load your class to/from `json`, `pkl` or `shelve` database (respectively). All classes have identical interfaces. If the serialization data does not exist when the class is instanced it will create it. If the serialization data does exist, and `autoload` is `True`, the class will be instanced with the serialized data regardless of the init data. `save` or `load` at any time by simply calling `.save()` or `.load()` ~ neither method accepts arguments.

The system works by serializing the class `__dict__` (save), and updating the class `__dict__` with deserialized data (load). Everything about this package is very simple and obvious.


### features:
* serialize classes as `json`, `pkl` or in a `shelve` database.
* optionally autoload saved state when class is instanced
* optionally overwrite saved state when class is instanced
* paths are internally managed based on subclass type and id


### example:

```python3
from dataclasses import dataclass, InitVar
from serialz import DBClass


@dataclass
class Entity(DBClass):
    name   :str
    x      :int
    y      :int
    width  :int
    height :int
    
    #serializer init vars
    #since InitVar is used, these vars will not be available for serialization
    autoload  :InitVar = True
    overwrite :InitVar = False
    
    def __post_init__(self, autoload:bool, overwrite:bool):
        #JSONClass and PKLClass are instanced in an identical manner
        DBClass.__init__(self, self.name, autoload, overwrite)
        
        
#nothing is any different than how you generally instance classes
#you simply also have save and (auto)load serialization features
ent = Entity('Rect_1', 0, 0, 100, 100)
```


