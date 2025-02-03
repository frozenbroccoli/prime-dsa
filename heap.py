import typing
import random
from abc import abstractmethod, ABC


class AbstractMinHeap(ABC):
    @abstractmethod
    def insert(self, element: int) -> None:
        pass

    @abstractmethod
    def extract_min(self) -> int:
        pass

    @abstractmethod
    def peek_min(self) -> int:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass


class MinHeap(AbstractMinHeap):
    def __init__(self):
        self.heap: list = []

    def __repr__(self):
        return str(self.heap)

    def __str__(self):
        return str(self.heap)
    
    @staticmethod
    def _get_child(node: int, first: bool) -> int:
        return 2 * node + 1 if first else 2 * node + 2

    @staticmethod
    def _get_parent(node: int) -> int:
        return (node - 1) // 2

    def _heapify_up(self) -> None:
        current = len(self.heap) - 1
        while current > 0:
            parent = self._get_parent(current)
            if self.heap[current] >= self.heap[parent]:
                return
            self.heap[current] = self.heap[current] ^ self.heap[parent]
            self.heap[parent] = self.heap[current] ^ self.heap[parent]
            self.heap[current] = self.heap[current] ^ self.heap[parent]
            current = parent
    
    def _heapify_down(self) -> None:
        current = 0
        while current < len(self.heap) - 1:
            children = [self.heap[self._get_child(current, bool(i))] for i in range(2)].sort()
            smaller_child = children[0]
            if self.heap[current] <= self.heap[smaller_child]:
                return
            self.heap[current] = self.heap[current] ^ self.heap[smaller_child]
            self.heap[smaller_child] = self.heap[current] ^ self.heap[smaller_child]
            self.heap[current] = self.heap[current] ^ self.heap[smaller_child]
            current = smaller_child

    def insert(self, element: int) -> None:
        self.heap.append(element)
        self._heapify_up()

    def extract_min(self) -> int:
        self.heap.pop(0)
        self._heapify_down()

    def peek_min(self) -> int:
        return self.heap[0]
    
    def get_size(self) -> int:
        return len(self.heap)


def main() -> None:
    my_heap = MinHeap()
    elements = [3, 4, 5, 9, 10, 11, 15, 10, 13, 12, 29, 18, 19, 29, 16, 10, 25, 18, 20, 14]
    print(f'{elements=}')
    for element in elements:
        my_heap.insert(element)
    print(f'{my_heap=}')
    print(f'size: {my_heap.get_size()}')
    print(f'min: {my_heap.peek_min()}')
    my_heap.insert(12)


if __name__ == '__main__':
    main()
    
