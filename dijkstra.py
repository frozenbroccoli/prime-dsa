import math
import dataclasses


@dataclasses.dataclass
class GraphEdge:
    to: int
    weight: int


type WeightedAdjacencyList = list[list[GraphEdge]]


def has_unvisited(seen: list[bool], dists: list[float | int]) -> bool:
    for index, visited in enumerate(seen):
        if not visited and dists[index] < math.inf:
            return True
    return False


def get_lowest_unvisited(seen: list[bool], dists: list[float | int]) -> int:
    lowest = math.inf
    idx = -1
    for index, dist in enumerate(dists):
        if seen[index]:
            continue
        if dist < lowest:
            lowest = dist
            idx = index
    return idx


def dijkstra(
        graph: WeightedAdjacencyList,
        source: int,
        sink: int
    ) -> list[int]:
    seen = len(graph) * [False]
    prev = len(graph) * [-1]
    dists = len(graph) * [math.inf]

    dists[source] = 0
    
    while has_unvisited(seen, dists):
        curr = get_lowest_unvisited(seen, dists)
        seen[curr] = True
        adjs = graph[curr]
        for edge in adjs:
            if seen[edge.to]:
                continue
            dist = dists[curr] + edge.weight
            if dist < dists[edge.to]:
                dists[edge.to] = dist
                prev[edge.to] = curr

    path: list[int] = []
    curr = sink
    while prev[curr] != -1:
        path.append(curr)
        curr = prev[curr]
    if len(path) != 0:
        path.append(source)
        path.reverse()

    return path


def main() -> None:
    graph: WeightedAdjacencyList = [
        [GraphEdge(1, 1)],
        [GraphEdge(3, 1), GraphEdge(4, 1)],
        [GraphEdge(4, 1), GraphEdge(7, 1)],
        [GraphEdge(1, 1), GraphEdge(5, 1)],
        [GraphEdge(1, 1), GraphEdge(2, 1)],
        [GraphEdge(3, 1), GraphEdge(6, 1), GraphEdge(7, 1)],
        [GraphEdge(5, 1), GraphEdge(7, 1)],
        [GraphEdge(2, 1), GraphEdge(6, 1), GraphEdge(5, 1)]
    ]
    source: int = 7
    sink: int = 0
    path = dijkstra(graph, source, sink)
    print(path)


if __name__ == '__main__':
    main()
