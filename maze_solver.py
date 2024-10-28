"""
Solve a maze from a text file.
"""
import typing
import copy
from dataclasses import dataclass


type Path = typing.List[Point]
type Grid = typing.List[Path]


@dataclass
class Point:
    """
    A point in a maze, i.e., a maze-cell.
    """
    x: int
    y: int
    symbol: str
    visited: bool = False

    def visit(self) -> None:
        """
        Visit the point.
        Returns
        -------
        None
        """
        self.visited = True

    def __str__(self):
        return self.symbol


@dataclass
class Maze:
    """
    A maze.
    """
    depth: int
    width: int
    maze: Grid

    def __getitem__(self, position: typing.Tuple[int, int]) -> Point:
        """
        Get an item with indices.
        Parameters
        ----------
        position: The [x, y] coordinates of the item to get.

        Returns
        -------
        The item to get.
        """
        x, y = position
        return self.maze[y][x]

    def __setitem__(self, position: typing.Tuple[int, int], point: Point) -> None:
        """
        Set the Point at given indices.
        Parameters
        ----------
        position:
            The [x, y] coordinates of where to set the Point.
        point:
            The new Point.

        Returns
        -------
        None
        """
        x, y = position
        self.maze[y][x] = point

    def __str__(self):
        grid = ''
        for row in self.maze:
            line = ''
            for point in row:
                line += point.symbol
            grid += (line + '\n')
        return grid


def load_maze(file: str) -> Maze:
    """
    Load a maze from a text file. This is not a part
    of the algo, this is what we are handed.
    Parameters
    ----------
    file:
        The file to load the maze from.

    Returns
    -------
    A maze that is a list of Points.
    """
    with open(file, mode='r', encoding='utf-8') as maze_file:
        maze = []
        for y, line in enumerate(maze_file):
            row = []
            for x, symbol in enumerate(line.strip('\n')):
                row.append(Point(x, y, symbol))
            maze.append(row)
    return Maze(depth=len(maze), width=len(maze[0]), maze=maze)


def insert_path(maze: Maze, path: Path, marker: str) -> Maze:
    """
    Insert a path into a maze.
    Parameters
    ----------
    maze:
        The input maze.
    path:
        Path to be inserted.
    marker:
        Symbol to mark the inserted path. Must be one character.

    Returns
    -------
    Maze with the path inserted.
    """
    new_maze = copy.copy(maze)
    for point in path:
        new_maze[point.x, point.y] = Point(point.x, point.y, marker)
    return new_maze


def hop(maze: Maze, current: Point, direction: str) -> Point:
    """
    Hop from a Point to its adjacent Point in the
    given direction.
    Parameters
    ----------
    maze:
        The maze in question.
    current:
        The current point.
    direction:
        The direction to hop to. Choices are 'left',
            'right', 'up', and 'down'.

    Returns
    -------
    The adjacent Point.
    """
    match direction:
        case 'left':
            return maze[current.x - 1, current.y]
        case 'right':
            return maze[current.x + 1, current.y]
        case 'up':
            return maze[current.x, current.y - 1]
        case 'down':
            return maze[current.x, current.y + 1]
        case _:
            raise ValueError(f'Accepted directions are up, down, left, and right')


def walk(
        maze: Maze,
        wall: str,
        current: Point,
        end: Point,
        path: Path
) -> bool:
    """
    Take one step in a maze.
    Parameters
    ----------
    maze:
        The maze.
    wall:
        The symbol denoting a wall.
    current:
        The current Point.
    end:
        The ending Point.
    path:
        The path to the destination.

    Returns
    -------
    The solved path.
    """
    # Base cases
    # 1. Off the grid
    if (current.x < 0) or (current.x >= maze.width) or (current.y < 0) or (current.y >= maze.depth):
        return False

    # 2. On a wall
    if current.symbol == wall:
        return False

    # 3. Already seen
    if current.visited:
        return False

    # 4. Reached destination
    if current == end:
        path.append(end)
        return True

    # Recursive cases
    # 1. Pre
    current.visit()
    path.append(current)

    # 2. Recurse
    for direction in ['right', 'up', 'left', 'down']:
        if walk(maze, wall, hop(maze, current, direction), end, path):
            return True

    # 3. Post
    path.pop()

    return False


def solve(
        maze: Maze,
        wall: str,
        start: Point,
        end: Point
) -> Path:
    """
    Solve a text based maze from a list of strings. Each
    element of the list is a line in the maze.

    Parameters
    ----------
    maze:
        The maze as a numpy array.
    wall:
        The character that denotes a wall.
    start:
        Coordinates of the starting point.
    end:
        Coordinates of the ending point.

    Returns
    -------
    return:
        The solved maze.
    """
    path = []
    walk(maze, wall, start, end, path)
    return path


def main() -> None:
    """
    Main function.
    Returns
    -------
    None
    """
    loaded_maze = load_maze('res/maze_2.txt')
    print('Puzzle:\n-------')
    print(loaded_maze)
    wall = '█'
    start = Point(x=0, y=0, symbol='S')
    end = Point(x=loaded_maze.width-1, y=loaded_maze.depth-2, symbol='E')
    path = solve(loaded_maze, wall, start, end)
    solved_maze = insert_path(loaded_maze, path, ':')
    print('Solution:\n--------')
    print(solved_maze)


if __name__ == '__main__':
    main()
