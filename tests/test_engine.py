import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from campus_data import EDGES, RESPONDERS
from engine import alternative_routes, build_graph, dispatch, shortest_route

G = build_graph(EDGES)


class TestEngine(unittest.TestCase):
    def test_shortest_route(self):
        d, p = shortest_route(G, "Medical Center", "IT Department")
        self.assertEqual(d, 270)
        self.assertEqual(p[0], "Medical Center")

    def test_blocked_road_reroutes(self):
        blocked = frozenset({frozenset(("Library", "Medical Center"))})
        d, p = shortest_route(G, "Medical Center", "IT Department", blocked)
        self.assertGreater(d, 270)
        self.assertNotIn(("Library", "Medical Center"), list(zip(p, p[1:])))

    def test_unreachable(self):
        blocked = frozenset(frozenset((a, b)) for a, b, _ in EDGES if "Security Office" in (a, b))
        self.assertIsNone(shortest_route(G, "Main Gate", "Security Office", blocked))

    def test_dispatch_eta(self):
        r = dispatch(G, "Medical", "IT Department", RESPONDERS)
        self.assertEqual(r["distance"], 270)
        self.assertEqual(r["eta_seconds"], round(270 / 8))

    def test_alternatives_sorted_unique(self):
        alts = alternative_routes(G, "Medical Center", "IT Department", k=3)
        dists = [d for d, _ in alts]
        self.assertEqual(dists, sorted(dists))
        self.assertEqual(len({tuple(p) for _, p in alts}), len(alts))


if __name__ == "__main__":
    unittest.main()
