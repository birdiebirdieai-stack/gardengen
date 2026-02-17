# GardenGen

Planificateur intelligent de potager avec optimisation spatiale et associations de plantes.

Intelligent garden planner with spatial optimization and companion planting.

---

## Fonctionnalites / Features

- **Placement 2D intelligent** — Algorithme de placement par blocs sur grille 2D, les legumes sont regroupes et l'espace est utilise efficacement
- **Associations de plantes** — Respect des bonnes et mauvaises associations entre legumes (compagnonnage)
- **Ligne complete** — Option pour planter des lignes entieres d'un legume (ex: carottes, radis)
- **Score global** — Visualisation du score de compatibilite du potager
- **Interface intuitive** — Selection des legumes, dimensions du potager, visualisation du plan genere

---

- **Smart 2D placement** — Block-based grid algorithm, vegetables are grouped and space is used efficiently
- **Companion planting** — Respects good and bad plant associations
- **Full row mode** — Option to plant full rows of a vegetable (e.g. carrots, radishes)
- **Global score** — Compatibility score visualization for the garden
- **Intuitive UI** — Vegetable selection, garden dimensions, generated plan visualization

## Stack technique / Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 19, TypeScript 5.9, Vite 7, Tailwind CSS 4, Zustand 5 |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| Base de donnees | SQLite |

## Installation

### Prerequisites

- Node.js 20+
- Python 3.11+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

La base de donnees est creee et initialisee automatiquement au demarrage (30 legumes, 136 associations).

The database is created and seeded automatically on startup (30 vegetables, 136 associations).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend est accessible sur http://localhost:5173 et communique avec le backend sur le port 8000.

The frontend is available at http://localhost:5173 and communicates with the backend on port 8000.

## Utilisation / Usage

1. **Dimensions** — Definir la taille du potager (largeur x hauteur en cm) / Set garden size (width x height in cm)
2. **Selection** — Choisir les legumes et leurs quantites, activer le mode "ligne complete" si besoin / Pick vegetables and quantities, enable "full row" mode if needed
3. **Generation** — L'algorithme place les legumes de maniere optimale sur la grille 2D / The algorithm places vegetables optimally on the 2D grid
4. **Visualisation** — Consulter le plan, le score de compatibilite et les legumes non places / View the plan, compatibility score and rejected vegetables

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/vegetables` | GET | Liste des legumes / List vegetables |
| `/api/vegetables` | POST | Creer un legume / Create vegetable |
| `/api/associations` | GET | Liste des associations / List associations |
| `/api/generate` | POST | Generer un plan de potager / Generate garden plan |

## Algorithme / Algorithm

L'algorithme utilise un placement 2D par blocs :

1. Chaque type de legume forme un bloc rectangulaire compact
2. Les blocs sont places par ordre de taille decroissante
3. L'ordre de placement suit les scores d'association (amis ensemble, ennemis separes)
4. Plusieurs dispositions sont testees pour chaque bloc (large, carre, etroit)
5. Les adjacences ennemies sont penalisees mais n'empechent pas le placement

---

The algorithm uses 2D block-based placement:

1. Each vegetable type forms a compact rectangular block
2. Blocks are placed largest-first
3. Placement order follows association scores (friends together, enemies apart)
4. Multiple arrangements are tried per block (wide, square, narrow)
5. Enemy adjacencies are penalized but don't prevent placement

## Licence

MIT
