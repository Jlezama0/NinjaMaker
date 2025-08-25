# MissionSystem.py

from enum import Enum, auto
from typing import List

# Importamos las clases necesarias para crear nuestro ninja de prueba
from NinjaBuilder import FinalNinja, Stats, Director, NinjaBuilder
from FactoryAbstractNaruto import KonohaFactory

# --- Definiciones de Rangos (Necesarias para el sistema de misiones) ---

class Rank(Enum):
    """Define los rangos que puede tener un ninja."""
    GENIN = auto()
    CHUNIN = auto()
    JONIN = auto()

class MissionRank(Enum):
    """Define los rangos de dificultad de las misiones."""
    D = auto()
    C = auto()
    B = auto()
    A = auto()
    S = auto()

# Mapeo para convertir el rango de string (en FinalNinja) a nuestro Enum
RANK_MAP = {
    "Genin": Rank.GENIN,
    "Chunin": Rank.CHUNIN,
    "Jonin": Rank.JONIN
}

# --- Clases de Misiones (Adaptadas para FinalNinja) ---

class Mission:
    """
    Representa una misión.
    Ahora valida la elegibilidad usando el objeto FinalNinja.
    """
    def __init__(self, mission_id: str, title: str, required_rank: MissionRank,
                reward: int, description: str):
        self.id = mission_id
        self.title = title
        self.required_rank = required_rank
        self.reward = reward
        self.description = description

    def is_eligible(self, ninja: FinalNinja) -> bool:
        """
        Verifica si el ninja tiene el rango adecuado para la misión.
        MODIFICACIÓN: Accede a 'ninja.rank' y usa el MAPA para convertirlo.
        """
        ninja_rank_str = ninja.rank
        if ninja_rank_str not in RANK_MAP:
            return False # Si el rango del ninja no es válido, no es elegible.
            
        ninja_rank_enum = RANK_MAP[ninja_rank_str]
        return self._rank_allowed(ninja_rank_enum)

    def _rank_allowed(self, rank: Rank) -> bool:
        """Lógica interna para verificar permisos de rango."""
        hierarchy = {
            Rank.GENIN: [MissionRank.D, MissionRank.C],
            Rank.CHUNIN: [MissionRank.D, MissionRank.C, MissionRank.B],
            Rank.JONIN: [MissionRank.D, MissionRank.C, MissionRank.B, MissionRank.A, MissionRank.S]
        }
        return self.required_rank in hierarchy.get(rank, [])


class MissionManager:
    """
    Gestiona la creación y asignación de misiones.
    Adaptado para trabajar con FinalNinja.
    """
    def __init__(self):
        self.missions: List[Mission] = []

    def add_mission(self, mission: Mission):
        self.missions.append(mission)
        print(f"Misión '{mission.title}' [Rango {mission.required_rank.name}] añadida al tablero.")

    def assign(self, ninja: FinalNinja, mission_id: str) -> str:
        """
        Asigna una misión a un ninja si cumple los requisitos.
        MODIFICACIÓN: Usa 'ninja.name' en los mensajes.
        """
        mission = next((m for m in self.missions if m.id == mission_id), None)
        if not mission:
            return "❌ Misión no encontrada."
        
        if mission.is_eligible(ninja):
            return f"✅ ¡{ninja.name} ha aceptado la misión '{mission.title}'!"
        
        return f"❌ {ninja.name} no tiene el rango suficiente para la misión '{mission.title}'."

# --- EJEMPLO DE USO ---

# 1. Creamos un ninja de rango Genin
factory = KonohaFactory()
director = Director(factory)
builder = NinjaBuilder()

stats_naruto = Stats()
stats_naruto.Ninjutsu = 90
stats_naruto.Willpower = 100

ninja_naruto = director.makeNinja(
    builder,
    name="Naruto",
    rank="Genin",  # <- Rango importante para las misiones
    chakra=1000,
    clan="Uzumaki",
    styleFight="Multi-clones",
    weapon="Kunai",
    stats=stats_naruto
)

print("--- Creación del Ninja ---")
print(f"Ninja creado: {ninja_naruto.name}, Rango: {ninja_naruto.rank}")
print("-" * 25)


# 2. Creamos y añadimos misiones al MissionManager
mission_board = MissionManager()
print("\n--- Preparando Misiones ---")
mission_board.add_mission(
    Mission("M01", "Encontrar al gato Tora", MissionRank.D, 100, "El gato de la esposa del Feudal se ha perdido de nuevo.")
)
mission_board.add_mission(
    Mission("M02", "Proteger al constructor de puentes", MissionRank.C, 500, "Escolta a Tazuna a la Tierra de las Olas.")
)
mission_board.add_mission(
    Mission("M03", "Infiltrarse en la base Akatsuki", MissionRank.S, 10000, "Misión de alto riesgo de espionaje y sabotaje.")
)
print("-" * 25)

# 3. Asignamos misiones al ninja y vemos el resultado
print("\n--- Asignando Misiones ---")

# Intento 1: Misión de Rango D (Debería poder)
resultado1 = mission_board.assign(ninja_naruto, "M01")
print(resultado1)

# Intento 2: Misión de Rango C (Debería poder)
resultado2 = mission_board.assign(ninja_naruto, "M02")
print(resultado2)

# Intento 3: Misión de Rango S (No debería poder)
resultado3 = mission_board.assign(ninja_naruto, "M03")
print(resultado3)

print("-" * 25)