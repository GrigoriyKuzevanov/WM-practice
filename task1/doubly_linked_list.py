from typing import Self


class ObjList:
    def __init__(self, data: str):
        self.__next = None
        self.__prev = None
        self.__data = data

    def set_next(self, obj: Self | None):
        self.__next = obj
    
    def get_next(self):
        return self.__next
    
    def set_prev(self, obj: Self | None):
        self.__prev = obj
    
    def get_prev(self):
        return self.__prev
    
    def set_data(self, data: str):
        self.__data = data
    
    def get_data(self):
        return self.__data
    
    def __repr__(self):
        return self.__data

 
class LinkedList:
    def __init__(self):
        self.head: ObjList | None = None
        self.tail: ObjList | None = None
        self.__objects: list[ObjList] = []
    
    def add_obj(self, obj: ObjList):
        self.__objects.append(obj)
        
        if self.tail:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
            self.tail = obj
        else:
            self.head = obj
            self.tail = obj               
    
    def remove_obj(self):
        if not self.__objects:
            print("List is empty!")
            return

        self.__objects.pop()
        
        if self.__objects:
            self.tail = self.__objects[-1]
            self.tail.set_next(None)
        else:
            self.head = None
            self.tail = None
            
    def get_data(self):
        return self.__objects
    
    def __str__(self):
        return f"LinkedList: {self.__objects}"
