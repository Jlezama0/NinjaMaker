from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from Visitor import Visitor



class Stats:
    def __init__(self, attack=0, defense=0, chakra=0):
        self.attack = attack
        self.defense = defense
        self.chakra = chakra

    def to_dict(self):
        return self.__dict__



class Jutsu(ABC):
    @abstractmethod
    def get_name(self) -> str: ...
    @abstractmethod
    def get_description(self) -> str: ...
    @abstractmethod
    def get_chakra_cost(self) -> int: ...
    @abstractmethod
    def execute(self, user: "Ninja") -> str: ...


class CreateJutsu(Jutsu):
    def __init__(self, name: str, description: str, chakra_cost: int):
        self._name = name
        self._description = description
        self._chakra_cost = chakra_cost

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_chakra_cost(self) -> int:
        return self._chakra_cost

    def execute(self, user: "Ninja") -> str:
        return f"{user.get_name()} usa {self._name}! (Costo {self._chakra_cost} chakra)"



class Ninja(ABC):
    @abstractmethod
    def get_name(self): ...
    @abstractmethod
    def get_rank(self): ...
    @abstractmethod
    def get_stats(self): ...
    @abstractmethod
    def get_jutsus(self) -> List[Jutsu]: ...
    @abstractmethod
    def use_jutsu(self, name: str) -> str: ...
    @abstractmethod
    def accept(self, visitor: "Visitor") -> None: ...



class BaseNinja(Ninja):
    def __init__(self, name: str, rank: str, stats: Stats, jutsus: List[Jutsu]):
        self._name = name
        self._rank = rank
        self._stats = stats
        self._jutsus = jutsus

    def get_name(self):
        return self._name

    def get_rank(self):
        return self._rank

    def get_stats(self):
        return self._stats

    def get_jutsus(self) -> List[Jutsu]:
        return self._jutsus

    def use_jutsu(self, name: str) -> str:
        for jutsu in self._jutsus:
            if jutsu.get_name() == name:
                return jutsu.execute(self)
        return f"{self._name} no conoce el jutsu {name}."

    def accept(self, visitor: "Visitor") -> None:
        visitor.visit_ninja(self)



class KonohaNinja(BaseNinja): pass
class SunaNinja(BaseNinja): pass
class KiriNinja(BaseNinja): pass
class IwaNinja(BaseNinja): pass
class KumoNinja(BaseNinja): pass



class NinjaFactory(ABC):
    @abstractmethod
    def createNinja(self, name: str, rank: str) -> Ninja: ...
    @abstractmethod
    def createJutsuSet(self) -> List[Jutsu]: ...


class KonohaFactory(NinjaFactory):
    def createNinja(self, name="Naruto Uzumaki", rank="Genin") -> Ninja:
        stats = Stats(attack=70, defense=60, chakra=80)
        return KonohaNinja(name, rank, stats, self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Rasengan", "Esfera de chakra concentrado", 30),
            CreateJutsu("Kage Bunshin", "Clones de sombra", 20)
        ]


class SunaFactory(NinjaFactory):
    def createNinja(self, name="Gaara", rank="Jonin") -> Ninja:
        stats = Stats(attack=90, defense=85, chakra=95)
        return SunaNinja(name, rank, stats, self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Sabaku Kyū", "Prisión de arena", 25),
            CreateJutsu("Sabaku Taisō", "Aplastamiento de arena", 40)
        ]


class KiriFactory(NinjaFactory):
    def createNinja(self, name="Zabuza Momochi", rank="Chunin") -> Ninja:
        stats = Stats(attack=80, defense=70, chakra=75)
        return KiriNinja(name, rank, stats, self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Kirigakure no Jutsu", "Ocultar en la niebla", 15),
            CreateJutsu("Suiton: Suiryūdan", "Dragón de agua", 35)
        ]


class IwaFactory(NinjaFactory):
    def createNinja(self, name="Onoki", rank="Tsuchikage") -> Ninja:
        stats = Stats(attack=85, defense=70, chakra=90)
        return IwaNinja(name, rank, stats, self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Earth Style: Rock Avalanche", "Avalancha de rocas controladas", 35),
            CreateJutsu("Earth Wall", "Muro de tierra defensivo", 25)
        ]


class KumoFactory(NinjaFactory):
    def createNinja(self, name="A", rank="Raikage") -> Ninja:
        stats = Stats(attack=95, defense=80, chakra=85)
        return KumoNinja(name, rank, stats, self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Lightning Style: Thunderclap Arrow", "Flecha de trueno concentrado", 40),
            CreateJutsu("Static Armor", "Armadura eléctrica que paraliza al contacto", 30)
        ]



