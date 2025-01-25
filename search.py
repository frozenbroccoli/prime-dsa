import typing


def walk(array: typing.List, item: float, last_idx: int, factor: int) -> int:
    """
    Do the recursive walk for a binary search while keeping track of the index.

    Parameters
    ----------
    array
        The array being searched on.
    item
        The item being searched for.
    last_idx
        The last index of the original array we landed on.
    factor
        1 or -1 depending on the subtree.

    Returns
    -------
    return
        The index of the item in the array.
    """
    # print(last_idx)
    if not (factor == 1 or factor == -1):
        raise ValueError(f'The parameter factor must be 1 or -1. It cannot be {factor}.')

    if len(array) == 1:
        if array[0] == item:
            return 0
        else:
            return -1

    mid_idx = len(array) // 2
    current_idx = last_idx + factor * mid_idx
    print(current_idx)
    mid = array[mid_idx]
    if mid == item:
        return current_idx
    if mid > item:
        return walk(array[:mid_idx], item, current_idx, -1)
    if mid < item:
        return walk(array[mid_idx + 1:], item, current_idx + 1, 1)


def do_binary_search(array: typing.List[float], item: float) -> int:
    """
    Do a binary search on a list of floats.

    Parameters
    ----------
    array
        The array being searched on.
    item
        The item being searched for.

    Returns
    -------
    return
        The index of the item in the array.
    """
    return walk(array, item, 0, 1)


if __name__ == '__main__':
    print('result: ', do_binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4))
