import random
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass


T = typing.TypeVar('T')


@dataclass
class Node(typing.Generic[T]):
    """
    A node in a linked list.
    """
    value: T
    prev: typing.Union['Node', None] = None
    next: typing.Union['Node', None] = None


class AbstractLinkedList(ABC, typing.Generic[T]):
    """
    The interface of a linked list structure.
    """
    _head: typing.Union[Node[T], None]
    _tail: typing.Union[Node[T], None]
    _length: int

    @abstractmethod
    def get_length(self) -> int:
        """
        Return
        ------
        return
            The length of the list.
        """
        pass

    @abstractmethod
    def insert_at(self, index: int, item: T) -> None:
        """
        Insert a value at the specified index of the list.

        Parameters
        ----------
        index
            The index where the item is to be inserted.
        item
            The item to be inserted.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def remove(self, item: T) -> typing.Union[T, None]:
        """
        Remove all instances of the item from the list.

        Parameters
        ----------
        item
            The item to be removed.

        Return
        ------
        return
            The removed item if it was in the list, else None.
        """
        pass

    @abstractmethod
    def remove_at(self, index: int) -> typing.Union[T, None]:
        """
        Remove the item at the specified index from the list.

        Parameters
        ----------
        index
            The index where the item is to be removed.

        Return
        ------
        return
            The removed item if it was in the list, else None.
        """
        pass

    @abstractmethod
    def append(self, item: T) -> None:
        """
        Append the item at the end of the list.

        Parameters
        ----------
        item
            The item to be appended.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def prepend(self, item: T) -> None:
        """
        Append the item at the beginning of the list.

        Parameters
        ----------
        item
            The item to be prepended.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def pop(self) -> typing.Union[T, None]:
        """
        Remove and return the last item of the list.

        Return
        ------
        return
            The last item of the list if the list is non-empty, else None.
        """
        pass

    @abstractmethod
    def get(self, index: int) -> typing.Union[T, None]:
        """
        Get the item at the specified index in the list.

        Parameters
        ----------
        index
            The index of the item to get.

        Return
        ------
        return
            The item at the specified index if it's in the list, else None.
        """
        pass


class DoublyLinkedList(AbstractLinkedList):
    """
    A doubly linked list.
    """
    def __init__(self):
        self._length = 0
        self._head = None
        self._tail = None

    def _get_node_at(self, index: int) -> Node:
        """
        Get the node at the specified index.

        Parameters
        ----------
        index
            The index of the node to get.

        Return
        ------
        return
            The node at the specified index.
        """
        current = self._head
        for i in range(index):
            assert current is not None, f'Missing node at index {i}'
            current = current.next
        assert current is not None, f'Missing node at index {index}'
        return current

    def __str__(self):
        if self._length == 0:
            return '[]'
        buffer = '['
        current = self._head
        assert current is not None
        buffer += str(current.value)
        for i in range(self._length):
            try:
                current = current.next
                buffer += f', {current.value}'
            except AttributeError:
                break
        buffer += ']'
        return buffer

    def prepend(self, item: T) -> None:
        self._length += 1
        node = Node(value=item)

        if self._head is None:
            self._head = self._tail = node
            return

        node.next = self._head
        self._head.prev = node
        self._head = node

    def insert_at(self, index: int, item: T) -> None:
        if index > self._length:
            raise IndexError(f'Index {index} is greater than the length {self._length} of the list')
        elif index == self._length:
            self.append(item)
            return
        elif index == 0:
            self.prepend(item)
            return

        self._length += 1
        node = Node(value=item)

        current = self._get_node_at(index)

        node.next = current
        node.prev = current.prev
        current.prev.next = node
        current.prev = node

    def append(self, item: T) -> None:
        self._length += 1
        node = Node(value=item)

        if self._tail is None:
            self._head = self._tail = node
            return

        node.prev = self._tail
        self._tail.next = node
        self._tail = node

    def pop(self) -> typing.Union[T, None]:
        if self._length == 0:
            return

        self._length -= 1

        if self._length == 0:
            out = self._head.value
            self._head = self._tail = None
            return out

        out = self._tail.value
        self._tail.prev.next = None
        self._tail = self._tail.prev

        return out

    def remove(self, item: T) -> typing.Union[T, None]:
        current = self._head
        for i in range(self._length):
            assert current is not None
            current = current.next
            if current.value == item:
                break
        else:
            return

        self._length -= 1

        if self._length == 0:
            out = self._head.value
            self._head = self._tail = None
            return out

        if current.next is not None:
            current.prev.next = current.next
            current.next.prev = current.prev
        else:
            current.prev.next = None

        if current == self._head:
            self._head = current.next

        if current == self._tail:
            self._tail = current.prev

        current.prev = current.next = None

        return current.value

    def remove_at(self, index: int) -> typing.Union[T, None]:
        if index >= self._length:
            raise IndexError(f'List index {index} out of range')

        current = self._get_node_at(index)

        self._length -= 1

        if self._length == 0:
            out = self._head.value
            self._head = self._tail = None
            return out

        if current.next is not None:
            current.prev.next = current.next
            current.next.prev = current.prev
        else:
            current.prev.next = None

        if current == self._head:
            self._head = current.next

        if current == self._tail:
            self._tail = current.prev

        current.prev = current.next = None

        return current.value

    def get(self, index: int) -> typing.Union[T, None]:
        if index >= self._length:
            raise IndexError(f'List index {index} out of range')
        current = self._get_node_at(index)
        return current.value

    def get_length(self) -> int:
        return self._length


def main() -> None:
    """
    Main function.
    """
    lst = DoublyLinkedList()
    for _ in range(10):
        lst.append(random.randint(1, 10))

    # Do stuff with the list
    print(lst)


if __name__ == '__main__':
    main()
