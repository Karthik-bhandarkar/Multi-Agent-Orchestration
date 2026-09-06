from typing import Any, Optional


class Node:
    """Doubly linked list node storing a key-value pair."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LRUCache:
    """
    O(1) Least Recently Used Cache.

    Data Structures:
      - dict[key] -> Node          : O(1) lookup
      - Doubly linked list          : O(1) reordering / eviction
        head (MRU side) <-> ... <-> tail (LRU side)

    Sentinel nodes (self.head, self.tail) eliminate None-checks
    at list boundaries.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self.map: dict[Any, Node] = {}

        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Optional[Any]:
        if key not in self.map:
            return None
        node = self.map[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        new_node = Node(key, value)
        self.map[key] = new_node
        self._add_to_front(new_node)

        if len(self.map) > self.capacity:
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.map[lru_node.key]

    def __len__(self) -> int:
        return len(self.map)

    def keys(self) -> list:
        """Debug helper: returns keys ordered MRU -> LRU."""
        result = []
        current = self.head.next
        while current is not self.tail:
            result.append(current.key)
            current = current.next
        return result
