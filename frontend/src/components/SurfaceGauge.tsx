interface Props {
  usedCells: number;
  totalCells: number;
}

export default function SurfaceGauge({ usedCells, totalCells }: Props) {
  const ratio = totalCells > 0 ? usedCells / totalCells : 0;
  const pct = Math.min(ratio * 100, 100);

  let color = 'bg-green-500';
  if (ratio > 0.9) color = 'bg-red-500';
  else if (ratio > 0.7) color = 'bg-yellow-500';

  return (
    <div className="w-full">
      <div className="flex justify-between text-sm text-gray-600 mb-1">
        <span>Surface utilisee</span>
        <span>{Math.round(pct)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-300 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs text-gray-500 mt-1">
        {((usedCells * 25) / 10000).toLocaleString(undefined, { maximumFractionDigits: 2 })} m² / {((totalCells * 25) / 10000).toLocaleString(undefined, { maximumFractionDigits: 2 })} m²
      </p>
    </div>
  );
}
