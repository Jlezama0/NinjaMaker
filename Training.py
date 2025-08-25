# Training.py

from NinjaBuilder import FinalNinja, Stats, Director, NinjaBuilder
from FactoryAbstractNaruto import KonohaFactory

class TrainingSystem:
    """
    Gestiona el entrenamiento de los ninjas, permitiendo mejorar sus estadísticas.
    """

    def train_ninja(self, ninja: FinalNinja, attribute: str, points_to_add: int):
        """
        Aumenta un atributo específico de un ninja.

        Args:
            ninja (FinalNinja): El objeto ninja que va a entrenar.
            attribute (str): El nombre del atributo a mejorar (ej. "Ninjutsu", "Taijutsu").
            points_to_add (int): La cantidad de puntos que se sumarán al atributo.
        """
        # Verificamos si el atributo existe en las estadísticas del ninja para evitar errores.
        if hasattr(ninja.stats, attribute):
            # Obtenemos el valor actual del atributo usando getattr()
            current_value = getattr(ninja.stats, attribute)
            
            # Calculamos el nuevo valor
            new_value = current_value + points_to_add
            
            # Asignamos el nuevo valor al atributo usando setattr()
            setattr(ninja.stats, attribute, new_value)
            
            print(f"✅ ¡Entrenamiento completado! {ninja.name} ha mejorado su {attribute}.")
            print(f"   Estadística anterior: {current_value} -> Nueva estadística: {new_value}\n")
        else:
            # Si el atributo no existe, mostramos un mensaje de error.
            print(f"❌ Error: El atributo '{attribute}' no es una estadística entrenable.\n")

# --- EJEMPLO DE USO ---

# 1. Reutilizamos el código que ya tenías para crear un ninja
factory = KonohaFactory()
director = Director(factory)
builder = NinjaBuilder()

stats_iniciales = Stats()
stats_iniciales.Ninjutsu = 80
stats_iniciales.Taijutsu = 50
stats_iniciales.Willpower = 95

# Creamos a nuestro ninja final
ninja_naruto = director.makeNinja(
    builder,
    name="Naruto",
    rank="Genin",
    chakra=1000,
    clan="Uzumaki",
    styleFight="Multi-clones",
    weapon="Kunai",
    stats=stats_iniciales
)

print("--- Creación del Ninja ---")
print(ninja_naruto)
print("-" * 25)

# 2. Creamos una instancia del sistema de entrenamiento
dojo_entrenamiento = TrainingSystem()

print("\n--- Inicio del Entrenamiento ---")

# 3. Entrenamos al ninja en diferentes estadísticas
print(f"Entrenando a {ninja_naruto.name}...\n")

# Entrenar una estadística que ya tiene puntos
dojo_entrenamiento.train_ninja(ninja_naruto, "Ninjutsu", 10)

# Entrenar una estadística que está en 0
dojo_entrenamiento.train_ninja(ninja_naruto, "Genjutsu", 5)

# Intentar entrenar una estadística que no existe
dojo_entrenamiento.train_ninja(ninja_naruto, "Cocina", 20)

# Entrenar Taijutsu
dojo_entrenamiento.train_ninja(ninja_naruto, "Taijutsu", 15)


print("--- Estado Final del Ninja ---")
print(ninja_naruto)
print("-" * 25)