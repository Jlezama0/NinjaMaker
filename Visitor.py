# Visitor.py
from abc import ABC, abstractmethod
import json
from typing import Any, List

class Visitor(ABC):
    @abstractmethod
    def visit_ninja(self, ninja: Any) -> None: ...
    @abstractmethod
    def visit_mission(self, mission: Any) -> None: ...

    def reset(self):
        pass

    def result(self):
        return None


class JSONExportVisitor(Visitor):
    def __init__(self):
        self.reset()

    def reset(self):
        self._data = {"ninjas": [], "missions": []}

    def visit_ninja(self, ninja: Any) -> None:
        # --- Compatibilidad con FinalNinja (atributos) y BaseNinja (métodos) ---
        name = getattr(ninja, "name", None) or getattr(ninja, "get_name", lambda: None)()
        rank = getattr(ninja, "rank", None) or getattr(ninja, "get_rank", lambda: None)()
        stats = getattr(ninja, "stats", None) or getattr(ninja, "get_stats", lambda: None)()

        jutsus = []
        if hasattr(ninja, "get_jutsus"):
            jutsus = [{
                "name": j.get_name(),
                "description": j.get_description(),
                "chakra_cost": j.get_chakra_cost()
            } for j in ninja.get_jutsus()]
        elif hasattr(ninja, "jutsus"):
            jutsus = ninja.jutsus

        village = type(ninja).__name__.replace("Ninja", "")
        self._data["ninjas"].append({
            "name": name,
            "village": village,
            "rank": rank if isinstance(rank, str) else getattr(rank, "value", None),
            "stats": {
                "attack": getattr(stats, "Ninjutsu", getattr(stats, "attack", 0)),
                "defense": getattr(stats, "Willpower", getattr(stats, "defense", 0)),
                "chakra": getattr(stats, "chakra", 0)
            },
            "jutsus": jutsus
        })

    def visit_mission(self, mission: Any) -> None:
        self._data["missions"].append({
            "id": mission.id,
            "title": mission.title,
            "required_rank": mission.required_rank.name if hasattr(mission.required_rank, "name") else mission.required_rank,
            "reward": mission.reward,
            "description": mission.description
        })

    def result(self):
        return json.dumps(self._data, ensure_ascii=False, indent=2)


def export_all(visitor: Visitor, ninjas: List[Any], missions: List[Any]) -> str:
    visitor.reset()
    for n in ninjas:
        n.accept(visitor)
    for m in missions:
        m.accept(visitor)
    return visitor.result()
