import { useState } from 'react';
import type { Association, Vegetable } from '../../api/types';
import { api } from '../../api/client';
import AssociationForm from './AssociationForm';

interface Props {
  associations: Association[];
  vegetables: Vegetable[];
  onRefresh: () => void;
}

export default function AssociationTable({ associations, vegetables, onRefresh }: Props) {
  const [creating, setCreating] = useState(false);

  // Deduplicate: only show where main < target
  const unique = associations.filter(
    (a) => a.vegetable_id_main < a.vegetable_id_target
  );

  const handleDelete = async (mainId: number, targetId: number) => {
    if (!confirm('Supprimer cette association ?')) return;
    await api.deleteAssociation(mainId, targetId);
    onRefresh();
  };

  const vegName = (id: number) => vegetables.find((v) => v.id === id)?.name ?? `ID ${id}`;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Associations ({unique.length})</h2>
        <button
          onClick={() => setCreating(true)}
          className="bg-green-600 text-white px-3 py-1.5 rounded text-sm hover:bg-green-700"
        >
          Ajouter
        </button>
      </div>

      {creating && (
        <div className="mb-4 p-4 bg-gray-50 border rounded-lg">
          <AssociationForm
            vegetables={vegetables}
            onSave={async (data) => {
              await api.upsertAssociation(data);
              setCreating(false);
              onRefresh();
            }}
            onCancel={() => setCreating(false)}
          />
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="py-2 pr-2">Legume 1</th>
              <th className="py-2 pr-2">Legume 2</th>
              <th className="py-2 pr-2">Score</th>
              <th className="py-2 pr-2">Raison</th>
              <th className="py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {unique.map((a) => (
              <tr key={`${a.vegetable_id_main}-${a.vegetable_id_target}`} className="border-b hover:bg-gray-50">
                <td className="py-2 pr-2">{vegName(a.vegetable_id_main)}</td>
                <td className="py-2 pr-2">{vegName(a.vegetable_id_target)}</td>
                <td className="py-2 pr-2">
                  <span
                    className={`font-bold ${
                      a.score > 0 ? 'text-green-600' : a.score < 0 ? 'text-red-600' : 'text-gray-400'
                    }`}
                  >
                    {a.score > 0 ? '+' : ''}{a.score}
                  </span>
                </td>
                <td className="py-2 pr-2 text-gray-600 max-w-xs truncate">{a.reason}</td>
                <td className="py-2">
                  <button
                    onClick={() => handleDelete(a.vegetable_id_main, a.vegetable_id_target)}
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
