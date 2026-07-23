from .iarea_service import IAreaService
from repositories.area.iarea_repository import IAreaRepository

class AreaService(IAreaService):
    def __init__(self, area_repository: IAreaRepository):
        self.area_repository = area_repository

    def obtener_areas(self):
        return self.area_repository.get_all()

    def obtener_area_por_id(self, id):
        return self.area_repository.get_by_id(id)

    def obtener_area_por_nombre(self, nombre):
        return self.area_repository.get_by_nombre(nombre)