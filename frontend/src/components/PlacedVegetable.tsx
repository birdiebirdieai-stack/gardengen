import type { PlacedVegetable as PlacedVeg } from '../api/types';
import type { Vegetable } from '../api/types';

interface Props {
  placed: PlacedVeg;
  vegetable: Vegetable | undefined;
  cellSize: number;
  selected: boolean;
  onClick: () => void;
}

export default function PlacedVegetableComp({ placed, vegetable, cellSize, selected, onClick }: Props) {
  if (!vegetable) return null;

  return (
    <div
      onClick={onClick}
      className={`absolute cursor-pointer flex items-center justify-center text-xs font-medium text-white rounded border-2 transition-all ${
        selected ? 'border-yellow-400 shadow-lg z-10 scale-105' : 'border-white/50 hover:border-white'
      }`}
      style={{
        left: placed.x * cellSize,
        top: placed.y * cellSize,
        width: placed.w * cellSize,
        height: placed.h * cellSize,
        backgroundColor: vegetable.color,
      }}
      title={vegetable.name}
    >
      {placed.w * cellSize > 30 && placed.h * cellSize > 20 && (
        <span className="truncate px-1">{vegetable.name}</span>
      )}
    </div>
  );
}
