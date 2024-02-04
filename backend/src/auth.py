
from typing import Any


class Example:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
