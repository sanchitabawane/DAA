"""Smart Campus Emergency Response System. Run: python main.py  (or --demo)"""
import sys

from campus_data import EDGES, RESPONDERS
from engine import (alternative_routes, build_graph, dispatch, export_dot,
                    shortest_route)

graph = build_graph(EDGES)
locations = sorted(graph)
blocked = set()


def pick(prompt, options):
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    try:
        n = int(input(prompt))
        if 1 <= n <= len(options):
            return options[n - 1]
    except ValueError:
        pass
    print("Invalid choice.")
    return None


def fmt_time(sec):
    return f"{sec // 60} min {sec % 60} s"


def show_dispatch(kind, incident):
    res = dispatch(graph, kind, incident, RESPONDERS, frozenset(blocked))
    if not res:
        print("\n!! No route available - all roads to the incident are blocked.")
        return
    print(f"\n=== {kind.upper()} EMERGENCY at {incident} ===")
    print(f"Dispatch : {res['vehicle']} from {res['base']}")
    print("Route    :", " -> ".join(res["path"]))
    print(f"Distance : {res['distance']} m   ETA: {fmt_time(res['eta_seconds'])}")
    alts = alternative_routes(graph, res["base"], incident, frozenset(blocked))
    if len(alts) > 1:
        print("Alternatives:")
        for d, p in alts[1:]:
            print(f"  {d} m: {' -> '.join(p)}")
    export_dot(graph, res["path"], frozenset(blocked))
    print("(Route saved to campus.dot - open with Graphviz to visualize)")


def report_emergency():
    kind = pick("Emergency type: ", list(RESPONDERS))
    if kind:
        place = pick("Incident location: ", locations)
        if place:
            show_dispatch(kind, place)


def route_between():
    a = pick("Source: ", locations)
    b = a and pick("Destination: ", locations)
    if a and b and a != b:
        r = shortest_route(graph, a, b, frozenset(blocked))
        print("\nNo route." if not r else f"\n{' -> '.join(r[1])}\nDistance: {r[0]} m")


def toggle_block():
    a = pick("Road start: ", locations)
    if not a:
        return
    b = pick("Road end: ", sorted(graph[a]))
    if b:
        e = frozenset((a, b))
        blocked.symmetric_difference_update({e})
        print(f"\nRoad {a} <-> {b} is now {'BLOCKED' if e in blocked else 'OPEN'}.")


def show_blocked():
    print("\nBlocked roads:" if blocked else "\nNo blocked roads.")
    for e in blocked:
        print("  ", " <-> ".join(sorted(e)))


COMPLEXITY = """
Dijkstra (heapq, adjacency list): O((V + E) log V) time, O(V + E) space.
Alternative routes: re-run Dijkstra once per road on the best route -> O(L (V + E) log V).
Requires non-negative weights (distances), which holds for campus roads.
"""


def demo():
    print("DEMO 1: Medical emergency at IT Department")
    show_dispatch("Medical", "IT Department")
    print("\nDEMO 2: Road Library <-> Medical Center is blocked")
    blocked.add(frozenset(("Library", "Medical Center")))
    show_dispatch("Medical", "IT Department")
    print("\nDEMO 3: Fire at Hostel")
    show_dispatch("Fire", "Hostel")


def main():
    if "--demo" in sys.argv:
        return demo()
    menu = {"1": report_emergency, "2": route_between, "3": toggle_block,
            "4": show_blocked, "5": lambda: print(COMPLEXITY)}
    while True:
        print("\n===== SMART CAMPUS EMERGENCY RESPONSE =====")
        print("1. Report emergency\n2. Shortest route\n3. Block/unblock road")
        print("4. Show blocked roads\n5. Algorithm complexity\n0. Exit")
        c = input("Choice: ").strip()
        if c == "0":
            break
        menu.get(c, lambda: print("Invalid choice."))()


if __name__ == "__main__":
    main()
