import random
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass


T = typing.TypeVar('T')


@dataclass
class ListNode(typing.Generic[T]):
    """
    A node in a linked list.
    """
    value: T
    prev: typing.Union['ListNode', None] = None
    next: typing.Union['ListNode', None] = None


class AbstractList(ABC, typing.Generic[T]):
    """
    The interface of a list data structure.
    """
    _head: typing.Union[ListNode[T], None]
    _tail: typing.Union[ListNode[T], None]
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
        Remove the first instance of the item from the list.

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


class DoublyLinkedList(AbstractList):
    """
    A doubly linked list.
    """
    def __init__(self):
        self._length = 0
        self._head = None
        self._tail = None
        self._item_type: typing.Optional[typing.Type[T]] = None

    def _set_item_type(self, item: T) -> None:
        """
        Set item type of the list instance to ensure homogeneity.

        Parameters
        ----------
        item
            The item being added to the list.

        Return
        ------
        return
            None
        """
        if self._item_type is None:
            self._item_type = type(item)

    def _ensure_homogeneity(self, item: T) -> None:
        """
        Enforce the list's homogeneity.

        Parameters
        ----------
        item
            The item being added to the list.
        """
        self._set_item_type(item)
        if not isinstance(item, self._item_type):
            raise TypeError(f'Expected item of type {self._item_type}, but got {type(item)} instead')

    def _get_node_at(self, index: int) -> ListNode:
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

    def _remove(self, node: ListNode) -> T:
        """
        Remove the given node from the list.

        Parameters
        ---------
        node
            The node to remove.

        Return
        ------
        return
            The value contained in the node.
        """
        self._length -= 1

        if self._length == 0:
            out = self._head.value
            self._head = self._tail = None
            return out

        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev

        if node == self._head:
            self._head = node.next

        if node == self._tail:
            self._tail = node.prev

        node.prev = node.next = None

        return node.value

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

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.get_length()

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __setitem__(self, index: int, item: T) -> None:
        self.remove_at(index)
        self.insert_at(index, item)

    def prepend(self, item: T) -> None:
        self._ensure_homogeneity(item)

        self._length += 1
        node = ListNode(value=item)

        if self._head is None:
            self._head = self._tail = node
            return

        node.next = self._head
        self._head.prev = node
        self._head = node

    def insert_at(self, index: int, item: T) -> None:
        self._ensure_homogeneity(item)

        if index < 0 or index > self._length:
            raise IndexError(f'Index {index} is greater than the length {self._length} of the list')
        elif index == self._length:
            self.append(item)
            return
        elif index == 0:
            self.prepend(item)
            return

        self._length += 1
        node = ListNode(value=item)

        current = self._get_node_at(index)

        node.next = current
        node.prev = current.prev
        current.prev.next = node
        current.prev = node

    def append(self, item: T) -> None:
        self._ensure_homogeneity(item)

        self._length += 1
        node = ListNode(value=item)

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
            if current.value == item:
                break
            current = current.next
        else:
            return

        return self._remove(current)

    def remove_at(self, index: int) -> T:
        if index < 0 or index >= self._length:
            raise IndexError(f'List index {index} out of range')

        current = self._get_node_at(index)

        return self._remove(current)

    def get(self, index: int) -> typing.Union[T, None]:
        if index < 0 or index >= self._length:
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
