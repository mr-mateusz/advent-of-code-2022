from dataclasses import dataclass
from functools import cache
from typing import Set, List, Optional, Dict, Tuple

from tqdm import tqdm

from day_02.solution import yield_rows


@dataclass
class Node:
    name: str
    value: int


@dataclass
class AccessibleNode:
    name: str
    distance: int


@dataclass
class Edge:
    nodes: Set
    value: int

    def __init__(self, _from: str, _to: str, value: int = 1) -> None:
        self.nodes = {_from, _to}
        self.value = value


class GraphEdges:
    def __init__(self) -> None:
        self.edges: List[Edge] = []

    def __len__(self) -> int:
        return len(self.edges)

    def get_edge(self, node_names: Set) -> Optional[Edge]:
        for edge in self.edges:
            if edge.nodes == node_names:
                return edge
        return None

    def add(self, _from: str, _to: str, value: int = 1, overwrite: bool = True) -> bool:
        if found := self.get_edge({_from, _to}):
            if found.value != value:
                raise ValueError
            if overwrite:
                # todo - delete edge and create new one
                return True
            else:
                return False

        self.edges.append(Edge(_from, _to, value))
        return True

    def get_accessible_nodes(self, node_name: str) -> List[AccessibleNode]:
        return [AccessibleNode(list(e.nodes.difference([node_name]))[0], e.value) for e in self.edges if
                node_name in e.nodes]

    @cache
    def distance(self, _from: str, _to: str) -> Optional[int]:
        visited_nodes = [(_from, 0)]

        for node in visited_nodes:
            if node[0] == _to:
                return node[1]

            for next_node in self.get_accessible_nodes(node[0]):
                possible_direction = (next_node.name, node[1] + next_node.distance)
                if possible_direction[0] not in [v[0] for v in visited_nodes]:
                    visited_nodes.append(possible_direction)
                else:
                    already_added = next(v for v in visited_nodes if v[0] == possible_direction[0])
                    if already_added[1] > possible_direction[1]:
                        visited_nodes.remove(already_added)
                        visited_nodes.append(possible_direction)
        return None


def parse_input(path: str) -> Tuple[Dict[str, Node], GraphEdges]:
    nodes = {}
    edges = GraphEdges()
    for line in yield_rows(path):
        tokens = line.split(maxsplit=9)
        name = tokens[1]
        flow = int(tokens[4].split('=')[1].strip(';'))
        accessible_nodes = tokens[9].split(', ')

        nodes[name] = Node(name, flow)

        for accessible_node in accessible_nodes:
            edges.add(name, accessible_node)

    return nodes, edges


def check_paths(current_node: str, nodes_to_visit: List[str], nodes: Dict[str, Node],
                edges: GraphEdges, time_left: int, total_pressure_released: int) -> int:
    total_pressure_released += nodes[current_node].value * time_left

    pressures_released = []
    for destination in nodes_to_visit:
        move_and_open_time = edges.distance(current_node, destination) + 1
        if move_and_open_time <= time_left:
            remaining_nodes = nodes_to_visit[:]
            remaining_nodes.remove(destination)
            pressures_released.append(check_paths(destination, remaining_nodes,
                                                  nodes, edges, time_left - move_and_open_time,
                                                  total_pressure_released))

    return max(pressures_released, default=total_pressure_released)


def _find_all_paths(current_node: str, nodes_to_visit: List[str], nodes: Dict[str, Node],
                    edges: GraphEdges, time_left: int, total_pressure_released: int,
                    visited_nodes: List, to_return: List[Tuple]) -> List[Tuple[List[str], int]]:
    total_pressure_released += nodes[current_node].value * time_left

    to_return.append((visited_nodes[:], total_pressure_released))

    pressures_released = []
    for destination in nodes_to_visit:
        move_and_open_time = edges.distance(current_node, destination) + 1
        if move_and_open_time <= time_left:
            remaining_nodes = nodes_to_visit[:]
            remaining_nodes.remove(destination)
            visited_nodes_next = visited_nodes[:]
            visited_nodes_next.append(destination)

            pressures_released.extend(_find_all_paths(destination, remaining_nodes,
                                                      nodes, edges, time_left - move_and_open_time,
                                                      total_pressure_released, visited_nodes_next, to_return[:]))

    if not pressures_released:
        return [(visited_nodes, total_pressure_released)] + to_return

    return pressures_released + to_return


if __name__ == '__main__':
    path = './input.txt'

    initial_node_name = 'AA'
    total_time = 30

    nodes, edges = parse_input(path)

    meaningful_nodes = [node.name for node in nodes.values() if node.value > 0]

    # Part 1
    max_pressure = check_paths(initial_node_name, meaningful_nodes, nodes, edges, total_time, 0)
    print(max_pressure)

    # Part 2
    total_time = 26

    all_possible_orders = _find_all_paths(initial_node_name, meaningful_nodes, nodes, edges, total_time, 0, [], [])

    # squash possible orders
    orders = {}
    for order, value in all_possible_orders:
        order = tuple(sorted(order))
        try:
            if orders[order] < value:
                orders[order] = value
        except KeyError:
            orders[order] = value

    best_val = 0
    for order, value in tqdm(orders.items()):
        elephant_meaningful_nodes = list(set(meaningful_nodes).difference(order))

        elephant_pressure_released = check_paths(initial_node_name, elephant_meaningful_nodes, nodes, edges, total_time,
                                                 0)

        if value + elephant_pressure_released > best_val:
            best_val = value + elephant_pressure_released
    print(best_val)
