from dataclasses import dataclass, field
from typing import Any


class Node:
    pass


@dataclass
class FieldNode(Node):
    name: str


@dataclass
class ConstantNode(Node):
    value: Any


@dataclass
class OperatorNode(Node):
    operator: str
    children: list[Node] = field(default_factory=list)