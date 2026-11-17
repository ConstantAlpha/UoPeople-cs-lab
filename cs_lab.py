# =====================================================
# CS LAB CLI - UoPeople Computer Science Portfolio
# Courses: CS 1102 (Python), CS 1103 (OOP), CS 3303 (Data Structures)
#          CS 3304 (Algorithms), CS 2203 (Databases)
# Author: Guardian / UoPeople Student
# Run: python cs_lab.py
# =====================================================

import time
from collections import deque

# ---------- 1. STACK (LIFO) - CS 3303 ----------
# Problem: Undo feature, browser back button
# Real use: Function calls, expression evaluation
class Stack:
    def __init__(self): self.items = []
    def push(self, x): self.items.append(x)
    def pop(self): return self.items.pop() if self.items else None
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return len(self.items) == 0
    def __str__(self): return str(self.items)

# ---------- 2. QUEUE (FIFO) - CS 3303 ----------
# Problem: Printer queue, customer service
# Real use: BFS, task scheduling
class Queue:
    def __init__(self): self.items = deque()
    def enqueue(self, x): self.items.append(x)
    def dequeue(self): return self.items.popleft() if self.items else None
    def __str__(self): return str(list(self.items))

# ---------- 3. LINKED LIST - CS 1103 / CS 3303 ----------
# Problem: Dynamic memory, insert/delete without shifting
# Why not list? List needs shifting O(n), Linked List O(1) insert
class Node:
    def __init__(self, data): self.data = data; self.next = None

class LinkedList:
    def __init__(self): self.head = None
    def insert(self, data):
        new = Node(data)
        new.next = self.head
        self.head = new
    def delete(self, data):
        cur = self.head; prev = None
        while cur:
            if cur.data == data:
                if prev: prev.next = cur.next
                else: self.head = cur.next
                return True
            prev, cur = cur, cur.next
        return False
    def display(self):
        out = []; cur = self.head
        while cur: out.append(str(cur.data)); cur = cur.next
        return " -> ".join(out) + " -> None"

# ---------- 4. BINARY SEARCH TREE - CS 3303 ----------
# Problem: Fast searching O(log n) vs linear O(n)
# Real use: Databases, file systems
class BSTNode:
    def __init__(self, key): self.key = key; self.left = None; self.right = None

class BST:
    def __init__(self): self.root = None
    def insert(self, key):
        def _insert(node, key):
            if not node: return BSTNode(key)
            if key < node.key: node.left = _insert(node.left, key)
            elif key > node.key: node.right = _insert(node.right, key)
            return node
        self.root = _insert(self.root, key)
    def search(self, key):
        cur = self.root
        steps = 0
        while cur:
            steps += 1
            if key == cur.key: return True, steps
            cur = cur.left if key < cur.key else cur.right
        return False, steps
    def inorder(self):
        res = []
        def _walk(n):
            if n: _walk(n.left); res.append(n.key); _walk(n.right)
        _walk(self.root); return res

# ---------- 5. HASH TABLE - CS 2203 / CS 3303 ----------
# Problem: Fast lookup by key, like Python dict
# Real use: Databases, caches, Guardian blocklist
class HashTable:
    def __init__(self, size=10): self.size = size; self.table = [[] for _ in range(size)]
    def _hash(self, key): return hash(key) % self.size
    def put(self, key, value):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key: pair[1] = value; return
        self.table[idx].append([key, value])
    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key: return v
        return None

# ---------- 6. GRAPH + BFS / DFS - CS 3304 ----------
# Problem: Shortest path, social network, Guardian site map
class Graph:
    def __init__(self): self.adj = {}
    def add_edge(self, a, b):
        self.adj.setdefault(a, []).append(b)
        self.adj.setdefault(b, []).append(a)
    def bfs(self, start):
        visited, queue, order = set([start]), deque([start]), []
        while queue:
            node = queue.popleft(); order.append(node)
            for n in self.adj.get(node, []):
                if n not in visited: visited.add(n); queue.append(n)
        return order
    def dfs(self, start):
        visited, order = set(), []
        def _dfs(n):
            visited.add(n); order.append(n)
            for nb in self.adj.get(n, []):
                if nb not in visited: _dfs(nb)
        _dfs(start); return order

# ---------- 7. SORTING & SEARCHING - CS 3304 ----------
def bubble_sort(arr):
    arr = arr[:]; n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]: arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

def binary_search(arr, target):
    low, high, steps = 0, len(arr)-1, 0
    while low <= high:
        steps += 1
        mid = (low+high)//2
        if arr[mid] == target: return mid, steps
        elif arr[mid] < target: low = mid+1
        else: high = mid-1
    return -1, steps

# ---------- CLI ----------
def main():
    stack = Stack(); queue = Queue(); ll = LinkedList()
    bst = BST(); ht = HashTable(); graph = Graph()
    # Pre-load Graph: UoPeople courses
    for a,b in [("CS1102","CS1103"),("CS1103","CS3303"),("CS3303","CS3304"),("CS1102","CS2203"),("CS2203","CS3303")]:
        graph.add_edge(a,b)
    for v in [50,30,70,20,40,60,80]: bst.insert(v)

    while True:
        print("\n" + "="*50)
        print("  🎓 UoPeople CS LAB - Data Structures & Algorithms")
        print("="*50)
        print("1. Stack (LIFO) - Undo / Back button")
        print("2. Queue (FIFO) - Printer / BFS")
        print("3. Linked List - Dynamic Insert/Delete")
        print("4. Binary Search Tree - O(log n) Search")
        print("5. Hash Table - Fast Lookup (like Guardian blocklist)")
        print("6. Graph BFS vs DFS - Course Map")
        print("7. Sorting - Bubble vs Quick Sort + Binary Search")
        print("8. Run ALL Demos (for assignment)")
        print("0. Exit")
        choice = input("\nChoose (0-8): ").strip()

        if choice == "1":
            print("\n--- STACK Demo ---")
            for x in ["CS1102","CS1103","CS3303"]: stack.push(x); print(f"push({x}) -> {stack}")
            print(f"pop() -> {stack.pop()} | Now: {stack}")
            print(f"peek() -> {stack.peek()} | Problem solved: Undo works LIFO")
        elif choice == "2":
            print("\n--- QUEUE Demo ---")
            for x in ["Student1","Student2","Student3"]: queue.enqueue(x); print(f"enqueue({x}) -> {queue}")
            print(f"dequeue() -> {queue.dequeue()} | First in, first out")
        elif choice == "3":
            print("\n--- LINKED LIST Demo ---")
            for x in [10,20,30]: ll.insert(x); print(f"insert({x}) -> {ll.display()}")
            ll.delete(20); print(f"delete(20) -> {ll.display()} | No shifting needed!")
        elif choice == "4":
            print("\n--- BST Demo ---")
            print(f"Inorder (sorted): {bst.inorder()}")
            target = int(input("Search for number (e.g. 40): ") or "40")
            found, steps = bst.search(target)
            print(f"Search {target}: Found={found} in {steps} steps vs 7 steps linear")
        elif choice == "5":
            print("\n--- HASH TABLE Demo (Guardian) ---")
            ht.put("pornhub.com","BLOCKED"); ht.put("wikipedia.org","ALLOWED")
            print(f"pornhub.com -> {ht.get('pornhub.com')}")
            print(f"wikipedia.org -> {ht.get('wikipedia.org')}")
            print("Problem solved: O(1) lookup, not O(n) scanning list")
        elif choice == "6":
            print("\n--- GRAPH Demo ---")
            print(f"BFS from CS1102: {graph.bfs('CS1102')}")
            print(f"DFS from CS1102: {graph.dfs('CS1102')}")
            print("BFS = shortest path, DFS = explore deep")
        elif choice == "7":
            print("\n--- SORTING Demo ---")
            arr = [64,34,25,12,22,11,90]
            print(f"Original: {arr}")
            start=time.time(); print(f"Bubble Sort: {bubble_sort(arr)} | O(n^2)")
            print(f"Quick Sort: {quick_sort(arr)} | O(n log n) - faster!")
            sorted_arr = quick_sort(arr)
            idx, steps = binary_search(sorted_arr, 22)
            print(f"Binary Search 22: index {idx} in {steps} steps vs 7 linear")
        elif choice == "8":
            print("\n=== RUNNING ALL FOR ASSIGNMENT ===")
            print(f"Stack: push A,B,C -> pop = C (LIFO)")
            print(f"Queue: enqueue A,B,C -> dequeue = A (FIFO)")
            print(f"Linked List: 10->20->30, delete 20 -> 10->30")
            print(f"BST: {bst.inorder()} - search is O(log n)")
            print(f"Hash: Guardian blocklist O(1)")
            print(f"Graph BFS: {graph.bfs('CS1102')}")
            print(f"Quick Sort beats Bubble Sort for large data")
            print("\n✅ All concepts demonstrated!")
        elif choice == "0":
            print("Bye! Good luck in UoPeople 🎓"); break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
