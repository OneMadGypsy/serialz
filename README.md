# serialz
A tiny python package for (de)serializing class data from/to `json`, `pkl` or an entry in a `shelve` database


### info:
You can extend `JSONClass`, `PKLClass` or `DBClass` to save/load your class to/from `json`, `pkl` or `shelve` database (respectively). All classes have identical interfaces. If the serialization data does not exist when the class is instanced, it will create it. If the serialization data does exist, and `autoload` is `True`, the class will be instanced with the deserialized data, regardless of the init data. You can `save()`, `load()` or `delete()` at any time.

The system works by serializing the class `__dict__` (save), and updating the class `__dict__` with deserialized data (load).


### features:
* serialize classes as `json`, `pkl` or in a `shelve` database (save)
* deserialize `json`, `pkl` or a database entry to class       (load)
* delete file or database entry 
* optionally autoload saved state when class is instanced
* optionally overwrite saved state when class is instanced
* data destinations are internally created/managed


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
#you simply also have save, (auto)load, and delete features

ent = Entity('Rect_1', 0, 0, 100, 100)
```


