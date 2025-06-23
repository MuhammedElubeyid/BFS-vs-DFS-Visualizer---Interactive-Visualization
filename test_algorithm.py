import unittest
from algorithm import bfs, dfs

class TestTraversal(unittest.TestCase):
    def setUp(self):
        self.graph = {"A":["B","C"],"B":["D","E"],"C":["F","G"],"D":[],"E":[],"F":[],"G":[]}
    def test_bfs_full(self):
        self.assertEqual(set(bfs(self.graph, "A")[-1]), set(list("ABCDEFG")))
    def test_dfs_full(self):
        self.assertEqual(set(dfs(self.graph, "A")[-1]), set(list("ABCDEFG")))
    def test_invalid(self):
        self.assertEqual(bfs(self.graph, "Z"), [])
        self.assertEqual(dfs(self.graph, "Z"), [])
if __name__ == '__main__':
    unittest.main()