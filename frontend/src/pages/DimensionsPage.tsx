import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGardenStore } from '../store/gardenStore';

export default function DimensionsPage() {
  const width = useGardenStore((state) => state.width);
  const height = useGardenStore((state) => state.height);
  const setDimensions = useGardenStore((state) => state.setDimensions);
  const [w, setW] = useState(width);
  const [h, setH] = useState(height);
  const navigate = useNavigate();

  const valid = w >= 100 && w <= 1000 && h >= 100 && h <= 1000;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!valid) return;
    setDimensions(w, h);
    navigate('/selection');
  };

  const maxDim = Math.max(w, h, 1);
  const previewW = (w / maxDim) * 200;
  const previewH = (h / maxDim) * 200;

  return (
    <div className="max-w-lg mx-auto py-12 px-4">
      <h1 className="text-3xl font-bold text-green-800 mb-2">GardenGen</h1>
      <p className="text-gray-600 mb-8">
        Entrez les dimensions de votre potager pour commencer.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Largeur (cm)
            </label>
            <input
              type="number"
              min={100}
              max={1000}
              value={w}
              onChange={(e) => setW(Number(e.target.value))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Longueur (cm)
            </label>
            <input
              type="number"
              min={100}
              max={1000}
              value={h}
              onChange={(e) => setH(Number(e.target.value))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />
          </div>
        </div>

        <div className="flex justify-center py-4">
          <div
            className="border-2 border-dashed border-green-400 bg-green-50 rounded"
            style={{ width: previewW, height: previewH }}
          >
            <div className="flex items-center justify-center h-full text-sm text-green-700">
              {w} x {h} cm
            </div>
          </div>
        </div>

        {!valid && (
          <p className="text-red-500 text-sm">
            Les dimensions doivent etre entre 100 et 1000 cm.
          </p>
        )}

        <button
          type="submit"
          disabled={!valid}
          className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Suivant
        </button>
      </form>
    </div>
  );
}
