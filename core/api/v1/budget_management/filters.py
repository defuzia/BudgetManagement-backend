from ninja import Schema


class CurrencyFilters(Schema):
    search: str | None = None


class BudgetFilters(Schema):
    search: str | None = None


class CategoryFilters(Schema):
    search: str | None = None


class OperationFilters(Schema):
    search: str | None = None
