import { useState, useRef, useEffect } from 'react';
import type { GenerateResponse, Vegetable, Association } from '../api/types';
import PlacedVegetableComp from './PlacedVegetable';

interface Props {
  result: GenerateResponse;
  vegetables: Vegetable[];
  associations: Association[];
  gridW: number;
  gridH: number;
}

export default function GardenGrid({ result, vegetables, associations, gridW, gridH }: Props) {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [zoom, setZoom] = useState(1);
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerWidth, setContainerWidth] = useState(0);

  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setContainerWidth(entry.contentRect.width);
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Dynamic cell size calculation based on container width
  // Fallback to 20 if containerWidth is 0 (initial render)
  // Ensure we don't divide by zero if gridW is somehow 0
  const baseSize = (containerWidth > 0 && gridW > 0) ? containerWidth / gridW : 20;
  const cellSize = baseSize * zoom;

  const totalW = gridW * cellSize;
  const totalH = gridH * cellSize;

  const selectedPlaced = selectedIdx !== null ? result.placed[selectedIdx] : null;
  const selectedVeg = selectedPlaced
    ? vegetables.find((v) => v.id === selectedPlaced.vegetable_id)
    : null;

  // Find neighbor associations for selected plant
  const neighborInfo: { name: string; score: number; reason: string }[] = [];
  if (selectedPlaced) {
    const vid = selectedPlaced.vegetable_id;
    // Find placed neighbors
    result.placed.forEach((p, i) => {
      if (i === selectedIdx) return;
      // Check adjacency (within 1 cell)
      const gapX = Math.max(0, Math.max(selectedPlaced.x, p.x) - Math.min(selectedPlaced.x + selectedPlaced.w, p.x + p.w));
      const gapY = Math.max(0, Math.max(selectedPlaced.y, p.y) - Math.min(selectedPlaced.y + selectedPlaced.h, p.y + p.h));
      if (gapX <= 1 && gapY <= 1) {
        const assoc = associations.find(
          (a) =>
            (a.vegetable_id_main === vid && a.vegetable_id_target === p.vegetable_id) ||
            (a.vegetable_id_main === p.vegetable_id && a.vegetable_id_target === vid)
        );
        const v = vegetables.find((v) => v.id === p.vegetable_id);
        neighborInfo.push({
          name: v?.name ?? `ID ${p.vegetable_id}`,
          score: assoc?.score ?? 0,
          reason: assoc?.reason ?? 'Pas d\'association connue',
        });
      }
    });
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <button
          onClick={() => setZoom((z) => Math.max(0.5, z - 0.25))}
          className="px-2 py-1 bg-gray-200 rounded text-sm hover:bg-gray-300"
        >
          -
        </button>
        <span className="text-sm text-gray-600">Zoom: {Math.round(zoom * 100)}%</span>
        <button
          onClick={() => setZoom((z) => Math.min(3, z + 0.25))}
          className="px-2 py-1 bg-gray-200 rounded text-sm hover:bg-gray-300"
        >
          +
        </button>
      </div>

      <div className="flex gap-4">
        <div
          ref={containerRef}
          className="overflow-auto border border-gray-300 rounded-lg bg-white flex-1"
          style={{ maxHeight: '70vh' }}
        >
          <div
            className="relative"
            style={{ width: totalW, height: totalH }}
            onClick={(e) => {
              if (e.target === e.currentTarget) setSelectedIdx(null);
            }}
          >
            {/* Grid lines */}
            <svg className="absolute inset-0 pointer-events-none" width={totalW} height={totalH}>
              {Array.from({ length: gridW + 1 }, (_, i) => (
                <line
                  key={`v${i}`}
                  x1={i * cellSize}
                  y1={0}
                  x2={i * cellSize}
                  y2={totalH}
                  stroke="#e5e7eb"
                  strokeWidth={i % 2 === 0 ? 0.5 : 0.25}
                />
              ))}
              {Array.from({ length: gridH + 1 }, (_, i) => (
                <line
                  key={`h${i}`}
                  x1={0}
                  y1={i * cellSize}
                  x2={totalW}
                  y2={i * cellSize}
                  stroke="#e5e7eb"
                  strokeWidth={i % 2 === 0 ? 0.5 : 0.25}
                />
              ))}
            </svg>

            {result.placed.map((p, i) => (
              <PlacedVegetableComp
                key={i}
                placed={p}
                vegetable={vegetables.find((v) => v.id === p.vegetable_id)}
                cellSize={cellSize}
                selected={selectedIdx === i}
                onClick={() => setSelectedIdx(selectedIdx === i ? null : i)}
              />
            ))}
          </div>
        </div>

        {/* Detail panel */}
        {selectedVeg && (
          <div className="w-64 shrink-0 bg-white border border-gray-200 rounded-lg p-4 self-start">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-6 h-6 rounded" style={{ backgroundColor: selectedVeg.color }} />
              <h3 className="font-bold">{selectedVeg.name}</h3>
            </div>
            <p className="text-xs text-gray-500 mb-3">
              Position : ({selectedPlaced!.x}, {selectedPlaced!.y}) —{' '}
              {selectedPlaced!.w * 5}x{selectedPlaced!.h * 5} cm
            </p>
            {neighborInfo.length > 0 ? (
              <div>
                <h4 className="text-sm font-medium mb-2">Voisins</h4>
                <ul className="space-y-2">
                  {neighborInfo.map((n, i) => (
                    <li key={i} className="text-sm">
                      <div className="flex items-center justify-between">
                        <span>{n.name}</span>
                        <span
                          className={`font-bold ${
                            n.score > 0
                              ? 'text-green-600'
                              : n.score < 0
                                ? 'text-red-600'
                                : 'text-gray-400'
                          }`}
                        >
                          {n.score > 0 ? '+' : ''}{n.score}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500">{n.reason}</p>
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <p className="text-sm text-gray-400">Aucun voisin avec association connue</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
