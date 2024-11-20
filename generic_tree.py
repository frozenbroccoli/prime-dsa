import typing
import dataclasses
from abc import abstractmethod, ABC


T = typing.TypeVar('T')


@dataclasses.dataclass
class TreeNode(typing.Generic[T]):
    """
    A node in a tree.
    """
    value: T
    parent: typing.Union['TreeNode[T]', None] = None
    children: typing.List['TreeNode[T]'] = dataclasses.field(default_factory=list)

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def add_child(self, child: 'TreeNode[T]') -> None:
        """
        Add a child node to this node.

        Parameters
        ----------
        child
            The child node to add.

        Return
        ------
        return
            None
        """
        self.children.append(child)
        child.parent = self

    def visit(self, action: typing.Callable[['TreeNode[T]'], typing.Any]) -> typing.Any:
        """
        Visit the node. Visiting can be any arbitrary action.

        Parameters
        ----------
        action
            The callable that implements the action to be
                performed on visit.

        Return
        ------
        return
            Anything returned by the arbitrary action.
        """
        return action(self)


class AbstractTree(ABC, typing.Generic[T]):
    """
    The abstract base class of a tree.
    """
    root: typing.Union[TreeNode[T], None]

    @abstractmethod
    def insert(self, item: T, parent: TreeNode[T]) -> None:
        """
        Insert a node to the tree with the given item as its value.

        Parameters
        ----------
        item
            The value of the new node.
        parent
            The parent node of the new node.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def find(self, item: T) -> typing.Union[TreeNode[T], None]:
        """
        Find a node by its value.

        Parameters
        ----------
        item
            The value to find the node by.

        Return
        ------
        return
            The first node with the given value found in the search.
            None if the node doesn't exist.
        """
        pass

    @abstractmethod
    def traverse_preorder(
            self,
            start: typing.Optional[TreeNode[T]],
            visit: typing.Callable[[TreeNode[T]], None]
    ) -> None:
        """
        Traverse the tree in preorder.

        Parameters
        ----------
        start
            The node where the traversal starts. The default is the root.
        visit
            A callable that visits a node and returns None.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def traverse_postorder(
            self,
            start: typing.Optional[TreeNode[T]],
            visit: typing.Callable[[TreeNode[T]], None]
    ) -> None:
        """
        Traverse the tree in postorder.

        Parameters
        ----------
        start
            The node where the traversal starts. The default is the root.
        visit
            A callable that visits a node and returns None.

        Return
        ------
        return
            None
        """
        pass

    @abstractmethod
    def remove(self, node: TreeNode[T]) -> None:
        """
        Remove a node and all its children from the tree.

        Parameters
        ----------
        node
            The node to remove.

        Return
        ------
        return
            None
        """
        pass


class GenericTree(AbstractTree):
    """
    A general tree with each node having an arbitrary
    number of children.
    """
    def __init__(self, item: typing.Optional[T]):
        if item is not None:
            self.root = TreeNode(value=item)
        else:
            self.root = None

    def __repr__(self):
        pass

    def insert(self, item: T, parent: TreeNode[T]) -> None:
        parent.add_child(TreeNode(value=item))

    def find(self, item: T) -> typing.Union[TreeNode[T], None]:
        def walk(value: T, current: TreeNode[T]) -> typing.Union[TreeNode[T], None]:
            """
            Walk the tree starting from the given node and
            find the desired node.

            Parameters
            ----------
            value
                The value contained in the desired node.
            current
                The current node from where the search begins.

            Return
            ------
            return
                The desired node in case of a successful search, else None.
            """
            if current.value == value:
                return current

            for child in current.children:
                return walk(value, child)

        return walk(item, self.root)

    def traverse_postorder(
            self,
            start: typing.Optional[TreeNode[T]],
            visit: typing.Callable[[TreeNode[T]], None]
    ) -> None:
        def walk(current: TreeNode[T]) -> None:
            """
            Traverse the tree and visit the node when all its children
            have been visited.

            Parameters
            ----------
            current
                The current node in the tree.

            Return
            ------
            return
                None
            """
            for child in current.children:
                walk(child)

            visit(current)

        walk(start)

    def traverse_preorder(
            self,
            start: typing.Optional[TreeNode[T]],
            visit: typing.Callable[[TreeNode[T]], None]
    ) -> None:
        def walk(current: TreeNode[T]) -> None:
            """
            Visit the current node and continue to traverse the tree.

            Parameters
            ----------
            current
                The current node in the tree.

            Return
            ------
            return
                None
            """
            visit(current)

            for child in current.children:
                walk(child)

        walk(start)

    def remove(self, node: TreeNode[T]) -> None:
        node.parent.children.remove(node)
        node.parent = None
        node.children.clear()
        del node


def main() -> None:
    """
    Main function to run the module for tests.
    """
    my_tree = GenericTree(0)

    for i in range(1, 4):
        my_tree.insert(i, my_tree.root)

    for node in my_tree.root.children:
        for i in range(1, 3):
            my_tree.insert(node.value + i, node)
        for child in node.children:
            for j in range(1, 3):
                my_tree.insert(child.value + j, child)

    print(f'Root: \n{my_tree.root}')
    print(f'Primary children: \n{my_tree.root.children}')
    print(f'Secondary children: \n{[child for node in my_tree.root.children for child in node.children]}')
    print(f'Tertiary children: \n{[grandchild for node in my_tree.root.children for child in node.children
                                   for grandchild in child.children]}')

    print(f'Traversing pre-order: ')
    my_tree.traverse_preorder(start=my_tree.root, visit=print)

    print('Traversing post-order: ')
    my_tree.traverse_postorder(start=my_tree.root, visit=print)


if __name__ == '__main__':
    main()

