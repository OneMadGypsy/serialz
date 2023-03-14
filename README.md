# serialz
A tiny python package for (de)serializing class data from/to `json`, `pkl` or an entry in a `shelve` database


### features:
* **save**: serialize class as `json`, `pkl` or a `shelve` database entry
* **load**: deserialize `json`, `pkl` or a database entry to class
* **delete**: file (`json`, `pkl`) or database entry 
* optionally autoload saved state when class is instanced
* optionally overwrite saved state when class is instanced
* data destinations are internally created/managed



## info:

The system works by serializing the class `__dict__` (save), and updating the class `__dict__` with deserialized data (load).

You can extend `JSONClass`, `PKLClass` or `DBClass` to save/load your class to/from `json`, `pkl` or `shelve` database (respectively). If the serialization data does not exist when the class is instanced, it will create it. If the serialization data does exist, and `autoload` is `True`, the class will be instanced with the deserialized data, regardless of the init data. You can `save()`, `load()` or `delete()` at any time.

All 3 serialization classes have the same interface
| argument  | description                                    | default |
| --------- |:---------------------------------------------- |:------- |
| id        | becomes file name or database entry name       | None    |
| autoload  | True/False autoload when instanced             | True    |
| overwrite | True/False overwrite saved data when instanced | False   |

In `serialz.py` is a constant named `ROOT`. This is the name of the folder wthin the CWD that will be used to store serialized data. The default is "data". Subfolders are created within this directory, named after the `type` of the serializers subclass. Below are possible destinations, based on a serializer subclass named `Entity` with an `id` of `"default"`.

| class         | destinations                                           |
|:------------- |:------------------------------------------------------ |
| **JSONClass** | `f'{os.getcwd()}/data/Entity/default.json'`            |
| **PKLClass**  | `f'{os.getcwd()}/data/Entity/default.pkl'`             |
| **DBClass**   | (`f'{os.getcwd()}/data/Entity/Entity_db'`)["default"]  |


## example:

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
        DBClass.__init__(self, self.name, autoload, overwrite)
        
        
ent = Entity('Rect_1', 0, 0, 100, 100)
#...
ent.width  = 200
ent.height = 200
ent.save()
```


