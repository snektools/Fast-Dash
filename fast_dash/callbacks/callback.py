import dataclasses
from dash.dependencies import Input, Output, State
import typing


@dataclasses.dataclass
class CallbackDefinition:
    inputs: typing.List[Input]
    outputs: typing.List[Output]
    func: typing.Callable
    states: typing.List[State] = tuple()
