from Rectangle import Rectangle


class Object:
    """
    Object loaded from disk
    """
    def __init__(self, id: int, coords):
        self.id = id
        self.mbr = self.__calculate_MBR(coords)
        self.geohash = None

    def __calculate_MBR(self, coords) -> Rectangle:
        x_low = min(coord[0] for coord in coords)
        x_high = max(coord[0] for coord in coords)
        y_low = min(coord[1] for coord in coords)
        y_high = max(coord[1] for coord in coords)

        return Rectangle(x_low, x_high, y_low, y_high)

    def calculate_geohash(self):
        try:
            import pymorton as pm
        except ImportError:
            raise RuntimeError("The following library is required to calculate geohash: pymorton")
        self.geohash = pm.interleave_latlng(*self.mbr.centroid())

    def __str__(self):
        return f'Object Id: {self.id}, Object MBR: {self.mbr}\n'

