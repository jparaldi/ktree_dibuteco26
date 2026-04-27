class Point:
    def __init__(
        self,
        id: int,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        neighborhood: str = None,
        city: str = None,
        cep: str = None,
    ):
        self.id = id
        self.name = name
        self.address = address
        self.adress = address
        self.latitude = latitude
        self.longitude = longitude
        self.neighborhood = neighborhood
        self.city = city
        self.cep = cep

    # Função muito importante para a Kd-Tree
    def get_coord(self, axis: int) -> float:
        if axis == 0:
            return self.latitude
        elif axis == 1:
            return self.longitude
        else:
            raise ValueError("Deve ser um valor entre 0 e 1")
        
    def __repr__(self):
        return (
            f"Ponto(id={self.id}, name='{self.name}', address='{self.address}', "
            f"latitude={self.latitude}, longitude={self.longitude})"
        )