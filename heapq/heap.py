import heapq
from typing import List

# By default, Python's heapq creates a MIN-HEAP.
# A heap is a binary tree where every parent node has a value less than or equal to any of its children.
# The smallest element is always at the root: heap[0]

heap = []

# heapq.heappush(heap, item) pushes the value item onto the heap, maintaining the heap invariant.
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 7)
heapq.heappush(heap, 3)
# heap is now [1, 3, 7, 4], the smallest is heap[0] == 1

# heapq.heappop(heap)
# Pops and returns the smallest item from the heap, maintaining the heap invariant, if the heap is empty, IndexError is raised.
smallest = heapq.heappop(heap) # returns 1
# heap is now [3, 4, 7]

# heapq.heappushpop(heap, item)
# Pushes item on the heap, then pops and returns the smallest item. This is more efficient than a heappush() followed by a separate heappop().
item = heapq.heappushpop(heap, 2) # pushes 2, pops 2 (since 2 is smallest)
# heap is still [3, 4, 7]

# heapq.heapreplace(heap, item)
# Pops and returns the smallest item, and also pushes the new item. 
# The heap size doesn't change. Raises IndexError if empty.
# More efficient than heappop() followed by heappush().
old_min = heapq.heapreplace(heap, 8) # pops 3, pushes 8
# heap is now [4, 8, 7]

# heapq.heapify(x)
# Transforms list x into a heap, in-place, in linear time O(n).
nums = [9, 5, 2, 8, 6]
heapq.heapify(nums) 
# nums is now [2, 5, 9, 8, 6], smallest is at nums[0]

# MAX-HEAP workaround
# Since Python only has Min-Heap, to create a Max-Heap we typically invert the values:
# Multiply numbers by -1 when pushing, and multiply by -1 when popping.
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -10)
heapq.heappush(max_heap, -2)
largest = -heapq.heappop(max_heap) # returns 10

# Note on Custom Objects:
# You can store tuples in the heap, they are compared element by element.
# E.g. heapq.heappush(heap, (priority, task_name))

# =============================================================================
# ADDITIONAL FUNCTIONS: nlargest, nsmallest, merge
# =============================================================================

# heapq.nlargest(n, iterable, key=None)
# Returns a list with the n largest elements from the dataset defined by iterable.
# O(N log k) time complexity, where N is iterable length, k is n.
nums_list = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
top_3 = heapq.nlargest(3, nums_list) # [42, 37, 23]

# heapq.nsmallest(n, iterable, key=None)
# Returns a list with the n smallest elements from the dataset.
# Extremely useful for finding minimums without sorting the entire list O(N log N).
bottom_3 = heapq.nsmallest(3, nums_list) # [-4, 1, 2]

# Using key function with nlargest / nsmallest
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
]
cheap = heapq.nsmallest(2, portfolio, key=lambda s: s['price'])
# [{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}]

# heapq.merge(*iterables, key=None, reverse=False)
# Merge multiple sorted inputs into a single sorted output.
# Returns an iterator over the sorted values.
# O(N log k) where N is total elements, k is number of iterables.
list1 = [1, 3, 5, 7]
list2 = [2, 4, 6, 8]
merged = list(heapq.merge(list1, list2)) # [1, 2, 3, 4, 5, 6, 7, 8]


# =============================================================================
# SECTION 2 — QUICK REFERENCE TABLE
# =============================================================================
#
#  Operation                         | Description                   | O(?)
#  ----------------------------------|-------------------------------|-------
#  heapq.heappush(heap, item)        | Insert item into heap         | O(log n)
#  heapq.heappop(heap)               | Pop smallest item out of heap | O(log n)
#  heapq.heappushpop(heap, item)     | Push then pop smallest        | O(log n)
#  heapq.heapreplace(heap, item)     | Pop smallest then push        | O(log n)
#  heapq.heapify(x)                  | Transform list into heap      | O(n)
#  heap[0]                           | Access smallest item          | O(1)
#  heapq.nlargest(n, iterable)       | Return the n largest elements | O(N log k)
#  heapq.nsmallest(n, iterable)      | Return the n smallest elements| O(N log k)
#


# =============================================================================
# SECTION 3 — DSA PROBLEM: Kth Largest Element in a Stream (LeetCode #703)
# =============================================================================
#
# PROBLEM:
#   Design a class to find the kth largest element in a stream. 
#   Note that it is the kth largest element in the sorted order, not the kth distinct element.
#
# WHY heapq?
#   To get the kth largest element quickly, we can maintain a MIN-HEAP of exactly 
#   k elements.
#   - The heap will always contain the top k largest elements seen so far.
#   - Because it's a min-heap, the SMALLest element of these k (which is the kth largest overall)
#     will be at the root (heap[0]).
#   - If a new element comes in and is bigger than the root, it means the root
#     is no longer in the top k, so we push the new element and pop the root.
#
# TRACE EXAMPLE (k = 3, nums = [4, 5, 8, 2]):
#   add(4) -> [4]                  - length < k, push
#   add(5) -> [4, 5]               - length < k, push
#   add(8) -> [4, 5, 8]            - length < k, push, 3rd largest is 4
#   add(2) -> [4, 5, 8]            - 2 <= heap[0] (4), ignore, 3rd largest is 4
#   add(9) -> [5, 8, 9]            - 9 > heap[0] (4), push 9 & pop 4. 3rd largest is 5

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.heap = []
        self.k = k
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap,val)
        elif val > self.heap[0]:
            heapq.heappush(self.heap,val)
            heapq.heappop(self.heap)
        return self.heap[0]


# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)

if __name__ == "__main__":
    kthLargest = KthLargest(3, [4, 5, 8, 2])
    print(kthLargest.add(3))  # 4
    print(kthLargest.add(5))  # 5
    print(kthLargest.add(10)) # 5
    print(kthLargest.add(9))  # 8
    print(kthLargest.add(4))  # 8
