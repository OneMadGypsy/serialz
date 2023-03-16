# serialz
A tiny python package for (de)serializing class data from/to `json`, `pkl` or an entry in a `shelve` database


### features:
* **save**: serialize class as `json`, `pkl` or a `shelve` database entry
* **load**: deserialize `json`, `pkl` or a database entry to class
* **delete**: file (`json`, `pkl`) or database entry 
* optionally autoload saved state when class is instanced
* optionally overwrite saved state when class is instanced
* data destinations are internally created/managed
* unpicklicking is restricted to `(type, bool, int, float, str, bytes, bytearray, list, tuple, dict, set)`



## info:

The system works by (de)serializing data to/from the class `__dict__`.

You can extend `JSONClass`, `PKLClass` or `DBClass` to save/load your class to/from `json`, `pkl` or `shelve` database (respectively). If the serialized data does not exist when the class is instanced, it will create it. If the serialized data does exist, and `autoload` is `True`, the class will be instanced with the deserialized data, overwriting init values. You can `save()`, `load()` or `delete()` at any time. Due to destination data being managed internally, these methods do not accept arguments.

____

All 3 serialization classes have the same interface
| argument  | description                                    | default |
| --------- |:---------------------------------------------- |:------- |
| id        | becomes file name or database entry name       | not set |
| autoload  | True/False autoload when instanced             | True    |
| overwrite | True/False overwrite saved data when instanced | False   |

____

In `serialz.py`, `ROOT` is the name of the subfolder, within the CWD, that will be used to store serialized data. The default is: `ROOT = "data"`. Subfolders are created within `ROOT` directory, named after the `type` of the serializers subclass. Below are possible destinations, based on a serializer subclass named `Entity` with an `id` of `"default"`.

| class         | destination                                            |
|:------------- |:------------------------------------------------------ |
| **JSONClass** | `f'{os.getcwd()}/data/Entity/default.json'`            |
| **PKLClass**  | `f'{os.getcwd()}/data/Entity/default.pkl'`             |
| **DBClass**   | (`f'{os.getcwd()}/data/Entity/Entity_db'`)["default"]  |

____

In `serialz.py`, `ALLOWED` is used by the unpickler as a filter of allowed types to unpickle. It is currently set as:<br /> 

```python3
ALLOWED = (type, bool, int, float, str, bytes, bytearray, list, tuple, dict, set)
```

## example:

```python3
from dataclasses import dataclass, InitVar

#you could use any one of these as the `super` below
#and the only thing that would change is the serialization format
#usage across these classes is identical
from serialz import DBClass, JSONClass, PKLClass


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
        DBClass.__init__(self, self.name, autoload, overwrite)
        
        
ent = Entity('Rect_1', 0, 0, 100, 100)
#...
ent.width  = 200
ent.height = 200
ent.save() #saved to: (CWD/data/Entity/Entity_db)["Rect_1"]
```


