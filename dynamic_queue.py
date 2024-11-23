import typing
from abc import ABC, abstractmethod
from linked_list import ListNode


T = typing.TypeVar('T')


class AbstractQueue(ABC, typing.Generic[T]):
    """
    The interface class of a queue.
    """
    _front: typing.Union[ListNode[T], None]
    _rear: typing.Union[ListNode[T], None]
    _size: int

    @abstractmethod
    def enqueue(self, item: T) -> None:
        """
        Enqueue an item at the back of the queue.

        Parameters
        ----------
        item
            The item on the enqueued node.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def dequeue(self) -> T:
        """
        Dequeue an item from the front of the queue.

        Return
        ------
        return
            The item on the dequeued node.
        """
        pass

    @abstractmethod
    def get_size(self) -> int:
        """
        Get the current size of the queue.

        Return
        ------
        return
            The size of the queue.
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check whether the queue is currently empty.

        Return
        ------
        return
            True if the queue is empty, else False.
        """
        pass


class SingleEndedQueue(AbstractQueue):
    """
    A single ended queue that can only enqueue
    at the rear and dequeue at the front.
    """
    def __init__(self, item: T):
        self._front = ListNode(item)
        self._rear = self._front
        self._size = 1

    def __getitem__(self, index):
        current = self._front
        for i in range(index):
            current = current.prev
        return current

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < self._size:
            result = self.__getitem__(self._index)
            self._index += 1
            return result
        else:
            raise StopIteration

    def enqueue(self, item: T) -> None:
        new = ListNode(item, next=self._rear)
        self._rear.prev = new
        self._rear = new
        self._size += 1

    def dequeue(self) -> T:
        tmp = self._front
        assert tmp is not None, "Cannot dequeue from an empty queue"
        if tmp.prev is not None:
            tmp.prev.next = None
        self._front = tmp.prev
        tmp.prev = None
        self._size -= 1
        return tmp.value

    def get_size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0


def main() -> None:
    """
    Main function to test the module.
    """
    my_queue = SingleEndedQueue(0)
    for i in range(1, 11):
        my_queue.enqueue(i)

    print('My queue from front to rear:')

    for node in my_queue:
        print(node)

    print(f'Size: {my_queue.get_size()}')

    print(f'Dequeued node: {my_queue.dequeue()}')

    print(f'Size after dequeue: {my_queue.get_size()}\n')

    for i in range(my_queue.get_size()):
        print(f'Dequeue {i + 1}: {my_queue.dequeue()}')
        print(f'Current size: {my_queue.get_size()}')
        print(f'Queue empty: {my_queue.is_empty()}')


if __name__ == '__main__':
    main()
