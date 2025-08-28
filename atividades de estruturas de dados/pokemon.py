from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Generic, Iterable, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")

@dataclass
class AVLNode(Generic[K, V]):
    key: K
    value: V
    height: int = 1
    left: Optional["AVLNode[K, V]"] = None
    right: Optional["AVLNode[K, V]"] = None

class AVLTree(Generic[K, V]):
    def __init__(self):
        self.root: Optional[AVLNode[K, V]] = None

    def _h(self, n: Optional[AVLNode[K, V]]) -> int:
        return n.height if n else 0

    def _update(self, n: AVLNode[K, V]) -> None:
        n.height = max(self._h(n.left), self._h(n.right)) + 1

    def _bf(self, n: AVLNode[K, V]) -> int:
        return self._h(n.left) - self._h(n.right)

    def _rotate_right(self, y: AVLNode[K, V]) -> AVLNode[K, V]:
        x = y.left
        assert x is not None
        T2 = x.right
        x.right = y
        y.left = T2
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x: AVLNode[K, V]) -> AVLNode[K, V]:
        y = x.right
        assert y is not None
        T2 = y.left
        y.left = x
        x.right = T2
        self._update(x)
        self._update(y)
        return y

    def _rebalance(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        self._update(node)
        bf = self._bf(node)
        if bf > 1 and self._bf(node.left) >= 0:
            return self._rotate_right(node)
        if bf > 1 and self._bf(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1 and self._bf(node.right) <= 0:
            return self._rotate_left(node)
        if bf < -1 and self._bf(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key: K, value: V) -> None:
        def _insert(n: Optional[AVLNode[K, V]], key: K, value: V) -> AVLNode[K, V]:
            if not n:
                return AVLNode(key, value)
            if key < n.key:
                n.left = _insert(n.left, key, value)
            elif key > n.key:
                n.right = _insert(n.right, key, value)
            else:
                n.value = value
                return n
            return self._rebalance(n)
        self.root = _insert(self.root, key, value)

    def search(self, key: K) -> Optional[V]:
        n = self.root
        while n:
            if key < n.key:
                n = n.left
            elif key > n.key:
                n = n.right
            else:
                return n.value
        return None

    def _min_node(self, n: AVLNode[K, V]) -> AVLNode[K, V]:
        while n.left:
            n = n.left
        return n

    def remove(self, key: K) -> bool:
        removed = False
        def _remove(n: Optional[AVLNode[K, V]], key: K) -> Optional[AVLNode[K, V]]:
            nonlocal removed
            if not n:
                return None
            if key < n.key:
                n.left = _remove(n.left, key)
            elif key > n.key:
                n.right = _remove(n.right, key)
            else:
                removed = True
                if not n.left:
                    return n.right
                if not n.right:
                    return n.left
                succ = self._min_node(n.right)
                n.key, n.value = succ.key, succ.value
                n.right = _remove(n.right, succ.key)
            return self._rebalance(n)
        self.root = _remove(self.root, key)
        return removed

    def inorder(self, reverse: bool = False) -> Iterable[Tuple[K, V]]:
        def _in(n: Optional[AVLNode[K, V]]):
            if not n:
                return
            if reverse:
                yield from _in(n.right)
                yield (n.key, n.value)
                yield from _in(n.left)
            else:
                yield from _in(n.left)
                yield (n.key, n.value)
                yield from _in(n.right)
        return _in(self.root)

    def is_balanced(self) -> bool:
        def _check(n: Optional[AVLNode[K, V]]) -> Tuple[bool, int]:
            if not n:
                return True, 0
            lb, lh = _check(n.left)
            rb, rh = _check(n.right)
            h = max(lh, rh) + 1
            balanced = lb and rb and abs(lh - rh) <= 1 and n.height == h
            return balanced, h
        ok, _ = _check(self.root)
        return ok

class PokemonManager:
    def __init__(self):
        self.by_name: AVLTree[str, int] = AVLTree()
        self.by_power: AVLTree[Tuple[int, str], None] = AVLTree()

    def add_pokemon(self, name: str, power: int) -> None:
        current = self.by_name.search(name)
        if current is not None:
            self.by_power.remove((current, name))
        self.by_name.insert(name, power)
        self.by_power.insert((power, name), None)

    def search_by_name(self, name: str) -> Optional[Tuple[str, int]]:
        power = self.by_name.search(name)
        return (name, power) if power is not None else None

    def remove_by_name(self, name: str) -> bool:
        power = self.by_name.search(name)
        if power is None:
            return False
        ok1 = self.by_name.remove(name)
        ok2 = self.by_power.remove((power, name))
        return ok1 and ok2

    def list_by_power_desc(self) -> List[Tuple[str, int]]:
        result: List[Tuple[str, int]] = []
        for (power, name), _ in self.by_power.inorder(reverse=True):
            result.append((name, power))
        return result

    def is_consistent(self) -> bool:
        if not (self.by_name.is_balanced() and self.by_power.is_balanced()):
            return False
        names_from_power = [name for (name, _) in self.list_by_power_desc()]
        names_from_name = [k for k, _ in self.by_name.inorder()]
        return sorted(names_from_power) == sorted(names_from_name)

if __name__ == "__main__":
    mgr = PokemonManager()
    data = [
        ("Pikachu", 55),
        ("Charizard", 120),
        ("Bulbasaur", 49),
        ("Squirtle", 48),
        ("Gengar", 130),
        ("Alakazam", 125),
        ("Snorlax", 110),
        ("Dragonite", 134),
        ("Mewtwo", 154),
        ("Gyarados", 125),
    ]
    for name, power in data:
        mgr.add_pokemon(name, power)

    print("\n=== Busca por nome ===")
    for q in ["Pikachu", "Mewtwo", "Eevee"]:
        res = mgr.search_by_name(q)
        print(res if res else f"{q} não encontrado")

    print("\n=== Listagem por força (desc) ===")
    for name, power in mgr.list_by_power_desc():
        print(f"{name}: {power}")

    print("\n=== Remoções ===")
    for r in ["Charizard", "Bulbasaur", "Inexistente"]:
        ok = mgr.remove_by_name(r)
        print(f"remove {r}: {ok}")

    print("\n=== Listagem após remoções ===")
    for name, power in mgr.list_by_power_desc():
        print(f"{name}: {power}")

    print("\nBalanceadas? ", mgr.by_name.is_balanced(), mgr.by_power.is_balanced())
    print("Consistente? ", mgr.is_consistent())
