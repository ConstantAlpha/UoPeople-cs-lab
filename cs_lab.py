#!/usr/bin/env python3
"""
UoPeople CS Lab CLI
Data Structures & Algorithms demonstrations for:
  CS 1102 Programming 1 | CS 1103 Programming 2 | CS 3303 Data Structures
  CS 3304 Analysis of Algorithms | CS 2203 Databases

Run:  python cs_lab.py
"""

import random
import time
from collections import deque


# ---------------------------------------------------------------------------
# CS 3303 — Stack (LIFO): browser back button / undo
# ---------------------------------------------------------------------------
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


# ---------------------------------------------------------------------------
# CS 3303 — Queue (FIFO): printer queue / BFS frontier
# ---------------------------------------------------------------------------
class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, x):
        self._items.append(x)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def front(self):
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"


# ---------------------------------------------------------------------------
# CS 3303 — Singly Linked List: O(1) insert/delete at head
# ---------------------------------------------------------------------------
class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def insert_head(self, value):
        self.head = _Node(value, self.head)
        self._size += 1

    def delete_head(self):
        if self.head is None:
            raise IndexError("delete from empty list")
        val = self.head.value
        self.head = self.head.next
        self._size -= 1
        return val

    def insert_tail(self, value):
        node = _Node(value)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self._size += 1

    def search(self, value):
        cur, idx = self.head, 0
        while cur:
            if cur.value == value:
                return idx
            cur, idx = cur.next, idx + 1
        return -1

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"LinkedList({self.to_list()})"


# ---------------------------------------------------------------------------
# CS 3303 — Binary Search Tree: average O(log n) search
# ---------------------------------------------------------------------------
class _BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = _BSTNode(key)
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = _BSTNode(key)
                    return
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = _BSTNode(key)
                    return
                cur = cur.right
            else:
                return  # duplicate ignored

    def search(self, key):
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def inorder(self):
        out = []
        stack, cur = [], self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    def height(self):
        def _h(n):
            if n is None:
                return 0
            return 1 + max(_h(n.left), _h(n.right))
        return _h(self.root)


# ---------------------------------------------------------------------------
# CS 3303 — Hash Table: O(1) average lookup (Guardian-style blocklist)
# Separate chaining with Python dicts as buckets.
# ---------------------------------------------------------------------------
class HashTable:
    def __init__(self, capacity=16):
        self._cap = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        # Deterministic string hash compatible across runs
        h = 5381
        for ch in str(key):
            h = ((h << 5) + h) + ord(ch)
        return h % self._cap

    def put(self, key, value):
        b = self._buckets[self._hash(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)
                return
        b.append((key, value))
        self._size += 1
        if self._size > self._cap * 0.75:
            self._resize()

    def get(self, key):
        for k, v in self._buckets[self._hash(key)]:
            if k == key:
                return v
        return None

    def delete(self, key):
        b = self._buckets[self._hash(key)]
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                self._size -= 1
                return True
        return False

    def _resize(self):
        old = self._buckets
        self._cap *= 2
        self._buckets = [[] for _ in range(self._cap)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)

    def __len__(self):
        return self._size


# ---------------------------------------------------------------------------
# CS 3303 — Graph: adjacency list, BFS vs DFS
# ---------------------------------------------------------------------------
class Graph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, [])
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start):
        if start not in self.adj:
            return []
        visited, order, q = {start}, [], deque([start])
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    def dfs(self, start):
        if start not in self.adj:
            return []
        visited, order = set(), []

        def _visit(u):
            visited.add(u)
            order.append(u)
            for v in self.adj[u]:
                if v not in visited:
                    _visit(v)

        _visit(start)
        return order


# ---------------------------------------------------------------------------
# CS 3304 — Sorting: Bubble O(n^2) vs Quick O(n log n) average
# ---------------------------------------------------------------------------
def bubble_sort(arr):
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def quick_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------
def _pause():
    input("\nPress Enter to continue...")


def _print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def menu_stack():
    _print_header("Stack (LIFO) — Undo / Back button")
    s = Stack()
    while True:
        print(f"\nCurrent: {s}")
        print(" 1) push   2) pop   3) peek   4) back")
        choice = input("> ").strip()
        if choice == "1":
            s.push(input("Value to push: "))
        elif choice == "2":
            try:
                print(f"Popped: {s.pop()}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                print(f"Top: {s.peek()}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == "4":
            return


def menu_queue():
    _print_header("Queue (FIFO) — Printer queue")
    q = Queue()
    while True:
        print(f"\nCurrent: {q}")
        print(" 1) enqueue   2) dequeue   3) front   4) back")
        choice = input("> ").strip()
        if choice == "1":
            q.enqueue(input("Job name: "))
        elif choice == "2":
            try:
                print(f"Dequeued: {q.dequeue()}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                print(f"Front: {q.front()}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == "4":
            return


def menu_linked_list():
    _print_header("Linked List — O(1) insert/delete at head")
    ll = LinkedList()
    while True:
        print(f"\nCurrent: {ll.to_list()}  (size={len(ll)})")
        print(" 1) insert head  2) insert tail  3) delete head  4) search  5) back")
        choice = input("> ").strip()
        if choice == "1":
            ll.insert_head(input("Value: "))
        elif choice == "2":
            ll.insert_tail(input("Value: "))
        elif choice == "3":
            try:
                print(f"Deleted: {ll.delete_head()}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == "4":
            val = input("Value to find: ")
            idx = ll.search(val)
            print(f"Found at index {idx}" if idx >= 0 else "Not found")
        elif choice == "5":
            return


def menu_bst():
    _print_header("Binary Search Tree — O(log n) search (average)")
    tree = BST()
    while True:
        print(f"\nIn-order: {tree.inorder()}  height={tree.height()}")
        print(" 1) insert  2) search  3) back")
        choice = input("> ").strip()
        if choice == "1":
            try:
                tree.insert(int(input("Integer key: ")))
            except ValueError:
                print("Please enter an integer.")
        elif choice == "2":
            try:
                k = int(input("Search key: "))
                print("Found" if tree.search(k) else "Not found")
            except ValueError:
                print("Please enter an integer.")
        elif choice == "3":
            return


def menu_hash_table():
    _print_header("Hash Table — O(1) average lookup (blocklist demo)")
    ht = HashTable()
    while True:
        print(f"\nSize: {len(ht)}")
        print(" 1) put  2) get  3) delete  4) back")
        choice = input("> ").strip()
        if choice == "1":
            ht.put(input("Key: "), input("Value: "))
        elif choice == "2":
            k = input("Key: ")
            v = ht.get(k)
            print(f"{k} -> {v}" if v is not None else f"{k} not in table")
        elif choice == "3":
            print("Deleted" if ht.delete(input("Key: ")) else "Key not found")
        elif choice == "4":
            return


def menu_graph():
    _print_header("Graph — BFS vs DFS")
    print("Building demo graph:  A-B, A-C, B-D, C-E, D-E")
    g = Graph()
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E")]:
        g.add_edge(u, v)
    while True:
        start = input("\nStart node (or 'q' to go back): ").strip()
        if start.lower() == "q":
            return
        print(f"BFS from {start}: {g.bfs(start)}")
        print(f"DFS from {start}: {g.dfs(start)}")


def menu_sorting():
    _print_header("Sorting — Bubble O(n^2) vs Quick O(n log n)")
    while True:
        print("\n 1) Sort small custom list  2) Benchmark both  3) back")
        choice = input("> ").strip()
        if choice == "1":
            raw = input("Numbers (comma-separated): ")
            try:
                nums = [int(x) for x in raw.split(",") if x.strip()]
            except ValueError:
                print("Invalid input.")
                continue
            print(f"Bubble: {bubble_sort(nums)}")
            print(f"Quick : {quick_sort(nums)}")
        elif choice == "2":
            size = input("List size (e.g. 500): ").strip()
            try:
                n = int(size)
            except ValueError:
                print("Invalid size.")
                continue
            data = [random.randint(1, 100_000) for _ in range(n)]
            t0 = time.perf_counter()
            bubble_sort(data)
            t1 = time.perf_counter()
            quick_sort(data)
            t2 = time.perf_counter()
            print(f"Bubble sort: {t1 - t0:.4f} s")
            print(f"Quick  sort: {t2 - t1:.4f} s")
        elif choice == "3":
            return


MAIN_MENU = """
┌──────────────────────────────────────────────────────────┐
│  UoPeople CS Lab CLI                                     │
├──────────────────────────────────────────────────────────┤
│  1) Stack        (CS 3303 — LIFO / Undo)                 │
│  2) Queue        (CS 3303 — FIFO / Printer)              │
│  3) Linked List  (CS 3303 — O(1) head ops)               │
│  4) BST          (CS 3303 — O(log n) search)             │
│  5) Hash Table   (CS 3303 — O(1) lookup)                 │
│  6) Graph        (CS 3303 — BFS vs DFS)                  │
│  7) Sorting      (CS 3304 — Bubble vs Quick)             │
│  0) Exit                                                 │
└──────────────────────────────────────────────────────────┘
"""

HANDLERS = {
    "1": menu_stack,
    "2": menu_queue,
    "3": menu_linked_list,
    "4": menu_bst,
    "5": menu_hash_table,
    "6": menu_graph,
    "7": menu_sorting,
}


def main():
    while True:
        print(MAIN_MENU)
        choice = input("Select: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        handler = HANDLERS.get(choice)
        if handler:
            handler()
            _pause()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted.")
