from abc import ABC, abstractmethod
from enum import Enum
from typing import List




# JUTSU PRODUCTO ABSTRACTO (ESTE NOS PERMITE DEFINIR LO QUE PUEDE HACER CADA JUTSU)
class Jutsu(ABC):
    @abstractmethod
    def get_name(self) -> str: ...
    @abstractmethod
    def get_description(self) -> str: ...
    @abstractmethod
    def get_chakra_cost(self) -> int: ...
    @abstractmethod
    def execute(self, user: "Ninja") -> str: ...

# CREATEJUTSU PRODUCTO CONCRETO (COMPLEMENTA LO QUE DEBE TENER CADA JUTSU)
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



# NINJA PRODUCTO ABSTRACTO (DEFINE A CADA NINJA PERO NO REPRESENTA A NINGUN NINJA EN ESPECIFICO)
class Ninja(ABC):
    def get_jutsus(self) -> List["Jutsu"]: ...
    @abstractmethod
    def use_jutsu(self, name: str) -> str: ...



# FACTORYNINJA CLASE BASE DE NINJAS (DEFINE LA ESTRUCTURA COMÚN QUE USAN LAS FÁBRICAS PARA CREAR NINJAS)
class BaseNinja(Ninja):
    def __init__(self, jutsus: List["Jutsu"]):
        self._jutsus = jutsus

    def get_jutsus(self) -> List["Jutsu"]:
        return self._jutsus

    def use_jutsu(self, name: str) -> str:
        for jutsu in self._jutsus:
            if jutsu.get_name() == name:
                return jutsu.execute(self)
        return f"Este ninja no conoce el jutsu {name}."

# ALDEANINJA (DA CONTENIDO A LA CREACION DE LOS NINJAS DE CADA FABRICA)
class KonohaNinja(BaseNinja):
    def __init__(self, jutsus: List["Jutsu"]):
        super().__init__(jutsus)

class SunaNinja(BaseNinja):
    def __init__(self, jutsus: List["Jutsu"]):
        super().__init__(jutsus)

class KiriNinja(BaseNinja):
    def __init__(self, jutsus: List["Jutsu"]):
        super().__init__(jutsus)

class IwaNinja(BaseNinja):
    def __init__(self, jutsus: List["Jutsu"]):
        super().__init__(jutsus)

class KumoNinja(BaseNinja):
    def __init__(self, jutsus: List["Jutsu"]):
        super().__init__(jutsus)

# NINJAFACTORY Y ALDEAFACTORY (ES LA QUE SE ENCARGA DE CREAR CADA NINJA Y JUTSUS BASICOS)
class NinjaFactory(ABC):
    @abstractmethod
    def createNinja(self) -> Ninja: ...
    @abstractmethod
    def createJutsuSet(self) -> List[Jutsu]: ...

class KonohaFactory(NinjaFactory):
    def createNinja(self) -> Ninja:
        return KonohaNinja(self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Rasengan", "Esfera de chakra concentrado", 30),
            CreateJutsu("Kage Bunshin", "Clones de sombra", 20)
        ]

class SunaFactory(NinjaFactory):
    def createNinja(self) -> Ninja:
        return SunaNinja(self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Sabaku Kyū", "Prisión de arena", 25),
            CreateJutsu("Sabaku Taisō", "Aplastamiento de arena", 40)
        ]

class KiriFactory(NinjaFactory):
    def createNinja(self) -> Ninja:
        return KiriNinja(self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Kirigakure no Jutsu", "Ocultar en la niebla", 15),
            CreateJutsu("Suiton: Suiryūdan", "Dragón de agua", 35)
        ]

class IwaFactory(NinjaFactory):
    def createNinja(self) -> Ninja:
        return IwaNinja(self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Earth Style: Rock Avalanche", "Avalancha de rocas controladas", 35),
            CreateJutsu("Earth Wall", "Muro de tierra defensivo", 25)
        ]

class KumoFactory(NinjaFactory):
    def createNinja(self) -> Ninja:
        return KumoNinja(self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Lightning Style: Thunderclap Arrow", "Flecha de trueno concentrado", 40),
            CreateJutsu("Static Armor", "Armadura eléctrica que paraliza al contacto", 30)
        ]


