from typing import List

# =============================================================================
# SECTION 1 — TRIE (PREFIX TREE) VIA NESTED DICTIONARIES
# =============================================================================
#
# Python doesn't have a built-in Trie structure, but its native `dict` is 
# incredibly efficient and syntactically clean for building one.
# A Trie is implemented as a set of nested dictionaries. 
# We use a special character (like '#') to mark the end of a valid word.

trie = {}

# 1. Insertion
# To insert "apple", we traverse/create dictionaries character by character.
word = "apple"
node = trie
for char in word:
    if char not in node:
        node[char] = {}
    node = node[char]
node['#'] = True  # Mark end of the word

# trie now looks like: {'a': {'p': {'p': {'l': {'e': {'#': True}}}}}}

# Quick Insert Function Example
def insert(t, w):
    curr = t
    for ch in w:
        if ch not in curr:
            curr[ch] = {}
        curr = curr[ch]
    curr['#'] = True

insert(trie, "app")
# trie now: {'a': {'p': {'p': {'l': {'e': {'#': True}}, '#': True}}}}

# 2. Search (Exact Word)
# To check if "app" exists, we traverse and check if the '#' key exists at the end.
def search(t, w):
    curr = t
    for ch in w:
        if ch not in curr:
            return False
        curr = curr[ch]
    return '#' in curr

print("Search 'app':", search(trie, "app"))    # True
print("Search 'appl':", search(trie, "appl"))  # False

# 3. StartsWith (Prefix Search)
# To check if a prefix exists, we just traverse the characters.
def starts_with(t, prefix):
    curr = t
    for ch in prefix:
        if ch not in curr:
            return False
        curr = curr[ch]
    return True

print("StartsWith 'appl':", starts_with(trie, "appl")) # True


# =============================================================================
# SECTION 2 — QUICK REFERENCE TABLE
# =============================================================================
#
#  Operation                       | Typical Implementation                   | O(?)
#  --------------------------------|------------------------------------------|-------
#  Insert Word                     | Loop chars: node = node.setdefault(c, {})| O(L)
#  Search Exact Word               | Loop chars; check '#' at end node        | O(L)
#  Search Prefix (StartsWith)      | Loop chars; check node exists            | O(L)
#  Space Complexity                | Varies by overlap                        | O(N*L)
#
#  * L = length of word, N = number of words


# =============================================================================
# SECTION 3 — DSA PROBLEM: Stream of Characters (LeetCode #1032)
# =============================================================================
#
# PROBLEM:
#   Design an algorithm that accepts a stream of characters and checks if a 
#   suffix of these characters is a string of a given array of words `words`.
#
# WHY NESTED DICTIONARIES (TRIE)?
#   Checking all possible suffixes against a list of words for every new character 
#   is too slow. Instead, if we insert all words into a Trie IN REVERSE, we can
#   just traverse our recent stream characters backwards on each query. 
#   Nested dictionaries make jumping from node to node O(1), making Python perfect for this.
#

class StreamChecker:

    def __init__(self, words: List[str]):
        self.stream = []
        self.trie = {}
        # Pre-process words by generating a reverse Trie
        for word in words:
            node = self.trie
            for char in reversed(word):
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['#'] = True

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        node = self.trie
        # Traverse the list of previously seen characters in reverse
        for i in range(len(self.stream)-1, -1, -1):
            c = self.stream[i]
            if c in node:
                node = node[c]
                if '#' in node:             # We found a complete reversed word
                    return True
            else:
                break                       # Path died, no matching suffix
        return False


# Your StreamChecker object will be instantiated and called as such:
# obj = StreamChecker(words)
# param_1 = obj.query(letter)

if __name__ == "__main__":
    streamChecker = StreamChecker(["cd", "f", "kl"])
    print("query('a') ->", streamChecker.query('a')) # False
    print("query('b') ->", streamChecker.query('b')) # False
    print("query('c') ->", streamChecker.query('c')) # False
    print("query('d') ->", streamChecker.query('d')) # True, because 'cd' is in words
    print("query('e') ->", streamChecker.query('e')) # False
    print("query('f') ->", streamChecker.query('f')) # True, because 'f' is in words
    print("query('g') ->", streamChecker.query('g')) # False
    print("query('h') ->", streamChecker.query('h')) # False
    print("query('i') ->", streamChecker.query('i')) # False
    print("query('j') ->", streamChecker.query('j')) # False
    print("query('k') ->", streamChecker.query('k')) # False
    print("query('l') ->", streamChecker.query('l')) # True, because 'kl' is in words
