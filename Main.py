# main.py
from FactoryAbstractNaruto import KonohaFactory, SunaFactory, KiriFactory
from MissionSystem import Mission, MissionRank
from Visitor import JSONExportVisitor, export_all

def main():
    konoha_factory = KonohaFactory()
    suna_factory = SunaFactory()
    kiri_factory = KiriFactory()

    naruto = konoha_factory.createNinja()
    gaara = suna_factory.createNinja()
    zabuza = kiri_factory.createNinja()

    ninjas = [naruto, gaara, zabuza]

    # Crear misiones
    m1 = Mission("M001", "Proteger al Puente", MissionRank.C, 500, "Defender al constructor de un puente.")
    m2 = Mission("M002", "Capturar espía", MissionRank.A, 1200, "Atrapar al espía en territorio enemigo.")
    m3 = Mission("M003", "Defender Konoha", MissionRank.S, 5000, "Proteger la aldea de un ataque enemigo.")

    missions = [m1, m2, m3]

    # Exportar en JSON
    json_exporter = JSONExportVisitor()
    reporte_json = export_all(json_exporter, ninjas, missions)

    with open("reporte.json", "w", encoding="utf-8") as f:
        f.write(reporte_json)

    print("Archivo generado")
    print("Ninjas exportados:", [type(n).__name__ for n in ninjas])
    print("Misiones exportadas:", [m.title for m in missions])


if __name__ == "__main__":
    main()

