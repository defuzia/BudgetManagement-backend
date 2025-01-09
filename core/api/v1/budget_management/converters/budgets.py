from core.api.v1.budget_management.schemas.budgets import CurrencySchema, BudgetSchema
from core.apps.budgets.entities.budgets import Currency as CurrencyEntity, Budget as BudgetEntity
from core.apps.budgets.models import Currency as CurrencyModel, Budget as BudgetModel


class CurrencyConverter:
    @staticmethod
    def to_entity(entity: CurrencyEntity) -> CurrencySchema:
        ...

    @staticmethod
    def from_entity(model: CurrencyModel) -> CurrencyEntity:
        ...


class BudgetConverter:
    @staticmethod
    def to_entity(entity: BudgetEntity) -> BudgetSchema:
        ...

    @staticmethod
    def from_entity(model: BudgetModel) -> BudgetEntity:
        ...
