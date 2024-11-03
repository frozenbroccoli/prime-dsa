import typing
import random


type Number = typing.Union[int, float]
type NumberArray = typing.List[Number]


def do_partition(array: NumberArray, low: int, high: int) -> int:
    """
    Do a weak sort on a section of an unsorted array.

    Parameters
    ----------
    array
        The unsorted array.
    low
        The starting index of the subarray.
    high
        The final index of the subarray.

    Return
    ------
    return
        The index of the pivot used in the weak sort.
    """
    pivot = array[high]
    index = low - 1

    for i in range(low, high):
        if array[i] <= pivot:
            index += 1
            tmp = array[index]
            array[index] = array[i]
            array[i] = tmp

    index += 1
    array[high] = array[index]
    array[index] = pivot

    return index


def sort(array: NumberArray, low: int, high: int) -> None:
    """
    Do QuickSort and sort a subarray of the input array in place.

    Parameters
    ----------
    array
        The array to sort.
    low
        The starting index of the subarray to be sorted.
    high
        The final index of the subarray to be sorted.

    Return
    ------
    return
        None
    """
    if low >= high:
        return
    pivot_index = do_partition(array, low, high)
    sort(array, low, pivot_index - 1)
    sort(array, pivot_index + 1, high)


def do_quick_sort(array: NumberArray) -> None:
    """
    Sort a list in place using QuickSort.

    Parameters
    ----------
    array
        The unsorted list.

    Return
    ------
    return
        None
    """
    sort(array, 0, len(array) - 1)


def main() -> None:
    """
    Main function.
    """
    array = [random.randint(1, 10) for _ in range(random.randint(5, 10))]
    print(f'Unsorted array: {array}')
    do_quick_sort(array)
    print(f'Sorted array: {array}')


if __name__ == '__main__':
    main()
