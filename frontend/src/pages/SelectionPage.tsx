import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGardenStore } from '../store/gardenStore';
import { api } from '../api/client';
import VegetableCard from '../components/VegetableCard';
import SurfaceGauge from '../components/SurfaceGauge';

export default function SelectionPage() {
  const navigate = useNavigate();
  const {
    width, height, vegetables, setVegetables,
    selectedItems, setQuantity,
    setResult, setLoading, setError, loading,
  } = useGardenStore();

  useEffect(() => {
    api.getVegetables().then(setVegetables);
  }, [setVegetables]);

  const totalCells = (width / 5) * (height / 5);
  let usedCells = 0;
  selectedItems.forEach((qty, vegId) => {
    const v = vegetables.find((v) => v.id === vegId);
    if (v) usedCells += v.grid_width * v.grid_height * qty;
  });

  const hasSelection = selectedItems.size > 0;

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const items = Array.from(selectedItems.entries()).map(([vegetable_id, quantity]) => ({
        vegetable_id,
        quantity,
      }));
      const result = await api.generate({ width_cm: width, height_cm: height, items });
      setResult(result);
      navigate('/garden');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-green-800">Choisir vos legumes</h1>
          <p className="text-gray-500 text-sm">Potager : {width} x {height} cm</p>
        </div>
        <button
          onClick={() => navigate('/')}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          Modifier dimensions
        </button>
      </div>

      <div className="mb-6">
        <SurfaceGauge usedCells={usedCells} totalCells={totalCells} />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8">
        {vegetables.map((v) => (
          <VegetableCard
            key={v.id}
            vegetable={v}
            quantity={selectedItems.get(v.id) ?? 0}
            onQuantityChange={(qty) => setQuantity(v.id, qty)}
          />
        ))}
      </div>

      <button
        onClick={handleGenerate}
        disabled={!hasSelection || loading}
        className="w-full bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Generation en cours...' : 'Generer le plan'}
      </button>
    </div>
  );
}
