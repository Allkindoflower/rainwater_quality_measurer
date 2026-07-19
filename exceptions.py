# Custom Exceptions


class IpLocationFailed(Exception):
    """Throws if geocoding service fails."""
    pass

class AQITooLow(Exception):
    """Throws if the air quality is very low."""
    pass