#Builder

from abc import ABC, abstractmethod
from typing import List

from FactoryAbstractNaruto import Jutsu, NinjaFactory, KonohaFactory, IwaFactory, KiriFactory, KumoFactory, SunaFactory


class Stats:
    def __init__(self):
        self.Chakra: int = 0
        self.chakraControl: int = 0
        self.Ninjutsu: int = 0
        self.Taijutsu: int = 0
        self.Genjutsu: int = 0
        self.Speed: int = 0
        self.Resistance: int = 0
        self.Intelligence: int = 0
        self.Willpower: int = 0

    def to_dict(self):
        return self.__dict__


class FinalNinja:
    def __init__(self):
        self.name = None
        self.rank = None
        self.chakra = None
        self.clan = None
        self.styleFight = None
        self.weapon = None
        self.village = None            # <- añadido
        self.jutsus: List["Jutsu"] = []  # <- añadido
        self.stats = Stats()

    def to_dict(self):
        return {
            "name": self.name,
            "rank": self.rank,
            "chakra": self.chakra,
            "clan": self.clan,
            "styleFight": self.styleFight,
            "weapon": self.weapon,
            "village": self.village,
            "jutsus": [j.get_name() for j in self.jutsus] if self.jutsus else [],
            "stats": self.stats.to_dict()
        }

    def __str__(self):
        return str(self.to_dict())
    

# Interfaz Builder
class Builder(ABC):
    @abstractmethod
    def reset(self): ...
    @abstractmethod
    def setName(self, name: str): ...
    @abstractmethod
    def setRank(self, rank: str): ...
    @abstractmethod
    def setChakra(self, chakra: int): ...
    @abstractmethod
    def setClan(self, clan: str): ...
    @abstractmethod
    def setStyleFight(self, style: str): ...
    @abstractmethod
    def setWeapon(self, weapon: str): ...
    @abstractmethod
    def setStats(self, stats: Stats): ...
    # añadidos para integrar la fábrica
    @abstractmethod
    def setVillage(self, village: str): ...
    @abstractmethod
    def setJutsus(self, jutsus: List["Jutsu"]): ...
    @abstractmethod
    def getResult(self) -> FinalNinja: ...


# Builder concreto
class NinjaBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self.ninja = FinalNinja()

    def setName(self, name: str):
        self.ninja.name = name
        return self

    def setRank(self, rank: str):
        self.ninja.rank = rank
        return self

    def setChakra(self, chakra: int):
        self.ninja.chakra = chakra
        return self

    def setClan(self, clan: str):
        self.ninja.clan = clan
        return self

    def setStyleFight(self, style: str):
        self.ninja.styleFight = style
        return self

    def setWeapon(self, weapon: str):
        self.ninja.weapon = weapon
        return self

    def setStats(self, stats: Stats):
        self.ninja.stats = stats
        return self

    def setVillage(self, village: str):
        self.ninja.village = village
        return self

    def setJutsus(self, jutsus: List["Jutsu"]):
        self.ninja.jutsus = jutsus or []
        return self

    def getResult(self) -> FinalNinja:
        result = self.ninja
        self.reset()
        return result

class Director:
    """Orquesta: 1) pide ninja base a la Factory (aldea+jutsus),
        2) aplica personalización con el Builder, 3) devuelve FinalNinja."""
    def __init__(self, factory: NinjaFactory):
        self.factory = factory

    def makeNinja(
        self,
        builder: Builder,
        *,
        name: str,
        rank: str,
        chakra: int,
        clan: str,
        styleFight: str,
        weapon: str,
        stats: Stats
    ) -> FinalNinja:
        # 1) Ninja base por aldea (trae jutsus característicos)
        base = self.factory.createNinja()
        village_name = type(base).__name__.replace("Ninja", "")  # ej. "Konoha"

        # 2) Secuencia de construcción del Director
        builder.reset()
        builder.setName(name)\
            .setRank(rank)\
            .setChakra(chakra)\
            .setClan(clan)\
            .setStyleFight(styleFight)\
            .setWeapon(weapon)\
            .setStats(stats)\
            .setVillage(village_name)\
            .setJutsus(base.get_jutsus())

        # 3) Resultado final
        return builder.getResult()
    

factory = KonohaFactory()
director = Director(factory)
builder = NinjaBuilder()

stats = Stats()
stats.Ninjutsu = 80
stats.Willpower = 95

ninja_final = director.makeNinja(
    builder,
    name="Naruto",
    rank="Genin",
    chakra=1000,
    clan="Uzumaki",
    styleFight="Multi-clones",
    weapon="Kunai",
    stats=stats
)

print(ninja_final)  # incluye village="Konoha" y jutsus de la fábrica