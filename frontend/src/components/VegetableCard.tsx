import type { Vegetable } from '../api/types';

interface Props {
  vegetable: Vegetable;
  quantity: number;
  onQuantityChange: (qty: number) => void;
  fullRow: boolean;
  onFullRowChange: (enabled: boolean) => void;
  perRow: number; // how many plants fit in one full row
}

export default function VegetableCard({
  vegetable, quantity, onQuantityChange, fullRow, onFullRowChange, perRow,
}: Props) {
  const label = fullRow ? 'lignes' : 'plants';
  const displayCount = fullRow ? `${quantity} ${label} (${quantity * perRow} plants)` : null;

  return (
    <div className="border border-gray-200 rounded-lg p-3 bg-white shadow-sm">
      <div className="flex items-center gap-3">
        <div
          className="w-10 h-10 rounded-lg shrink-0"
          style={{ backgroundColor: vegetable.color }}
        />
        <div className="flex-1 min-w-0">
          <p className="font-medium text-sm truncate">{vegetable.name}</p>
          <p className="text-xs text-gray-500">
            {vegetable.grid_width * 5}x{vegetable.grid_height * 5} cm
          </p>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => onQuantityChange(quantity - 1)}
            className="w-7 h-7 rounded bg-gray-100 hover:bg-gray-200 text-gray-700 flex items-center justify-center font-bold"
          >
            -
          </button>
          <input
            type="number"
            min={0}
            max={100}
            value={quantity}
            onChange={(e) => onQuantityChange(Math.max(0, Math.min(100, parseInt(e.target.value) || 0)))}
            className="w-10 text-center text-sm font-medium bg-transparent border-b border-transparent focus:border-gray-400 focus:outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />
          <button
            onClick={() => onQuantityChange(quantity + 1)}
            className="w-7 h-7 rounded bg-green-100 hover:bg-green-200 text-green-700 flex items-center justify-center font-bold"
          >
            +
          </button>
        </div>
      </div>
      {quantity > 0 && (
        <div className="mt-2 flex items-center justify-between">
          <label className="flex items-center gap-1.5 cursor-pointer">
            <input
              type="checkbox"
              checked={fullRow}
              onChange={(e) => onFullRowChange(e.target.checked)}
              className="w-3.5 h-3.5 rounded accent-green-600"
            />
            <span className="text-xs text-gray-500">Ligne complète</span>
          </label>
          {fullRow && displayCount && (
            <span className="text-xs text-gray-400">{displayCount}</span>
          )}
        </div>
      )}
    </div>
  );
}
