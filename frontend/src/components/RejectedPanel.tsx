import type { Vegetable } from '../api/types';

interface Props {
  rejectedIds: number[];
  vegetables: Vegetable[];
}

export default function RejectedPanel({ rejectedIds, vegetables }: Props) {
  if (rejectedIds.length === 0) return null;

  // Count occurrences
  const counts = new Map<number, number>();
  rejectedIds.forEach((id) => counts.set(id, (counts.get(id) ?? 0) + 1));

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <h3 className="font-medium text-red-800 mb-2">
        Legumes non places ({rejectedIds.length})
      </h3>
      <ul className="space-y-1">
        {Array.from(counts.entries()).map(([vegId, count]) => {
          const v = vegetables.find((v) => v.id === vegId);
          return (
            <li key={vegId} className="text-sm text-red-700">
              {v?.name ?? `ID ${vegId}`} x{count}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
