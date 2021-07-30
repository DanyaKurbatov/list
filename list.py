from typing import TypeVar, Generic, Union, Any

T = TypeVar('T')


class Item(Generic[T]):

    def __init__(self, data: T):
        self.prev: Union[Item[T], None] = None
        self.next: Union[Item[T], None] = None
        self.data = data

    def delete(self) -> None:
        if self.prev is not None:
            self.prev.next = self.next
        if self.next is not None:
            self.next.prev = self.prev

    def after(self, item: 'Item'[T]) -> None:
        if self.next is not None:
            self.next.prev = item
        item.prev = self
        item.next = self.next
        self.next = item

    def before(self, item: 'Item'[T]) -> None:
        if self.prev is not None:
            self.prev.next = item
        item.prev = self.prev
        item.next = self
        self.prev = item


class MyList(Generic[T]):

    def __init__(self, iterable: Any = None) -> None:
        self.head: Union[Item[T], None] = None
        self.tail: Union[Item[T], None] = None
        if iterable is not None:
            for i in iterable:
                self.append(i)

    def append(self, data: T) -> None:
        if self.tail is not None:
            self.tail.after(Item(data))
            self.tail = self.tail.next
        else:
            self.head = Item(data)
            self.tail = self.head

    def prepend(self, data: T) -> None:
        if self.head is not None:
            self.head.before(Item(data))
            self.head = self.head.prev
        else:
            self.tail = Item(data)
            self.head = self.tail

    def insert(self, index: int, data: T) -> None:
        index = self.__check(index)
        counter = 0
        i = self.head
        while i is not None:
            if counter == index:
                i.before(Item(data))
                if i == self.head:
                    self.head = self.head.prev
                return
            i = i.next
            counter += 1
        raise IndexError('list index out of range')

    def __check(self, index: int) -> int:
        assert isinstance(index, int)
        if index < 0:
            index = len(self) + index
        return index

    def __enumerate(self) -> Any:
        counter = 0
        i = self.head
        while i is not None:
            yield counter, i
            i = i.next
            counter += 1

    def __iter__(self) -> Any:
        i = self.head
        while i is not None:
            yield i.data
            i = i.next

    def __reversed__(self) -> Any:
        i = self.tail
        while i is not None:
            yield i.data
            i = i.prev

    def __contains__(self, data: T) -> bool:
        for i in self:
            if i == data:
                return True
        return False

    def __len__(self) -> int:
        counter = 0
        for _ in self:
            counter += 1
        return counter

    def __getitem__(self, index: int) -> Any:
        if isinstance(index, slice):
            if index.start is None:
                start = 0
            else:
                start = self.__check(index.start)
            if index.stop is None:
                stop = len(self)
            else:
                stop = self.__check(index.stop)
            if index.step is None:
                step = 1
            else:
                step = index.step
                assert isinstance(step, int) and step > 1
            items = []
            for n, i in self.__enumerate():
                if n >= start and n < stop:
                    if (n - start) % step == 0:
                        items.append(i.data)
            return items
        else:
            index = self.__check(index)
            for n, i in self.__enumerate():
                if n == index:
                    return i.data
            raise IndexError('list index out of range')

    def __setitem__(self, index: int, value: int) -> None:
        index = self.__check(index)
        for n, i in self.__enumerate():
            if n == index:
                i.data = value
                return
        raise IndexError('list assignment index out of range')

    def __delitem__(self, index: int) -> None:
        index = self.__check(index)
        for n, i in self.__enumerate():
            if n == index:
                if i == self.head:
                    self.head = self.head.next
                if i == self.tail:
                    self.tail = self.tail.prev
                i.delete()
                return
        raise IndexError('list assignment index out of range')

    def __repr__(self) -> str:
        return ', '.join(map(str, self))


if __name__ == '__main__':
    lst: MyList[int] = MyList()
    lst.append(1)
    lst.prepend(5)
    a = lst[1]
    b = lst[-1]
    for i in lst:
        print(i)
    for i in reversed(lst):
        print(i)
    lst[1] = 3
    lst[-1] = 5
    del lst[0]
    del lst[-1]
    len(lst)
    if lst:
        print(lst)
    if 5 in lst:
        print('in')
    lst = MyList([1, 2, 3, 4])
