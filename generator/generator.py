from config.operator_definition import OPERATORS, DataType
from generator.expression import *
import random


class Generator:

    def __init__(
        self,
        operator_selector,
        field_selector,
        parameter_generator,
        max_depth=4
    ):
        self.operator_selector = operator_selector
        self.field_selector = field_selector
        self.parameter_generator = parameter_generator
        self.max_depth = max_depth

    def generate(self):
        # 최상위 Alpha는 Matrix(Expression)
        return self._generate_node(DataType.MATRIX, 0)

    def _generate_node(self, required_type, depth):

        # Leaf(Field)가 될 수 있는 자료형
        FIELD_TYPES = {
            DataType.MATRIX,
            DataType.VECTOR,
            DataType.GROUP,
        }

        # 최대 깊이에서는 Leaf만 생성
        if depth >= self.max_depth:

            if required_type in FIELD_TYPES:
                field = self.field_selector.select(required_type)
                return FieldNode(field.id)

            elif required_type == DataType.INTEGER:
                return ConstantNode(
                    self.parameter_generator.generate_integer()
                )

            elif required_type == DataType.WINDOW:
                return ConstantNode(
                    self.parameter_generator.generate_window()
                )

            raise ValueError(f"Unsupported DataType: {required_type}")

        # 일정 확률로 Field 생성
        if required_type in FIELD_TYPES:

            if random.random() < 0.25:
                field = self.field_selector.select(required_type)
                return FieldNode(field.id)

        op = self.operator_selector.select(required_type)

        children = []

        for input_type in op.inputs:

            if input_type == DataType.INTEGER:

                children.append(
                    ConstantNode(
                        self.parameter_generator.generate_integer()
                    )
                )

            elif input_type == DataType.WINDOW:

                children.append(
                    ConstantNode(
                        self.parameter_generator.generate_window()
                    )
                )

            else:

                children.append(
                    self._generate_node(
                        input_type,
                        depth + 1
                    )
                )

        return OperatorNode(op.name, children)