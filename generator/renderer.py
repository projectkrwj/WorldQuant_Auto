from generator.expression import OperatorNode, FieldNode, ConstantNode


def render(node):
    if isinstance(node, FieldNode):
        return node.name

    if isinstance(node, ConstantNode):
        return str(node.value)

    if isinstance(node, OperatorNode):
        args = ",".join(
            render(child)
            for child in node.children
        )

        return f"{node.operator}({args})"


    raise TypeError(
        f"Unknown node type: {type(node)}"
    )