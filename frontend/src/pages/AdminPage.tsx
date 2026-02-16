import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Vegetable, Association } from '../api/types';
import VegetableTable from '../components/admin/VegetableTable';
import AssociationTable from '../components/admin/AssociationTable';

type Tab = 'vegetables' | 'associations';

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>('vegetables');
  const [vegetables, setVegetables] = useState<Vegetable[]>([]);
  const [associations, setAssociations] = useState<Association[]>([]);

  const loadVegetables = () => api.getVegetables().then(setVegetables);
  const loadAssociations = () => api.getAssociations().then(setAssociations);

  useEffect(() => {
    loadVegetables();
    loadAssociations();
  }, []);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold text-green-800 mb-6">Administration</h1>

      <div className="flex gap-1 mb-6 border-b">
        <button
          onClick={() => setTab('vegetables')}
          className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
            tab === 'vegetables'
              ? 'border-green-600 text-green-700'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Legumes
        </button>
        <button
          onClick={() => setTab('associations')}
          className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
            tab === 'associations'
              ? 'border-green-600 text-green-700'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Associations
        </button>
      </div>

      {tab === 'vegetables' && (
        <VegetableTable vegetables={vegetables} onRefresh={loadVegetables} />
      )}
      {tab === 'associations' && (
        <AssociationTable
          associations={associations}
          vegetables={vegetables}
          onRefresh={loadAssociations}
        />
      )}
    </div>
  );
}
