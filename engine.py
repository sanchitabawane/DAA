"""Core algorithms: Dijkstra with blocked roads, dispatch, alternative routes."""
import heapq


def build_graph(edges):
    graph = {}
    for a, b, w in edges:
        graph.setdefault(a, {})[b] = w
        graph.setdefault(b, {})[a] = w
    return graph


def dijkstra(graph, start, blocked=frozenset()):
    """Shortest distances from start, skipping blocked roads. O((V+E) log V)."""
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u].items():
            if frozenset((u, v)) in blocked:
                continue
            if d + w < dist[v]:
                dist[v], prev[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    return dist, prev


def build_path(prev, dest):
    path = []
    while dest is not None:
        path.append(dest)
        dest = prev[dest]
    return path[::-1]


def shortest_route(graph, src, dst, blocked=frozenset()):
    """Returns (distance, path) or None if unreachable."""
    dist, prev = dijkstra(graph, src, blocked)
    if dist[dst] == float("inf"):
        return None
    return dist[dst], build_path(prev, dst)


def alternative_routes(graph, src, dst, blocked=frozenset(), k=3):
    """Best route plus alternatives: block each road of the best route in turn."""
    best = shortest_route(graph, src, dst, blocked)
    if not best:
        return []
    routes, seen = [best], {tuple(best[1])}
    for edge in zip(best[1], best[1][1:]):
        r = shortest_route(graph, src, dst, blocked | {frozenset(edge)})
        if r and tuple(r[1]) not in seen:
            seen.add(tuple(r[1]))
            routes.append(r)
    return sorted(routes, key=lambda r: r[0])[:k]


def dispatch(graph, emergency_type, incident, responders, blocked=frozenset()):
    """Send the responder to the incident. Returns dict or None."""
    base, vehicle, speed = responders[emergency_type]
    route = shortest_route(graph, base, incident, blocked)
    if not route:
        return None
    dist, path = route
    return {"vehicle": vehicle, "base": base, "distance": dist,
            "path": path, "eta_seconds": round(dist / speed)}


def export_dot(graph, path=(), blocked=frozenset(), filename="campus.dot"):
    """Graphviz DOT file. Route = red, blocked roads = dashed grey."""
    on_path = {frozenset(e) for e in zip(path, path[1:])}
    lines = ["graph Campus {", "  node [shape=box, style=rounded];"]
    done = set()
    for u in graph:
        for v, w in graph[u].items():
            key = frozenset((u, v))
            if key in done:
                continue
            done.add(key)
            style = f'label="{w} m"'
            if key in blocked:
                style += ', style=dashed, color=grey'
            elif key in on_path:
                style += ', color=red, penwidth=3'
            lines.append(f'  "{u}" -- "{v}" [{style}];')
    lines.append("}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename
