import random

from config.operator_definition import DataType
from database.field_repository import FieldRepository


class RandomFieldSelector:
    """
    Field 선택 전략

    현재:
        Random 선택

    추후:
        BayesianFieldSelector
        WeightedFieldSelector
        GeneticFieldSelector
    로 교체 가능
    """


    def __init__(
        self,
        repository: FieldRepository
    ):
        self.repository = repository


    def select(
        self,
        data_type: DataType
    ):
        """
        필요한 DataType의 Field 하나 선택
        """

        fields = self.repository.get_fields_by_data_type(
            data_type
        )

        if not fields:
            raise ValueError(
                f"No field found for type {data_type}"
            )

        return random.choice(fields)
