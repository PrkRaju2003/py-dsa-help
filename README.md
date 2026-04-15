# py-dsa-help

> Underrated Python standard library tools that make DSA problems cleaner and faster.

Most DSA resources skip Python's built-ins entirely. This repo shows you the right tool for the right problem — with real implementations and inline explanations.

---

## 📁 Structure

```
py-dsa-help/
├── collections/
│   └── ordered_dict.py     # OrderedDict — all operations + LRU Cache
├── heapq/
│   └── heap.py             # heapq — min/max heap operations + Kth Largest
```

---

## Libraries

### `collections` module

| Tool          | File                                                           | Problem Solved            |
| ------------- | -------------------------------------------------------------- | ------------------------- |
| `OrderedDict` | [`collections/ordered_dict.py`](./collections/ordered_dict.py) | LRU Cache (LeetCode #146) |
| `heapq`       | [`heapq/heap.py`](./heapq/heap.py)                             | Kth Largest (LeetCode #703)|

---

## Roadmap

Libraries planned for future additions:

| Module        | Tool          | Use Case                          |
| ------------- | ------------- | --------------------------------- |
| `collections` | `Counter`     | Frequency maps, anagram detection |
| `collections` | `deque`       | Sliding window, monotonic queue   |
| `collections` | `defaultdict` | Graph adjacency, grouping         |
| `bisect`      | —             | Binary search on sorted lists     |
| `functools`   | `lru_cache`   | Memoization / DP                  |

---

## Contributing

Each addition should follow the same pattern as existing files:

1. Create `module_name/tool_name.py`
2. Section 1 — all operations with inline examples and time complexity table
3. Section 2 — at least one real DSA problem with a trace walkthrough
4. Add a row to the Libraries table above

---

## License

[Apache 2.0](./LICENSE)
