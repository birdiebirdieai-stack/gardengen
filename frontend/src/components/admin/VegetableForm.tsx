import { useState } from 'react';
import type { Vegetable } from '../../api/types';

interface Props {
  initial?: Vegetable;
  onSave: (data: {
    name: string;
    slug: string;
    grid_width: number;
    grid_height: number;
    color: string;
  }) => void;
  onCancel: () => void;
}

export default function VegetableForm({ initial, onSave, onCancel }: Props) {
  const [name, setName] = useState(initial?.name ?? '');
  const [slug, setSlug] = useState(initial?.slug ?? '');
  const [gw, setGw] = useState(initial?.grid_width ?? 4);
  const [gh, setGh] = useState(initial?.grid_height ?? 4);
  const [color, setColor] = useState(initial?.color ?? '#22c55e');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({ name, slug, grid_width: gw, grid_height: gh, color });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs text-gray-600 mb-1">Nom</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border rounded px-2 py-1 text-sm"
            required
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Slug</label>
          <input
            value={slug}
            onChange={(e) => setSlug(e.target.value)}
            className="w-full border rounded px-2 py-1 text-sm"
            required
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Largeur (cellules 5cm)</label>
          <input
            type="number"
            min={1}
            value={gw}
            onChange={(e) => setGw(Number(e.target.value))}
            className="w-full border rounded px-2 py-1 text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Hauteur (cellules 5cm)</label>
          <input
            type="number"
            min={1}
            value={gh}
            onChange={(e) => setGh(Number(e.target.value))}
            className="w-full border rounded px-2 py-1 text-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Couleur</label>
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="w-full h-8 border rounded cursor-pointer"
          />
        </div>
      </div>
      <div className="flex gap-2">
        <button type="submit" className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
          {initial ? 'Sauvegarder' : 'Creer'}
        </button>
        <button type="button" onClick={onCancel} className="text-gray-500 text-sm hover:text-gray-700">
          Annuler
        </button>
      </div>
    </form>
  );
}
