"""Hypothetical campus map: (location_a, location_b, distance_in_meters)."""

EDGES = [
    ("Main Gate", "First Year Block", 200), ("Main Gate", "Central Ground", 200),
    ("Main Gate", "Security Office", 60),
    ("First Year Block", "IT Department", 100), ("First Year Block", "Admin Block", 150),
    ("Central Ground", "Hostel", 150), ("Central Ground", "Admin Block", 180),
    ("IT Department", "AI & DS Department", 100), ("IT Department", "Library", 180),
    ("AI & DS Department", "Mechanical Department", 60),
    ("AI & DS Department", "E&TC Department", 50),
    ("Mechanical Department", "Canteen", 70), ("E&TC Department", "Canteen", 40),
    ("E&TC Department", "Library", 100), ("Canteen", "Library", 80),
    ("Library", "Admin Block", 120), ("Library", "Medical Center", 90),
    ("Canteen", "Medical Center", 110), ("Hostel", "Medical Center", 200),
    ("Admin Block", "Fire Station", 100), ("Hostel", "Fire Station", 130),
]

# emergency type -> (responder location, vehicle, speed in m/s)
RESPONDERS = {
    "Medical":  ("Medical Center", "Ambulance", 8),
    "Fire":     ("Fire Station", "Fire Truck", 6),
    "Security": ("Security Office", "Security Patrol", 4),
}
