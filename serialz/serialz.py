import os, json, pickle, shelve
from typing import Callable

#folder within CWD to be used for data storage
#will be created if it doesn't exist
ROOT = 'data'

#serializer base
class SerialClass:
    SUBCLASS_MSG    = '{} must be instanced through a subclass.'
    DESTINATION_MSG = ('\n\tself.destname must be set in SerialClass subclass'
                       '\n\tthis should involve self._id or self._type (depending on serializer style)')
    
    #decorator for IO
    def voodoo(func:Callable) -> Callable:
        def inner(self):
            if not self.__path: raise Exception(SerialClass.DESTINATION_MSG)
            func(self)
        return inner
        
    @property       #return full path
    def dest(self) -> str:
        return self.__path
    
    @dest.setter    #set path with destname joined to location
    def destname(self, name:str) -> None:
        self.__path = os.path.join(self.__loc, name)

    def __init__(self, id:str, baseclass:type):
        #store id
        self.id    = id
        
        #get type
        self._type = type(self).__name__
        
        #root data directory create 
        if not os.path.isdir(ROOT):
            os.mkdir(ROOT)
            
        #ensure type is not a base
        if self._type in (baseclass.__name__, SerialClass.__name__):
            raise Exception(SerialClass.SUBCLASS_MSG.format(self._type))
            
        #init internal path
        self.__path = None
        
        #init internal location ~ absolute
        self.__loc  = os.path.join(os.getcwd(), os.path.join(ROOT, self._type))
        
        #type directory create 
        if not os.path.isdir(self.__loc):
            os.mkdir(self.__loc)
        

#saved as: {root}/{type}/{id}.json
class JSONClass(SerialClass):
    def __init__(self, id:str, autoload:bool=True, overwrite=False):
        SerialClass.__init__(self, id, JSONClass)
            
        #set filename
        self.destname = f'{self.id}.json'
        
        #json overwrite or create
        if overwrite or not os.path.isfile(self.dest):
            self.save()
            return #skip loading
            
        #load json
        if autoload: self.load()

    @SerialClass.voodoo
    def save(self) -> None:
        json.dump(self.__dict__, open(self.dest, "w"))

    @SerialClass.voodoo
    def load(self) -> None:
        self.__dict__.update(json.load(open(self.dest, "r")))
     
    @SerialClass.voodoo 
    def delete(self) -> None:
        os.remove(self.dest)


#saved as: {root}/{type}/{id}.pkl
class PKLClass(SerialClass):
    def __init__(self, id:str, autoload:bool=True, overwrite=False):
        SerialClass.__init__(self, id, PKLClass)
            
        #set filename
        self.destname = f'{self.id}.pkl'
        
        #pkl overwrite or create
        if overwrite or not os.path.isfile(self.dest):
            self.save()
            return #skip loading
            
        #load pkl
        if autoload: self.load()

    @SerialClass.voodoo
    def save(self) -> None:
        pickle.dump(self.__dict__, open(self.dest, "wb"))

    @SerialClass.voodoo
    def load(self) -> None:
        self.__dict__.update(pickle.load(open(self.dest, "rb")))

    @SerialClass.voodoo
    def delete(self) -> None:
        os.remove(self.dest)


#saved as: ({root}/{type}/{type}_db)[id]    
class DBClass(SerialClass):
    def __init__(self, id:str, autoload:bool=True, overwrite=False):
        SerialClass.__init__(self, id, DBClass)
    
        #set database name
        self.destname = f"{self._type}_db"
    
        #database update or create
        with shelve.open(self.dest) as db:
            #entry or None
            entry = db.get(self.id)
            
            #entry overwrite or create
            if overwrite or not entry:
                db[self.id] = self.__dict__
                return #skip loading
                
            #load entry
            if autoload and entry: self.__dict__.update(entry)
                
    @SerialClass.voodoo
    def save(self) -> None:
        with shelve.open(self.dest) as db:
            db[self.id] = self.__dict__

    @SerialClass.voodoo
    def load(self) -> None:
        with shelve.open(self.dest) as db:
            if (entry := db.get(self.id)):
                self.__dict__.update(entry)
      
    @SerialClass.voodoo         
    def delete(self):
        with shelve.open(self.dest) as db:
            if db.get(self.id): del db[self.id]

