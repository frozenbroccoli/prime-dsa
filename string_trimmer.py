"""
Make a move on a string containing only B's and A's.
In one move remove a substr AB or BB. Find the
minimum length of the string after any sequence of
such moves.
"""
import typing
from dataclasses import dataclass


@dataclass
class StringNode:
    """
    A node in a special binary tree.
    """
    key: str
    left: typing.Optional['StringNode'] = None
    right: typing.Optional['StringNode'] = None
    left_mover: str = 'AB'
    right_mover: str = 'BB'

    def __str__(self):
        return self.key

    def spawn(self, direction: str) -> typing.Union['StringNode', None]:
        """
        Spawn a child StringNode.
        Parameters
        ----------
        direction
            Which child to spawn, left or right.

        Returns
        -------
        return
            Child StringNode if successfully spawned else None.
        """
        match direction:
            case 'left':
                index = self.key.find(self.left_mover)
                if index != -1:
                    self.left = StringNode(key=self.key[:index] + self.key[index + len(self.left_mover):])
                    return self.left
                return None
            case 'right':
                index = self.key.find(self.right_mover)
                if index != -1:
                    self.right = StringNode(key=self.key[:index] + self.key[index + len(self.right_mover):])
                    return self.right
                return None
            case _:
                raise ValueError('Accepted values are left and right')


def walk(current: StringNode, root_sequence: str, results: typing.List[str]) -> None:
    """
    Walk on a binary tree and explore all possibilities.
    Parameters
    ----------
    current
        The current StringNode.
    root_sequence
        The key of the root node in the tree.
    results
        All the keys on the leaves.

    Returns
    -------
    return
        True if the entire tree is scanned, else False.
    """
    # Base case
    # No more moves
    if current is None:
        return None

    # Recurse
    results.append(current.key)

    walk(current.spawn('left'), root_sequence, results)
    walk(current.spawn('right'), root_sequence, results)


def solve(sequence: str) -> int:
    """
    Find the shortest possible sequence.
    Parameters
    ----------
    sequence
        The problem sequence.

    Returns
    -------
        The length of the shortest string.
    """
    node = StringNode(key=sequence)
    results = []
    walk(node, sequence, results)
    sizes = [len(result) for result in results]
    return min(sizes)


def main() -> None:
    """
    Main function.
    Returns
    -------
        None
    """
    sequence = 'BABBA'
    print(solve(sequence))


if __name__ == '__main__':
    main()
