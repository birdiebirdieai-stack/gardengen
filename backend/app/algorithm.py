"""Garden placement algorithm — row-based layout with companion planting."""

from itertools import permutations
from sqlalchemy.orm import Session

from .models import Association, Vegetable
from .schemas import GenerateRequest, GenerateResponse, PlacedVegetable


def generate_plan(req: GenerateRequest, db: Session) -> GenerateResponse:
    W = req.width_cm // 5   # grid width in 5cm cells
    H = req.height_cm // 5  # grid height in 5cm cells

    # Load vegetables
    veg_map: dict[int, Vegetable] = {}
    for item in req.items:
        v = db.get(Vegetable, item.vegetable_id)
        if v:
            veg_map[item.vegetable_id] = v

    # Load association scores
    assoc_scores: dict[tuple[int, int], int] = {}
    all_ids = list(veg_map.keys())
    for a in db.query(Association).filter(
        Association.vegetable_id_main.in_(all_ids),
        Association.vegetable_id_target.in_(all_ids),
    ).all():
        assoc_scores[(a.vegetable_id_main, a.vegetable_id_target)] = a.score

    # Build rows: one row per vegetable type, each row = full width of garden
    # Row height = plant height, items placed side by side along the row
    rows: list[dict] = []  # {veg_id, row_h, plants: [{x, y_offset, w, h}]}
    rejected: list[int] = []

    for item in req.items:
        v = veg_map.get(item.vegetable_id)
        if not v:
            continue
        pw, ph = v.grid_width, v.grid_height
        # How many fit per row of width W?
        per_row = W // pw if pw > 0 else 0
        if per_row == 0:
            rejected.extend([item.vegetable_id] * item.quantity)
            continue

        remaining = item.quantity
        while remaining > 0:
            n = min(remaining, per_row)
            plants = []
            for i in range(n):
                plants.append({"x_offset": i * pw, "w": pw, "h": ph})
            rows.append({
                "veg_id": item.vegetable_id,
                "row_h": ph,
                "plants": plants,
            })
            remaining -= n

    # Optimize row order using greedy nearest-neighbor on association scores
    if len(rows) > 1:
        rows = _optimize_row_order(rows, assoc_scores)

    # Place rows top to bottom
    placed: list[PlacedVegetable] = []
    cursor_y = 0
    for row in rows:
        if cursor_y + row["row_h"] > H:
            rejected.extend([row["veg_id"]] * len(row["plants"]))
            continue
        for p in row["plants"]:
            placed.append(PlacedVegetable(
                vegetable_id=row["veg_id"],
                x=p["x_offset"],
                y=cursor_y,
                w=p["w"],
                h=p["h"],
            ))
        cursor_y += row["row_h"]

    # Compute global score between adjacent rows
    global_score = _compute_global_score(placed, assoc_scores)

    return GenerateResponse(placed=placed, rejected=rejected, global_score=global_score)


def _optimize_row_order(
    rows: list[dict],
    assoc_scores: dict[tuple[int, int], int],
) -> list[dict]:
    """Greedy nearest-neighbor: pick the next row that has the best
    association score with the current row. For small counts (<= 8),
    try all permutations."""
    n = len(rows)

    def pair_score(a: dict, b: dict) -> int:
        return assoc_scores.get((a["veg_id"], b["veg_id"]), 0)

    def total_score(order: list[int]) -> int:
        return sum(pair_score(rows[order[i]], rows[order[i + 1]]) for i in range(len(order) - 1))

    if n <= 8:
        # Brute force best permutation
        best_order = list(range(n))
        best = total_score(best_order)
        for perm in permutations(range(n)):
            s = total_score(list(perm))
            if s > best:
                best = s
                best_order = list(perm)
        return [rows[i] for i in best_order]

    # Greedy for larger sets
    remaining = set(range(n))
    # Start with the row that has the most associations
    current = max(remaining, key=lambda i: sum(
        abs(assoc_scores.get((rows[i]["veg_id"], rows[j]["veg_id"]), 0))
        for j in remaining if j != i
    ))
    order = [current]
    remaining.remove(current)

    while remaining:
        best_next = max(remaining, key=lambda j: pair_score(rows[current], rows[j]))
        order.append(best_next)
        remaining.remove(best_next)
        current = best_next

    return [rows[i] for i in order]


def _compute_global_score(
    placed: list[PlacedVegetable],
    assoc_scores: dict[tuple[int, int], int],
) -> float:
    """Sum association scores between all adjacent placed vegetables."""
    total = 0.0
    seen: set[tuple[int, int]] = set()
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            if _are_adjacent(placed[i], placed[j]):
                pair = (min(i, j), max(i, j))
                if pair not in seen:
                    seen.add(pair)
                    s = assoc_scores.get(
                        (placed[i].vegetable_id, placed[j].vegetable_id), 0
                    )
                    total += s
    return total


def _are_adjacent(a: PlacedVegetable, b: PlacedVegetable) -> bool:
    gap_x = max(0, max(a.x, b.x) - min(a.x + a.w, b.x + b.w))
    gap_y = max(0, max(a.y, b.y) - min(a.y + a.h, b.y + b.h))
    return gap_x <= 1 and gap_y <= 1
