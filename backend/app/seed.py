"""Seed database with 30 vegetables and companion planting associations."""

from .database import init_db, SessionLocal
from .models import Vegetable, Association


VEGETABLES = [
    # name, slug, grid_w, grid_h (in 5cm cells), color
    ("Tomate", "tomate", 9, 9, "#ef4444"),
    ("Courgette", "courgette", 16, 16, "#65a30d"),
    ("Concombre", "concombre", 10, 10, "#4ade80"),
    ("Aubergine", "aubergine", 10, 10, "#7c3aed"),
    ("Poivron", "poivron", 8, 8, "#f97316"),
    ("Piment", "piment", 7, 7, "#dc2626"),
    ("Carotte", "carotte", 1, 1, "#f97316"),
    ("Radis", "radis", 1, 1, "#f43f5e"),
    ("Navet", "navet", 2, 2, "#fde68a"),
    ("Betterave", "betterave", 2, 2, "#991b1b"),
    ("Oignon", "oignon", 2, 2, "#d97706"),
    ("Ail", "ail", 2, 2, "#fef9c3"),
    ("Poireau", "poireau", 2, 2, "#16a34a"),
    ("Échalote", "echalote", 2, 2, "#b45309"),
    ("Laitue", "laitue", 4, 4, "#86efac"),
    ("Épinard", "epinard", 3, 3, "#166534"),
    ("Chou", "chou", 8, 8, "#22d3ee"),
    ("Brocoli", "brocoli", 8, 8, "#059669"),
    ("Chou-fleur", "chou-fleur", 8, 8, "#f5f5f4"),
    ("Haricot vert", "haricot-vert", 3, 3, "#4ade80"),
    ("Petit pois", "petit-pois", 3, 3, "#a3e635"),
    ("Basilic", "basilic", 4, 4, "#15803d"),
    ("Persil", "persil", 3, 3, "#16a34a"),
    ("Ciboulette", "ciboulette", 2, 2, "#65a30d"),
    ("Menthe", "menthe", 6, 6, "#34d399"),
    ("Thym", "thym", 4, 4, "#a16207"),
    ("Romarin", "romarin", 6, 6, "#6366f1"),
    ("Céleri", "celeri", 5, 5, "#a3e635"),
    ("Pomme de terre", "pomme-de-terre", 6, 6, "#a8a29e"),
    ("Fraise", "fraise", 4, 4, "#e11d48"),
]

# (slug_main, slug_target, score, reason)
ASSOCIATIONS = [
    ("tomate", "basilic", 40, "Le basilic repousse les pucerons et améliore la saveur"),
    ("tomate", "carotte", 20, "Bonne cohabitation, la tomate protège la carotte"),
    ("tomate", "persil", 25, "Le persil stimule la croissance de la tomate"),
    ("tomate", "oignon", 15, "L'oignon éloigne certains parasites"),
    ("tomate", "poireau", 15, "Association bénéfique classique"),
    ("tomate", "laitue", 15, "La tomate offre de l'ombre à la laitue"),
    ("tomate", "celeri", 20, "Association mutuellement bénéfique"),
    ("tomate", "pomme-de-terre", -40, "Même famille, maladies communes (mildiou)"),
    ("tomate", "chou", -30, "Mauvais voisinage, croissance réduite"),
    ("tomate", "concombre", -15, "Compétition en nutriments"),
    ("carotte", "oignon", 35, "L'oignon repousse la mouche de la carotte"),
    ("carotte", "poireau", 35, "Association emblématique du compagnonnage"),
    ("carotte", "ail", 25, "L'ail protège la carotte des parasites"),
    ("carotte", "radis", 20, "Le radis marque les rangs et ameublit le sol"),
    ("carotte", "laitue", 15, "Bonne cohabitation au potager"),
    ("carotte", "ciboulette", 20, "La ciboulette éloigne la mouche de la carotte"),
    ("carotte", "petit-pois", 15, "Les pois fixent l'azote bénéfique"),
    ("courgette", "haricot-vert", 30, "Les haricots fixent l'azote pour la courgette"),
    ("courgette", "petit-pois", 25, "Apport d'azote bénéfique"),
    ("courgette", "radis", 15, "Le radis est un bon compagnon de la courgette"),
    ("courgette", "menthe", 20, "La menthe repousse les pucerons"),
    ("courgette", "pomme-de-terre", -20, "Compétition en nutriments"),
    ("concombre", "haricot-vert", 25, "Association bénéfique (azote)"),
    ("concombre", "petit-pois", 25, "Les pois enrichissent le sol"),
    ("concombre", "laitue", 15, "Bonne cohabitation"),
    ("concombre", "basilic", 20, "Le basilic repousse les insectes"),
    ("concombre", "pomme-de-terre", -25, "Mauvais voisinage"),
    ("aubergine", "haricot-vert", 25, "Association classique bénéfique"),
    ("aubergine", "basilic", 20, "Le basilic éloigne les pucerons"),
    ("aubergine", "thym", 15, "Aromatique protectrice"),
    ("poivron", "basilic", 25, "Éloigne les parasites, améliore la saveur"),
    ("poivron", "carotte", 15, "Bonne association"),
    ("poivron", "aubergine", 10, "Même famille mais bonne cohabitation"),
    ("chou", "celeri", 30, "Le céleri éloigne la piéride du chou"),
    ("chou", "oignon", 20, "L'oignon protège le chou"),
    ("chou", "betterave", 15, "Association bénéfique"),
    ("chou", "haricot-vert", 15, "Bonne association"),
    ("chou", "epinard", 15, "Bon voisinage"),
    ("chou", "fraise", -30, "Mauvais voisinage"),
    ("brocoli", "celeri", 25, "Protection contre la piéride"),
    ("brocoli", "oignon", 20, "L'oignon éloigne les parasites"),
    ("brocoli", "betterave", 15, "Association favorable"),
    ("chou-fleur", "celeri", 25, "Le céleri protège le chou-fleur"),
    ("chou-fleur", "haricot-vert", 15, "Les haricots enrichissent le sol"),
    ("laitue", "radis", 20, "Très bonne association classique"),
    ("laitue", "fraise", 20, "Bonne cohabitation"),
    ("laitue", "ciboulette", 15, "La ciboulette éloigne les pucerons"),
    ("laitue", "epinard", 10, "Association possible"),
    ("haricot-vert", "pomme-de-terre", 20, "Les haricots enrichissent le sol"),
    ("haricot-vert", "celeri", 15, "Bonne association"),
    ("haricot-vert", "fraise", 15, "Association bénéfique"),
    ("haricot-vert", "oignon", -30, "Les alliacées inhibent les légumineuses"),
    ("haricot-vert", "ail", -30, "Les alliacées inhibent les légumineuses"),
    ("petit-pois", "oignon", -30, "Les alliacées inhibent les légumineuses"),
    ("petit-pois", "ail", -30, "Les alliacées inhibent les légumineuses"),
    ("petit-pois", "radis", 20, "Le radis ameublit le sol"),
    ("petit-pois", "carotte", 15, "L'azote bénéficie à la carotte"),
    ("pomme-de-terre", "ail", 20, "L'ail protège des maladies"),
    ("pomme-de-terre", "oignon", 15, "Protection contre les parasites"),
    ("fraise", "ail", 25, "L'ail protège contre les maladies fongiques"),
    ("fraise", "oignon", 20, "L'oignon éloigne les parasites de la fraise"),
    ("fraise", "thym", 20, "Le thym repousse les parasites"),
    ("fraise", "epinard", 15, "Bon voisinage"),
    ("oignon", "betterave", 15, "Bonne association classique"),
    ("betterave", "laitue", 15, "Cohabitation bénéfique"),
    ("epinard", "radis", 15, "Croissance rapide des radis avant l'épinard"),
    ("epinard", "fraise", 15, "Bon voisinage"),
    ("basilic", "persil", 10, "Aromatiques complémentaires"),
    ("thym", "romarin", 20, "Même besoins, bonne cohabitation"),
    ("menthe", "chou", 20, "La menthe repousse la piéride"),
]


def run_seed():
    init_db()
    db = SessionLocal()
    try:
        # Seed vegetables
        slug_to_id: dict[str, int] = {}
        for name, slug, gw, gh, color in VEGETABLES:
            existing = db.query(Vegetable).filter_by(slug=slug).first()
            if existing:
                slug_to_id[slug] = existing.id
                continue
            v = Vegetable(name=name, slug=slug, grid_width=gw, grid_height=gh, color=color)
            db.add(v)
            db.flush()
            slug_to_id[slug] = v.id

        # Seed associations (bidirectional)
        for slug_main, slug_target, score, reason in ASSOCIATIONS:
            id_main = slug_to_id[slug_main]
            id_target = slug_to_id[slug_target]
            existing = db.query(Association).filter_by(
                vegetable_id_main=id_main, vegetable_id_target=id_target
            ).first()
            if not existing:
                db.add(Association(
                    vegetable_id_main=id_main,
                    vegetable_id_target=id_target,
                    score=score,
                    reason=reason,
                ))
            # reverse direction
            existing_rev = db.query(Association).filter_by(
                vegetable_id_main=id_target, vegetable_id_target=id_main
            ).first()
            if not existing_rev:
                db.add(Association(
                    vegetable_id_main=id_target,
                    vegetable_id_target=id_main,
                    score=score,
                    reason=reason,
                ))

        db.commit()
        print(f"Seeded {len(VEGETABLES)} vegetables and {len(ASSOCIATIONS)} associations (bidirectional).")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
