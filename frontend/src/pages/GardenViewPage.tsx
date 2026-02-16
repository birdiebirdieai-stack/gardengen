import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGardenStore } from '../store/gardenStore';
import { api } from '../api/client';
import type { Association } from '../api/types';
import GardenGrid from '../components/GardenGrid';
import RejectedPanel from '../components/RejectedPanel';

export default function GardenViewPage() {
  const navigate = useNavigate();
  const width = useGardenStore((state) => state.width);
  const height = useGardenStore((state) => state.height);
  const result = useGardenStore((state) => state.result);
  const vegetables = useGardenStore((state) => state.vegetables);
  const [associations, setAssociations] = useState<Association[]>([]);

  useEffect(() => {
    api.getAssociations().then(setAssociations);
  }, []);

  if (!result) {
    return (
      <div className="max-w-lg mx-auto py-12 px-4 text-center">
        <p className="text-gray-500 mb-4">Aucun plan genere.</p>
        <button
          onClick={() => navigate('/selection')}
          className="text-green-600 hover:underline"
        >
          Retour a la selection
        </button>
      </div>
    );
  }

  const gridW = Math.floor(width / 5);
  const gridH = Math.floor(height / 5);

  return (
    <div className="max-w-5xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-green-800">Votre potager</h1>
          <p className="text-gray-500 text-sm">
            {width} x {height} cm — Score global :{' '}
            <span
              className={`font-bold ${
                result.global_score > 0
                  ? 'text-green-600'
                  : result.global_score < 0
                    ? 'text-red-600'
                    : 'text-gray-500'
              }`}
            >
              {result.global_score > 0 ? '+' : ''}{result.global_score}
            </span>
          </p>
        </div>
        <button
          onClick={() => navigate('/selection')}
          className="text-sm text-green-600 hover:underline"
        >
          Modifier la selection
        </button>
      </div>

      <GardenGrid
        result={result}
        vegetables={vegetables}
        associations={associations}
        gridW={gridW}
        gridH={gridH}
      />

      <div className="mt-6">
        <RejectedPanel rejectedIds={result.rejected} vegetables={vegetables} />
      </div>
    </div>
  );
}
