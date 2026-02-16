import type { Vegetable } from '../api/types';

interface Props {
  vegetable: Vegetable;
  quantity: number;
  onQuantityChange: (qty: number) => void;
}

export default function VegetableCard({ vegetable, quantity, onQuantityChange }: Props) {
  return (
    <div className="border border-gray-200 rounded-lg p-3 flex items-center gap-3 bg-white shadow-sm">
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
        <span className="w-8 text-center text-sm font-medium">{quantity}</span>
        <button
          onClick={() => onQuantityChange(quantity + 1)}
          className="w-7 h-7 rounded bg-green-100 hover:bg-green-200 text-green-700 flex items-center justify-center font-bold"
        >
          +
        </button>
      </div>
    </div>
  );
}
