"""United States city coordinates used by Vigilantae's map views."""

US_CENTER = (39.8283, -98.5795)
US_ZOOM = 5

# Major U.S. cities and common input aliases. Add new cities here once and both
# dashboard maps gain support automatically.
CITY_COORDS = {
    "Atlanta": (33.7490, -84.3880),
    "Austin": (30.2672, -97.7431),
    "Baltimore": (39.2904, -76.6122),
    "Boston": (42.3601, -71.0589),
    "Charlotte": (35.2271, -80.8431),
    "Chicago": (41.8781, -87.6298),
    "Columbus": (39.9612, -82.9988),
    "Dallas": (32.7767, -96.7970),
    "Denver": (39.7392, -104.9903),
    "Detroit": (42.3314, -83.0458),
    "Houston": (29.7604, -95.3698),
    "Indianapolis": (39.7684, -86.1581),
    "Jacksonville": (30.3322, -81.6557),
    "Las Vegas": (36.1699, -115.1398),
    "Los Angeles": (34.0522, -118.2437),
    "Louisville": (38.2527, -85.7585),
    "Memphis": (35.1495, -90.0490),
    "Miami": (25.7617, -80.1918),
    "Milwaukee": (43.0389, -87.9065),
    "Minneapolis": (44.9778, -93.2650),
    "Nashville": (36.1627, -86.7816),
    "New Orleans": (29.9511, -90.0715),
    "New York": (40.7128, -74.0060),
    "Oklahoma City": (35.4676, -97.5164),
    "Orlando": (28.5383, -81.3792),
    "Philadelphia": (39.9526, -75.1652),
    "Phoenix": (33.4484, -112.0740),
    "Pittsburgh": (40.4406, -79.9959),
    "Portland": (45.5152, -122.6784),
    "Raleigh": (35.7796, -78.6382),
    "Sacramento": (38.5816, -121.4944),
    "San Antonio": (29.4241, -98.4936),
    "San Diego": (32.7157, -117.1611),
    "San Francisco": (37.7749, -122.4194),
    "San Jose": (37.3382, -121.8863),
    "Seattle": (47.6062, -122.3321),
    "St. Louis": (38.6270, -90.1994),
    "Tampa": (27.9506, -82.4572),
    "Washington, DC": (38.9072, -77.0369),
    "Unknown": US_CENTER,
}

CITY_ALIASES = {
    "nyc": "New York",
    "new york city": "New York",
    "la": "Los Angeles",
    "l.a.": "Los Angeles",
    "sf": "San Francisco",
    "san fran": "San Francisco",
    "dc": "Washington, DC",
    "washington dc": "Washington, DC",
    "d.c.": "Washington, DC",
    "st louis": "St. Louis",
}

# State centroids make the map forgiving when a demo record uses a state rather
# than a city (for example, "Ohio, USA"). City entries remain more precise.
STATE_COORDS = {
    "Alabama": (32.8067, -86.7911), "Alaska": (61.3707, -152.4044),
    "Arizona": (33.7298, -111.4312), "Arkansas": (34.9697, -92.3731),
    "California": (36.1162, -119.6816), "Colorado": (39.0598, -105.3111),
    "Connecticut": (41.5978, -72.7554), "Delaware": (39.3185, -75.5071),
    "Florida": (27.7663, -81.6868), "Georgia": (33.0406, -83.6431),
    "Hawaii": (21.0943, -157.4983), "Idaho": (44.2405, -114.4788),
    "Illinois": (40.3495, -88.9861), "Indiana": (39.8494, -86.2583),
    "Iowa": (42.0115, -93.2105), "Kansas": (38.5266, -96.7265),
    "Kentucky": (37.6681, -84.6701), "Louisiana": (31.1695, -91.8678),
    "Maine": (44.6939, -69.3819), "Maryland": (39.0639, -76.8021),
    "Massachusetts": (42.2302, -71.5301), "Michigan": (43.3266, -84.5361),
    "Minnesota": (45.6945, -93.9002), "Mississippi": (32.7416, -89.6787),
    "Missouri": (38.4561, -92.2884), "Montana": (46.9219, -110.4544),
    "Nebraska": (41.1254, -98.2681), "Nevada": (38.3135, -117.0554),
    "New Hampshire": (43.4525, -71.5639), "New Jersey": (40.2989, -74.5210),
    "New Mexico": (34.8405, -106.2485), "New York State": (42.1657, -74.9481),
    "North Carolina": (35.6301, -79.8064), "North Dakota": (47.5289, -99.7840),
    "Ohio": (40.3888, -82.7649), "Oklahoma": (35.5653, -96.9289),
    "Oregon": (44.5720, -122.0709), "Pennsylvania": (40.5908, -77.2098),
    "Rhode Island": (41.6809, -71.5118), "South Carolina": (33.8569, -80.9450),
    "South Dakota": (44.2998, -99.4388), "Tennessee": (35.7478, -86.6923),
    "Texas": (31.0545, -97.5635), "Utah": (40.1500, -111.8624),
    "Vermont": (44.0459, -72.7107), "Virginia": (37.7693, -78.1700),
    "Washington State": (47.4009, -121.4905), "West Virginia": (38.4912, -80.9545),
    "Wisconsin": (44.2685, -89.6165), "Wyoming": (42.7560, -107.3025),
}


def city_coordinates(city: str | None):
    """Return coordinates for a city, accepting case-insensitive aliases."""
    if not city:
        return CITY_COORDS["Unknown"]
    normalized = city.strip().lower().removesuffix(", usa").removesuffix(" usa").strip()
    canonical_name = CITY_ALIASES.get(normalized)
    if canonical_name:
        return CITY_COORDS[canonical_name]
    for name, coordinates in CITY_COORDS.items():
        if name.lower() == normalized:
            return coordinates
    for name, coordinates in STATE_COORDS.items():
        if name.lower() == normalized:
            return coordinates
    return None
