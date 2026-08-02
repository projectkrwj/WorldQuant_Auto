from generator.renderer import render


class AlphaBuilder:

    def __init__(
        self,
        generator,
        settings
    ):
        self.generator = generator
        self.settings = settings


    def build(self):

        node = self.generator.generate()

        expression = render(node)

        return {
            "expression": expression,
            **self.settings
        }