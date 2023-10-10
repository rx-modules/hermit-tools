from dataclasses import dataclass, replace
from functools import cache
from typing import Self

import bolt_expressions as expr
from beet import Context, Generator
from bolt import Runtime


@dataclass
class ResourceGenerator:
    _generator: Generator

    def __init__(self, _generator: Generator | Context):
        match _generator:
            case Generator():
                self._generator = _generator
            case Context():
                self._generator = _generator.generate

    def __truediv__(self, path: str):
        return replace(self, _generator=self._generator[path])

    @cache
    def __getattr__(self, key: str):
        return self.__getitem__(key)

    @cache
    def __getitem__(self, key: str):
        return self._generator.id(key)

    @cache
    def __call__(
        self,
        *,
        scoreboard: str = "",
        entity: str = "",
        storage: str = "",
        block: str = "",
        criteria: str = "dummy",
    ):
        def _generator():
            if scoreboard:
                yield expr.Scoreboard.objective(self[scoreboard], criteria=criteria)

            if entity:
                yield expr.Data.entity(entity)

            if storage:
                yield expr.Data.storage(self[storage].replace(".", ":", 1))

            if block:
                yield expr.Data.block(block)

        generated = list(_generator())

        if len(generated) > 1:
            return generated

        return generated.pop()

    def __neg__(self):
        return str(self)

    def __str__(self):
        return self._generator.format("{namespace}:{path}")[:-1]

    def __eq__(self, other: Self):
        return str(self) == str(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __hash__(self):
        return hash(str(self))


def beet_default(ctx: Context):
    """Adds `ctx.inject(ResourceGenerator)` as `pack` to runtime globals"""
    runtime = ctx.inject(Runtime)
    runtime.globals["pack"] = ctx.inject(ResourceGenerator)
