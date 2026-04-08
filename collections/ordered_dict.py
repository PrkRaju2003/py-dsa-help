from collections import OrderedDict
od = OrderedDict()

od["a"] = 1 # new keys go to the END
od["b"] = 2       
od["c"] = 3       
od["a"] = 99 #{ a:99, b:2, c:3 }update keeps original position

val = od["b"] #KeyError if missing
val = od.get("z", -1) # -1 safe access with default

exists = "b" in od # True
missing = "z" in od # False

# move_to_end(key, last=True)
# Moves an existing key to the FRONT or BACK in O(1).
od.move_to_end("a", last=True)   # { b:2, c:3, a:99 }  — moved to END (default)
od.move_to_end("a", last=False)  # { a:99, b:2, c:3 }  — moved to FRONT

# Removes and returns the LAST or FIRST item as a (key, value) tuple.
item = od.popitem(last=True)     # ('c', 3) — removes from END   → { a:99, b:2 }
item = od.popitem(last=False)    # ('a', 99) — removes from FRONT → { b:2 }

od["x"] = 10
val = od.pop("x") # 10 — removes key, returns value
val = od.pop("z", None) # None — safe pop with default

od["d"] = 4
del od["d"] # Removes key; KeyError if missing

# Iteration (always in insertion order)
od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])

keys   = list(od.keys())    # ['a', 'b', 'c']
values = list(od.values())  # [1, 2, 3]
pairs  = list(od.items())   # [('a',1), ('b',2), ('c',3)]

for k, v in od.items():
    pass                    # iterates front → back

for k in reversed(od):
    pass                    # iterates back → front  (O(1) iterator)

size = len(od) 

od.update({"d": 4, "e": 5}) # appends new keys to the end

# Two OrderedDicts are equal only if items match AND order matches.
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
od1 == od2 # False — order differs!

od1 == {"b": 2, "a": 1} # True

od.clear() # Removes all items


# =============================================================================
# SECTION 2 — QUICK REFERENCE TABLE
# =============================================================================
#
#  Operation                         | Description                   | O(?)
#  ----------------------------------|-------------------------------|-------
#  od[key] = value                   | Insert / update               | O(1)
#  od[key]                           | Access                        | O(1)
#  od.get(key, default)              | Safe access                   | O(1)
#  key in od                         | Membership check              | O(1)
#  del od[key]                       | Delete                        | O(1)
#  od.pop(key, default)              | Remove + return value         | O(1)
#  od.move_to_end(key, last=T/F)     | Reorder to front or back      | O(1)
#  od.popitem(last=T/F)              | Remove from front or back     | O(1)
#  od.keys() / .values() / .items()  | Ordered views                 | O(1)
#  list(od)                          | Keys as a list                | O(n)
#  len(od)                           | Count of pairs                | O(1)
#  od.update(other)                  | Merge dict into od            | O(k)
#  od.clear()                        | Remove all                    | O(1)
#  od == other_od                    | Order-sensitive equality      | O(n)
#  reversed(od)                      | Reverse-order iterator        | O(1)
#


# =============================================================================
# SECTION 3 — DSA PROBLEM: LRU Cache  (LeetCode #146)
# =============================================================================
#
# PROBLEM:
#   Design a cache with a fixed capacity. When full, evict the
#   Least Recently Used item before inserting a new one.
#   Both get() and put() count as "using" an item.
#
# WHY OrderedDict?
#   We need three things simultaneously:
#     1. O(1) lookup            → dict
#     2. O(1) recency update    → move_to_end
#     3. O(1) LRU eviction      → popitem(last=False)
#
# ORDERING CONVENTION used here:
#   FRONT of dict = Least Recently Used  (evicted first)
#   END   of dict = Most Recently Used   (kept longest)
#
# TRACE EXAMPLE (capacity = 2):
#   put(1,1) → { 1:1 }
#   put(2,2) → { 1:1, 2:2 }
#   get(1)   → move 1 to end → { 2:2, 1:1 }
#   put(3,3) → capacity exceeded, evict FRONT (key 2) → { 1:1, 3:3 }
#   get(2)   → -1  (was evicted)

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.lru = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.lru:
            return -1
        # Accessing a key makes it most recently used → move to end
        self.lru.move_to_end(key, last=True)
        return self.lru[key]

    def put(self, key: int, value: int) -> None:
        if key in self.lru:
            # Key already exists → refresh its recency before updating
            self.lru.move_to_end(key)
        self.lru[key] = value
        if len(self.lru) > self.cap:
            # Evict the LRU item (always at the FRONT)
            self.lru.popitem(last=False)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))      # 1   — key 1 found, moved to end
    cache.put(3, 3)          # evicts key 2 (LRU)
    print(cache.get(2))      # -1  — key 2 was evicted
    cache.put(4, 4)          # evicts key 1 (LRU now)
    print(cache.get(1))      # -1  — key 1 was evicted
    print(cache.get(3))      # 3
    print(cache.get(4))      # 4
