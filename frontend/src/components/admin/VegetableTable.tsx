import { useState } from 'react';
import type { Vegetable } from '../../api/types';
import { api } from '../../api/client';
import VegetableForm from './VegetableForm';

interface Props {
  vegetables: Vegetable[];
  onRefresh: () => void;
}

export default function VegetableTable({ vegetables, onRefresh }: Props) {
  const [editing, setEditing] = useState<Vegetable | null>(null);
  const [creating, setCreating] = useState(false);

  const handleDelete = async (id: number) => {
    if (!confirm('Supprimer ce legume ?')) return;
    await api.deleteVegetable(id);
    onRefresh();
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Legumes ({vegetables.length})</h2>
        <button
          onClick={() => { setCreating(true); setEditing(null); }}
          className="bg-green-600 text-white px-3 py-1.5 rounded text-sm hover:bg-green-700"
        >
          Ajouter
        </button>
      </div>

      {(creating || editing) && (
        <div className="mb-4 p-4 bg-gray-50 border rounded-lg">
          <VegetableForm
            initial={editing ?? undefined}
            onSave={async (data) => {
              if (editing) {
                await api.updateVegetable(editing.id, data);
              } else {
                await api.createVegetable(data as any);
              }
              setEditing(null);
              setCreating(false);
              onRefresh();
            }}
            onCancel={() => { setEditing(null); setCreating(false); }}
          />
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="py-2 pr-2">Couleur</th>
              <th className="py-2 pr-2">Nom</th>
              <th className="py-2 pr-2">Slug</th>
              <th className="py-2 pr-2">Taille (cm)</th>
              <th className="py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {vegetables.map((v) => (
              <tr key={v.id} className="border-b hover:bg-gray-50">
                <td className="py-2 pr-2">
                  <div className="w-6 h-6 rounded" style={{ backgroundColor: v.color }} />
                </td>
                <td className="py-2 pr-2">{v.name}</td>
                <td className="py-2 pr-2 text-gray-500">{v.slug}</td>
                <td className="py-2 pr-2">{v.grid_width * 5}x{v.grid_height * 5}</td>
                <td className="py-2 space-x-2">
                  <button
                    onClick={() => { setEditing(v); setCreating(false); }}
                    className="text-blue-600 hover:underline"
                  >
                    Modifier
                  </button>
                  <button
                    onClick={() => handleDelete(v.id)}
                    className="text-red-600 hover:underline"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
