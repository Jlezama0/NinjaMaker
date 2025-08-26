from abc import ABC, abstractmethod
from enum import Enum
from typing import List
import json

# VALORES CONSTANTES
class Rank(Enum):
    GENIN = "Genin"
    CHUNIN = "Chunin"
    JONIN = "Jonin"

class MissionRank(Enum):
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"

# ESTADISTICAS (COMPONENTES QUE DEBE TENER EL NINJA)
class Stats:
    def __init__(self, attack: int, defense: int, chakra: int):
        self.attack = attack
        self.defense = defense
        self.chakra = chakra

    def __str__(self):
        return f"ATK:{self.attack}, DEF:{self.defense}, CHK:{self.chakra}"

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
    @abstractmethod
    def get_name(self) -> str: ...
    @abstractmethod
    def get_rank(self) -> Rank: ...
    @abstractmethod
    def get_stats(self) -> Stats: ...
    @abstractmethod
    def get_jutsus(self) -> List[Jutsu]: ...
    @abstractmethod
    def use_jutsu(self, name: str) -> str: ...
    @abstractmethod
    def accept(self, visitor: "Visitor") -> None: ...

# MISION REPRESENTA CADA MISION CON SU DIFICULTAD RANGO REQUERIDO Y RECOMPENSA. TAMBIEN VALIDA SI PUEDE SER ACEPTADA
class Mission:
    def __init__(self, mission_id: str, title: str, required_rank: MissionRank,
                 reward: int, description: str):
        self.id = mission_id
        self.title = title
        self.required_rank = required_rank
        self.reward = reward
        self.description = description

    def is_eligible(self, ninja: Ninja) -> bool:
        return self._rank_allowed(ninja.get_rank())

    def _rank_allowed(self, rank: Rank) -> bool:
        hierarchy = {
            Rank.GENIN: [MissionRank.D, MissionRank.C],
            Rank.CHUNIN: [MissionRank.C, MissionRank.B, MissionRank.D],
            Rank.JONIN: [MissionRank.A, MissionRank.S, MissionRank.B, MissionRank.C, MissionRank.D]
        }
        return self.required_rank in hierarchy[rank]
    
    def accept(self, visitor: "Visitor") -> None:
        visitor.visit_mission(self)

# MISSIONMANAGER GESTIONA Y ADMINISTRA CADA MISION
class MissionManager:
    def __init__(self):
        self.missions: List[Mission] = []

    def add_mission(self, mission: Mission):
        self.missions.append(mission)

    def list_by_rank(self, rank: MissionRank) -> List[Mission]:
        return [m for m in self.missions if m.required_rank == rank]

    def assign(self, ninja: Ninja, mission_id: str) -> str:
        mission = next((m for m in self.missions if m.id == mission_id), None)
        if not mission:
            return "Misión no encontrada."
        if mission.is_eligible(ninja):
            return f"{ninja.get_name()} ha aceptado la misión {mission.title}"
        return f"{ninja.get_name()} no tiene rango suficiente para esta misión."

# FACTORYNINJA CLASE BASE DE NINJAS (DEFINE LA ESTRUCTURA COMÚN QUE USAN LAS FÁBRICAS PARA CREAR NINJAS)
class BaseNinja(Ninja):
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        self._name = name
        self._rank = rank
        self._stats = stats
        self._jutsus = jutsus

    def get_name(self) -> str:
        return self._name

    def get_rank(self) -> Rank:
        return self._rank

    def get_stats(self) -> Stats:
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
    

# ALDEANINJA (DA CONTENIDO A LA CREACION DE LOS NINJAS DE CADA FABRICA)
class KonohaNinja(BaseNinja): 
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        super().__init__(name, rank, stats, jutsus)

class SunaNinja(BaseNinja):
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        super().__init__(name, rank, stats, jutsus)

class KiriNinja(BaseNinja):
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        super().__init__(name, rank, stats, jutsus)

class IwaNinja(BaseNinja):
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        super().__init__(name, rank, stats, jutsus)

class KumoNinja(BaseNinja):
    def __init__(self, name: str, rank: Rank, stats: Stats, jutsus: List[Jutsu]):
        super().__init__(name, rank, stats, jutsus)

# NINJAFACTORY Y ALDEAFACTORY (ES LA QUE SE ENCARGA DE CREAR CADA NINJA Y JUTSUS BASICOS)
class NinjaFactory(ABC):
    @abstractmethod
    def createNinja(self, name: str, rank: Rank) -> Ninja: ...
    @abstractmethod
    def createJutsuSet(self) -> List[Jutsu]: ...

class KonohaFactory(NinjaFactory):
    def createNinja(self, name: str, rank: Rank) -> Ninja:
        return KonohaNinja(name, rank, Stats(70, 60, 80), self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Rasengan", "Esfera de chakra concentrado", 30),
            CreateJutsu("Kage Bunshin", "Clones de sombra", 20)
        ]

class SunaFactory(NinjaFactory):
    def createNinja(self, name: str, rank: Rank) -> Ninja:
        return SunaNinja(name, rank, Stats(60, 70, 65), self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Sabaku Kyū", "Prisión de arena", 25),
            CreateJutsu("Sabaku Taisō", "Aplastamiento de arena", 40)
        ]

class KiriFactory(NinjaFactory):
    def createNinja(self, name: str, rank: Rank) -> Ninja:
        return KiriNinja(name, rank, Stats(75, 55, 70), self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Kirigakure no Jutsu", "Ocultar en la niebla", 15),
            CreateJutsu("Suiton: Suiryūdan", "Dragón de agua", 35)
        ]

class IwaFactory(NinjaFactory):
    def createNinja(self, name: str, rank: Rank) -> Ninja:
        return IwaNinja(name, rank, Stats(80, 55, 70), self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Earth Style: Rock Avalanche", "Avalancha de rocas controladas", 35),
            CreateJutsu("Earth Wall", "Muro de tierra defensivo", 25)
        ]

class KumoFactory(NinjaFactory):
    def createNinja(self, name: str, rank: Rank) -> Ninja:
        return KumoNinja(name, rank, Stats(70, 80, 65), self.createJutsuSet())

    def createJutsuSet(self) -> List[Jutsu]:
        return [
            CreateJutsu("Lightning Style: Thunderclap Arrow", "Flecha de trueno concentrado", 40),
            CreateJutsu("Static Armor", "Armadura eléctrica que paraliza al contacto", 30)
        ]
    
class Visitor(ABC):
    @abstractmethod
    def visit_ninja(self, ninja: Ninja) -> None: ...
    @abstractmethod
    def visit_mission(self, mission: Mission) -> None: ...
    def reset(self): pass
    def result(self): return None

class JSONExportVisitor(Visitor):
    def __init__(self):
        self.reset()

    def reset(self): self._data = {"ninjas": [], "missions": []}

    def visit_ninja(self, ninja: Ninja) -> None:
        stats = ninja.get_stats()
        jutsus = [{
            "name": j.get_name(),
            "description": j.get_description(),
            "chakra_cost": j.get_chakra_cost()
        } for j in ninja.get_jutsus()]
        village = type(ninja).__name__.replace("Ninja", "")
        self._data["ninjas"].append({
            "name": ninja.get_name(),
            "village": village,
            "rank": ninja.get_rank().value,
            "stats": {"attack": stats.attack, "defense": stats.defense, "chakra": stats.chakra},
            "jutsus": jutsus
        })

    def visit_mission(self, mission: Mission) -> None:
        self._data["missions"].append({
            "id": mission.id,
            "title": mission.title,
            "required_rank": mission.required_rank.value,
            "reward": mission.reward,
            "description": mission.description
        })

    def result(self): return json.dumps(self._data, ensure_ascii=False, indent=2)

def export_all(visitor: Visitor, ninjas: List[Ninja], missions: List[Mission]):
    visitor.reset()
    for n in ninjas: n.accept(visitor)
    for m in missions: m.accept(visitor)
    return visitor.result()



def main():
    # Crear ninjas con factories
    konoha_factory = KonohaFactory()
    suna_factory = SunaFactory()
    kiri_factory = KiriFactory()

    naruto = konoha_factory.createNinja("Naruto Uzumaki", Rank.GENIN)
    gaara = suna_factory.createNinja("Gaara", Rank.JONIN)
    zabuza = kiri_factory.createNinja("Zabuza Momochi", Rank.CHUNIN)
    ninjas = [naruto, gaara, zabuza]

    # Crear misiones
    m1 = Mission("M001", "Proteger al Puente", MissionRank.C, 500, "Defender al constructor de un puente.")
    m2 = Mission("M002", "Capturar espía", MissionRank.A, 1200, "Atrapar al espía en territorio enemigo.")
    m3 = Mission("M003", "Defender Konoha", MissionRank.S, 5000, "Proteger la aldea de un ataque enemigo.")
    missions = [m1, m2, m3]

    # Exportar en JSON con Visitor
    json_exporter = JSONExportVisitor()
    reporte_json = export_all(json_exporter, ninjas, missions)

    # Guardar en archivo reporte.json
    with open("reporte.json", "w", encoding="utf-8") as f:
        f.write(reporte_json)

    print("Archivo generado")
    print("Ninjas exportados:", [n.get_name() for n in ninjas])
    print("Misiones exportadas:", [m.title for m in missions])

if __name__ == "__main__":
    main()