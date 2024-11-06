from typing import Self


class ObjList:
    """
    Класс, представляющий элемент двусвязного списка.
    
    Attrs:
        __next (ObjList | None): Ссылка на следующий элемент списка
        __prev (ObjList | None): Ссылка на предыдущий элемент списка
        __data (str): Данные, которые хранятся в элементе списка
    """
    
    def __init__(self, data: str) -> None:
        """
        Инициализирует элемент двузсвязного списка с данными.
        
        Args:
            data (str): Данные в виде строки для хранения в элементе списка
        """
        
        self.__next: Self | None = None
        self.__prev: Self | None = None
        self.__data: str = data

    def set_next(self, obj: Self | None) -> None:
        """
        Устанавливает ссылку на следующий элемент.
        """
        
        self.__next = obj
    
    def get_next(self) -> Self | None:
        """
        Возвращает следующий элемент.
        """
        
        return self.__next
    
    def set_prev(self, obj: Self | None) -> None:
        """
        Устанавливает ссылку на предыдущий элемент.
        """
        
        self.__prev = obj
    
    def get_prev(self) -> Self | None:
        """
        Возвращает предыдущий элемент.
        """
        
        return self.__prev
    
    def set_data(self, data: str) -> None:
        """
        Помещает данные в текущий элемент.
        """
        
        self.__data = data
    
    def get_data(self) -> str:
        """
        Возвращает данные из элемента.
        """
        
        return self.__data
    
    def __repr__(self) -> str:
        """
        Возвращает строковое представление данных элемента списка.
        """
        
        return self.__data

 
class LinkedList:
    """
    Класс, представляющий двусвязный список.
    
    Attrs:
        head (ObjList): Первый элемент списка
        tail (ObjList): Последний элемент списка
    """
    
    def __init__(self):
        """
        Инициализирует пустой двусвязный список.
        """
        
        self.head: ObjList | None = None
        self.tail: ObjList | None = None
        self.__objects: list[ObjList] = []
    
    def add_obj(self, obj: ObjList) -> None:
        """
        Добавляет новый объект в конец списка и обновляет ссылки если необходимо.
        
        Args:
            obj (ObjList): Новый объект для добавления
        """
        
        self.__objects.append(obj)
        
        if self.tail:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
            self.tail = obj
        else:
            self.head = obj
            self.tail = obj               
    
    def remove_obj(self) -> None:
        """
        Удаляет последний объект из списка и обноаляет ссылки.
        Если список пуст, выодит в консоль сообщение.
        """
        
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
            
    def get_data(self) -> list[ObjList]:
        """
        Возвращает список всех объектов хранящихся в списке.
        """
        
        return self.__objects
    
    def __str__(self) -> str:
        """
        Возвращает строковое представления списка.
        """
        
        return f"LinkedList: {self.__objects}"
