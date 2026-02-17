"""Garden placement algorithm — 2D block-based layout with companion planting."""

import math
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

    # Build vegetable blocks: each vegetable type = one rectangular block
    blocks: list[dict] = []
    for item in req.items:
        v = veg_map.get(item.vegetable_id)
        if not v:
            continue
        pw, ph = v.grid_width, v.grid_height
        if pw > W or ph > H:
            continue
        qty = item.quantity
        per_row = W // pw
        if per_row == 0:
            continue

        # Calculate block dimensions
        rows_needed = math.ceil(qty / per_row)
        last_row_count = qty - (rows_needed - 1) * per_row
        block_w = min(qty, per_row) * pw
        block_h = rows_needed * ph

        blocks.append({
            "veg_id": item.vegetable_id,
            "qty": qty,
            "pw": pw, "ph": ph,
            "per_row": per_row,
            "block_w": block_w,
            "block_h": block_h,
            "area": block_w * block_h,
        })

    # Order blocks: largest first, then chain by best association score.
    # This ensures friendly vegetables are placed next to each other.
    blocks = _order_blocks_by_association(blocks, assoc_scores)

    # 2D occupancy grid: grid[y][x] = veg_id or 0 (free)
    grid: list[list[int]] = [[0] * W for _ in range(H)]

    placed: list[PlacedVegetable] = []
    rejected: list[int] = []

    for block in blocks:
        veg_id = block["veg_id"]
        pw, ph = block["pw"], block["ph"]
        qty = block["qty"]
        max_per_row = block["per_row"]

        # Try different block arrangements (varying columns per row)
        # from widest to narrowest
        placed_block = False
        for cols in range(min(qty, max_per_row), 0, -1):
            rows_needed = math.ceil(qty / cols)
            bw = cols * pw
            bh = rows_needed * ph

            pos = _find_block_position(grid, W, H, veg_id, bw, bh, assoc_scores)
            if pos is not None:
                bx, by = pos
                _place_block(grid, placed, bx, by, veg_id, pw, ph, cols, qty)
                placed_block = True
                break

        if placed_block:
            continue

        # No full block arrangement fits — try placing sub-groups
        remaining = qty
        while remaining > 0:
            placed_any = False

            # Try sub-groups from largest to smallest, with varying columns
            for sub_qty in range(remaining, 0, -1):
                found = False
                for cols in range(min(sub_qty, max_per_row), 0, -1):
                    sub_rows = math.ceil(sub_qty / cols)
                    sub_w = cols * pw
                    sub_h = sub_rows * ph

                    pos = _find_block_position(
                        grid, W, H, veg_id, sub_w, sub_h, assoc_scores
                    )
                    if pos is not None:
                        bx, by = pos
                        actual_placed = _place_block(
                            grid, placed, bx, by, veg_id, pw, ph, cols, sub_qty
                        )
                        remaining -= actual_placed
                        placed_any = True
                        found = True
                        break
                if found:
                    break

            if not placed_any:
                rejected.extend([veg_id] * remaining)
                break

    global_score = _compute_global_score(placed, assoc_scores)
    return GenerateResponse(placed=placed, rejected=rejected, global_score=global_score)


def _order_blocks_by_association(
    blocks: list[dict],
    assoc_scores: dict[tuple[int, int], int],
) -> list[dict]:
    """Order blocks so that friendly vegetables are placed consecutively.

    Start with the largest block, then greedily pick the next block with the
    best association score to the last placed one. This ensures friends end
    up as neighbors on the grid (since placement is top-left greedy).
    Enemies are naturally pushed apart in the sequence."""
    if len(blocks) <= 1:
        return blocks

    # Start with the largest block
    remaining = list(blocks)
    remaining.sort(key=lambda b: -b["area"])
    ordered = [remaining.pop(0)]

    while remaining:
        last_vid = ordered[-1]["veg_id"]
        # Pick the block with the best association to the last placed
        # Break ties by area descending (place big blocks first)
        best_idx = 0
        best_key = None
        for i, b in enumerate(remaining):
            score = assoc_scores.get((last_vid, b["veg_id"]), 0)
            key = (score, b["area"])
            if best_key is None or key > best_key:
                best_key = key
                best_idx = i
        ordered.append(remaining.pop(best_idx))

    return ordered


def _find_block_position(
    grid: list[list[int]],
    W: int, H: int,
    veg_id: int,
    block_w: int, block_h: int,
    assoc_scores: dict[tuple[int, int], int],
) -> tuple[int, int] | None:
    """Find the best position for a rectangular block on the grid.

    Strategy:
    1. Must not overlap existing plants
    2. Strongly prefer no enemies, but accept them as last resort
    3. Prefer positions adjacent to same vegetable (grouping)
    4. Prefer positions with good association scores
    5. Prefer top-left for compact layout
    """
    best_pos = None
    best_score = None

    for y in range(H - block_h + 1):
        for x in range(W - block_w + 1):
            if not _area_free(grid, x, y, block_w, block_h):
                continue

            neighbor_score, has_enemy, has_same = _evaluate_neighbors(
                grid, W, H, x, y, block_w, block_h, veg_id, assoc_scores
            )

            # Score: no_enemy > has_enemy, then grouping, then assoc, then top-left
            score = (not has_enemy, has_same, neighbor_score, -y, -x)

            if best_score is None or score > best_score:
                best_score = score
                best_pos = (x, y)

    return best_pos


def _place_block(
    grid: list[list[int]],
    placed: list[PlacedVegetable],
    bx: int, by: int,
    veg_id: int, pw: int, ph: int,
    per_row: int, qty: int,
) -> int:
    """Place plants in a rectangular block starting at (bx, by).
    Returns the number of plants actually placed."""
    count = 0
    row = 0
    col = 0
    for _ in range(qty):
        x = bx + col * pw
        y = by + row * ph

        # Mark grid
        for dy in range(ph):
            for dx in range(pw):
                grid[y + dy][x + dx] = veg_id

        placed.append(PlacedVegetable(
            vegetable_id=veg_id, x=x, y=y, w=pw, h=ph
        ))
        count += 1
        col += 1
        if col >= per_row:
            col = 0
            row += 1

    return count


def _area_free(grid: list[list[int]], x: int, y: int, w: int, h: int) -> bool:
    """Check if a rectangular area is entirely free on the grid."""
    for dy in range(h):
        row = grid[y + dy]
        for dx in range(w):
            if row[x + dx] != 0:
                return False
    return True


def _evaluate_neighbors(
    grid: list[list[int]],
    W: int, H: int,
    x: int, y: int, bw: int, bh: int,
    veg_id: int,
    assoc_scores: dict[tuple[int, int], int],
) -> tuple[int, bool, bool]:
    """Evaluate the neighborhood around a block position.

    Returns: (total_score, has_enemy, has_same_vegetable)
    Checks cells immediately adjacent to the block border.
    """
    total_score = 0
    has_enemy = False
    has_same = False
    checked_veg_ids: set[int] = set()

    # Scan the 1-cell border around the block
    for dy in range(-1, bh + 1):
        for dx in range(-1, bw + 1):
            # Skip interior
            if 0 <= dy < bh and 0 <= dx < bw:
                continue
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W:
                neighbor_id = grid[ny][nx]
                if neighbor_id != 0:
                    if neighbor_id == veg_id:
                        has_same = True
                    if neighbor_id not in checked_veg_ids:
                        checked_veg_ids.add(neighbor_id)
                        score = assoc_scores.get((veg_id, neighbor_id), 0)
                        total_score += score
                        if score < 0:
                            has_enemy = True

    return total_score, has_enemy, has_same


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
