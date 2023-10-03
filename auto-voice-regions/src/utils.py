import json
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from random import randint
from typing import NamedTuple

from allay import Parser
from minecraft_text_components import minify
from nbtlib import Float, List

Z_FIGHTING_OFFSET = 0.004

class Coords(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: "Coords"):
        return Coords(*(self[i] + other[i] for i in range(3)))

    def __sub__(self, other: "Coords"):
        return Coords(*(self[i] - other[i] for i in range(3)))


@dataclass(frozen=True)
class Location:
    name: str
    origin: Coords
    corner: Coords
    _color: str | None = None

    @cached_property
    def color(self):
        if self._color is None:
            r = randint(128, 255)
            g = randint(128, 255)
            b = randint(128, 255)
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return self._color


    @cached_property
    def x(self):
        return self.origin.x

    @cached_property
    def y(self):
        return self.origin.y

    @cached_property
    def z(self):
        return self.origin.z

    @cached_property
    def dxdydz(self):
        return self.corner - self.origin

    @cached_property
    def dx(self):
        return self.dxdydz.x
    
    @cached_property
    def dy(self):
        return self.dxdydz.y

    @cached_property
    def dz(self):
        return self.dxdydz.z

    @cached_property
    def scale(self):
        return List(
            [
                Float(self.dx + 1 + (Z_FIGHTING_OFFSET * 2)),
                Float(self.dy - 1 + (Z_FIGHTING_OFFSET * 2)),
                Float(self.dz + 1 + (Z_FIGHTING_OFFSET * 2)),
            ]
        )

    @cached_property
    def pretty_name(self):
        return self.name.replace("-", " ").title()

    @cached_property
    def id(self):
        return self.name.lower().replace(" ", "-").replace("-", "_")

    def __str__(self):
        return self.id

    @classmethod
    def parse_coords(cls, coords: str | None = None) -> list["Location"]:
        if coords is None:
            if not (path := Path("src/config.json")).exists():
                raise ValueError("No src/config.json file found and `coords` not provided")
            coords = json.loads(path.read_text())

        return [
            cls(
                name=dic["name"],
                origin=Coords(*(int(number.strip()) for number in dic["origin"].split(" "))),
                corner=Coords(*(int(number.strip()) for number in dic["corner"].split(" "))),
            )
            for dic in coords["locations"]
        ]


def allay(input: str | Callable[[str], str]) -> str | dict[str, str]:
    match input:
        case str(text):
            return minify(
                Parser(json_dump=False).parse(
                    "@gray1 = (#89908B)\n"
                    "@gray2 = (#6A6F71)\n"
                    "@success = (#ACF39D)\n"
                    "@error = (#FAC8CD)\n"
                    "\n#ALLAYDEFS\n"
                    f"{text}"
                )
            )

        case _ as func:
            def inner(*args, **kwargs):
                return allay(func(*args, **kwargs))
        
            return inner
