import random


class RandomParameterGenerator:
    """
    Constant parameter 생성 담당

    현재:
        Random 방식

    추후:
        BayesianParameterGenerator
        AdaptiveParameterGenerator
    로 교체 가능
    """

    def __init__(self):

        # WorldQuant에서 자주 사용하는 window 후보
        self.window_values = [
            5,
            10,
            20,
            30,
            60,
            120,
            252
        ]

        # 혹시 integer input이 필요한 operator 대비
        self.integer_values = [
            1,
            2,
            3,
            5,
            10
        ]


    def generate_window(self) -> int:
        """
        DataType.WINDOW 생성

        예:
        ts_mean(close, 20)
        """

        return random.choice(
            self.window_values
        )


    def generate_integer(self) -> int:
        """
        DataType.INTEGER 생성

        현재 사용 빈도 낮음.
        추후 operator input 확장 대비.
        """

        return random.choice(
            self.integer_values
        )
