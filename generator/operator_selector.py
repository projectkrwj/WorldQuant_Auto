import random
from config.operator_definition import OperatorDefinition, OPERATORS, DataType

"""이 클래스는 
selector = RandomOperatorSelector()
op = selector.select(DataType.VECTOR)
print(op.name)
이거만 되면 됨"""

class RandomOperatorSelector:
    """출력 타입에 맞는 Operator를 랜덤 선택"""

    def __init__(self, operators=None):
        self.operators = operators or OPERATORS

    def select(self, output_type):

        candidates = [
            op for op in self.operators
            if op.output == output_type
        ]

        if not candidates:
            raise ValueError(
                f"No operator produces output type: {output_type}"
            )

        return random.choice(candidates)