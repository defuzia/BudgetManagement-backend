from core.api.v1.budget_management.schemas.operations import CategorySchema, OperationSchema
from core.apps.budgets.entities.operations import Category as CategoryEntity, Operation as OperationEntity
from core.apps.budgets.models.operations import Category as CategoryModel, Operation as OperationModel


class CategoryConverter:
    @staticmethod
    def to_entity(entity: CategoryEntity) -> CategorySchema:
        ...

    @staticmethod
    def from_entity(model: CategoryModel) -> CategoryEntity:
        ...


class OperationConverter:
    @staticmethod
    def to_entity(entity: OperationEntity) -> OperationSchema:
        ...

    @staticmethod
    def from_entity(model: OperationModel) -> OperationEntity:
        ...
