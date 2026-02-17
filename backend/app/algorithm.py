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
                plants.append({
                    "veg_id": item.vegetable_id,
                    "x_offset": i * pw,
                    "w": pw,
                    "h": ph
                })
            rows.append({
                "veg_id": item.vegetable_id,
                "row_h": ph,
                "plants": plants,
            })
            remaining -= n

    # Optimize row order using greedy nearest-neighbor on association scores.
    # We group rows by vegetable ID first to keep same vegetables together.
    if len(rows) > 1:
        # Group rows by vegetable type
        groups = {}
        for r in rows:
            groups.setdefault(r["veg_id"], []).append(r)

        # Create representative rows for optimization (use the first row of each group)
        # We wrap them to preserve the group reference
        meta_rows = []
        for vid, grouped_rows in groups.items():
            rep = grouped_rows[0].copy()
            rep["_original_group"] = grouped_rows
            meta_rows.append(rep)

        # Optimize order of groups
        optimized_meta = _optimize_row_order(meta_rows, assoc_scores)

        # Flatten back to rows
        rows = []
        for meta in optimized_meta:
            rows.extend(meta["_original_group"])

    # Calculate total height of the layout
    total_height = sum(r["row_h"] for r in rows)

    # Fill gaps in rows with vegetables from other rows ONLY if the layout overflows the garden height.
    # This prevents "agglutination" when there is plenty of space.
    # We now also allow filling from ANY row to optimize space (bidirectional compaction).
    if total_height > H:
        _fill_gaps(rows, W, assoc_scores)

    # Remove empty rows (in case all items were moved)
    rows = [r for r in rows if r["plants"]]

    # Place rows top to bottom
    placed: list[PlacedVegetable] = []
    cursor_y = 0
    for row in rows:
        if cursor_y + row["row_h"] > H:
            rejected.extend([row["veg_id"]] * len(row["plants"]))
            continue
        for p in row["plants"]:
            placed.append(PlacedVegetable(
                vegetable_id=p["veg_id"],
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


def _fill_gaps(
    rows: list[dict],
    W: int,
    assoc_scores: dict[tuple[int, int], int],
) -> None:
    """Try to fill gaps at the end of rows with vegetables from other rows,
    prioritizing non-negative associations and fitting dimensions.
    Iterates through all possible source rows to maximize compaction."""
    # Iterate through rows top to bottom
    for i in range(len(rows)):
        target_row = rows[i]

        # Skip if target row is empty (it will be removed, preserving vertical space)
        if not target_row["plants"]:
            continue

        while True:
            # Calculate current gap
            used_width = 0
            if target_row["plants"]:
                last_plant = target_row["plants"][-1]
                used_width = last_plant["x_offset"] + last_plant["w"]

            gap = W - used_width
            if gap <= 0:
                break

            # Identify potential source rows
            potential_sources = []
            for j in range(len(rows)):
                if i == j:
                    continue
                if not rows[j]["plants"]:
                    continue

                # Check if the row has a representative plant that fits
                candidate_plant = rows[j]["plants"][-1]
                if candidate_plant["w"] <= gap and candidate_plant["h"] <= target_row["row_h"]:
                    potential_sources.append(j)

            # Sort sources:
            # 1. Height Ascending (Prioritize emptying small rows to save vertical space)
            # 2. Index Descending (Prioritize bottom rows to avoid rejection)
            potential_sources.sort(key=lambda idx: (rows[idx]["row_h"], -idx))

            candidate_found = False

            for j in potential_sources:
                source_row = rows[j]

                # We try to take the last plant
                for k in range(len(source_row["plants"]) - 1, -1, -1):
                    plant = source_row["plants"][k]

                    # 1. Check dimensions
                    if plant["w"] > gap:
                        continue
                    if plant["h"] > target_row["row_h"]:
                        continue

                    # Avoid moving a plant back to its "home" row type from a "host" row,
                    # as this usually increases vertical space usage (un-hiding the plant).
                    # We allow merging two rows of same type (Home -> Home).
                    if plant["veg_id"] == target_row["veg_id"] and plant["veg_id"] != source_row["veg_id"]:
                        continue

                    # 2. Check associations
                    # Horizontal: Check all neighbors within interaction distance (gap <= 1)
                    valid_horizontal = True
                    for placed_p in reversed(target_row["plants"]):
                        dist = used_width - (placed_p["x_offset"] + placed_p["w"])
                        if dist > 1:
                            break  # Too far, no more interactions

                        score = assoc_scores.get((placed_p["veg_id"], plant["veg_id"]), 0)
                        if score < 0:
                            valid_horizontal = False
                            break

                    if not valid_horizontal:
                        continue

                    # Vertical: Neighbor below
                    vertical_conflict = False
                    for r_idx in range(i + 1, len(rows)):
                        neighbor_row = rows[r_idx]
                        if not neighbor_row["plants"]:
                            continue

                        # Check all plants in that row for overlap and conflict
                        for neighbor_p in neighbor_row["plants"]:
                            p_x, p_w = neighbor_p["x_offset"], neighbor_p["w"]
                            cand_x, cand_w = used_width, plant["w"]

                            gap_x = max(0, max(p_x, cand_x) - min(p_x + p_w, cand_x + cand_w))
                            if gap_x <= 1:
                                score = assoc_scores.get((plant["veg_id"], neighbor_p["veg_id"]), 0)
                                if score < 0:
                                    vertical_conflict = True
                                    break
                        # Only check the immediate next non-empty row
                        break

                    if vertical_conflict:
                        continue

                    # Vertical: Neighbor above
                    vertical_conflict = False
                    for r_idx in range(i - 1, -1, -1):
                        neighbor_row = rows[r_idx]
                        if not neighbor_row["plants"]:
                            continue

                        # Check all plants in that row for overlap and conflict
                        for neighbor_p in neighbor_row["plants"]:
                            p_x, p_w = neighbor_p["x_offset"], neighbor_p["w"]
                            cand_x, cand_w = used_width, plant["w"]

                            gap_x = max(0, max(p_x, cand_x) - min(p_x + p_w, cand_x + cand_w))
                            if gap_x <= 1:
                                score = assoc_scores.get((plant["veg_id"], neighbor_p["veg_id"]), 0)
                                if score < 0:
                                    vertical_conflict = True
                                    break
                        # Only check the immediate prev non-empty row
                        break

                    if vertical_conflict:
                        continue

                    # Found a candidate! Move it.
                    moved_plant = source_row["plants"].pop(k)

                    # Update its position
                    moved_plant["x_offset"] = used_width

                    # Add to target
                    target_row["plants"].append(moved_plant)

                    candidate_found = True
                    break  # Break inner loop (plants)

                if candidate_found:
                    break  # Break outer loop (source rows) to recalculate gap

            if not candidate_found:
                break  # No more candidates fit in this gap
