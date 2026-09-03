"""A deliberately small U.S. city directory for local demo records."""

CITY_COORDINATES = {
    "Atlanta, GA": (33.7490, -84.3880),
    "Austin, TX": (30.2672, -97.7431),
    "Boston, MA": (42.3601, -71.0589),
    "Chicago, IL": (41.8781, -87.6298),
    "Columbus, OH": (39.9612, -82.9988),
    "Denver, CO": (39.7392, -104.9903),
    "Detroit, MI": (42.3314, -83.0458),
    "Houston, TX": (29.7604, -95.3698),
    "Las Vegas, NV": (36.1699, -115.1398),
    "Los Angeles, CA": (34.0522, -118.2437),
    "Miami, FL": (25.7617, -80.1918),
    "New York, NY": (40.7128, -74.0060),
    "Phoenix, AZ": (33.4484, -112.0740),
    "Portland, OR": (45.5152, -122.6784),
    "Seattle, WA": (47.6062, -122.3321),
    "Washington, DC": (38.9072, -77.0369),
}


def locate(city: str):
    return CITY_COORDINATES.get(city)
