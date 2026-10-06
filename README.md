# Smart Campus Emergency Response System

A decision-support tool that dispatches the right responder (ambulance, fire truck, security patrol) to an incident on a campus using **Dijkstra's shortest path algorithm**, with blocked-road handling, ETA estimation and alternative routes.

## Problem
In an emergency, every second counts. Staff need the fastest valid route from the responder's base to the incident, even when roads are blocked.

## Model
- **Vertex** = campus location (including Medical Center, Fire Station, Security Office)
- **Edge** = road with weight = distance in metres (undirected)
- **Blocked road** = edge ignored during Dijkstra
- **ETA** = distance / vehicle speed (Ambulance 8 m/s, Fire Truck 6 m/s, Security Patrol 4 m/s)

## Features
- Emergency dispatch: Medical, Fire, Security
- Shortest route between any two locations
- Block / unblock roads at runtime
- Alternative routes (re-run Dijkstra with each road of the best route blocked)
- Graph export to Graphviz `.dot` (route in red, blocked roads dashed)

## Complexity
- Dijkstra: O((V + E) log V) time, O(V + E) space
- Alternative routes: O(L (V + E) log V), L = roads on the best route

## Run
```bash
python main.py            # interactive menu
python main.py --demo     # scripted scenarios
python -m unittest discover tests
dot -Tpng campus.dot -o campus.png   # optional, needs Graphviz
```

## Structure
```
main.py          menu / CLI
engine.py        Dijkstra, dispatch, alternatives, DOT export
campus_data.py   campus map + responders
tests/test_engine.py
```

## Future Scope
- Real campus coordinates and an interactive map (matplotlib / web)
- Traffic-dependent edge weights, multiple simultaneous incidents
- A* comparison, GUI, live alerts
