import { useState } from 'react';
import type { Vegetable } from '../../api/types';

interface Props {
  vegetables: Vegetable[];
  onSave: (data: {
    vegetable_id_main: number;
    vegetable_id_target: number;
    score: number;
    reason: string;
  }) => void;
  onCancel: () => void;
}

export default function AssociationForm({ vegetables, onSave, onCancel }: Props) {
  const [mainId, setMainId] = useState(vegetables[0]?.id ?? 0);
  const [targetId, setTargetId] = useState(vegetables[1]?.id ?? 0);
  const [score, setScore] = useState(0);
  const [reason, setReason] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (mainId === targetId) return;
    onSave({
      vegetable_id_main: mainId,
      vegetable_id_target: targetId,
      score,
      reason,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs text-gray-600 mb-1">Legume 1</label>
          <select
            value={mainId}
            onChange={(e) => setMainId(Number(e.target.value))}
            className="w-full border rounded px-2 py-1 text-sm"
          >
            {vegetables.map((v) => (
              <option key={v.id} value={v.id}>{v.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-xs text-gray-600 mb-1">Legume 2</label>
          <select
            value={targetId}
            onChange={(e) => setTargetId(Number(e.target.value))}
            className="w-full border rounded px-2 py-1 text-sm"
          >
            {vegetables.map((v) => (
              <option key={v.id} value={v.id}>{v.name}</option>
            ))}
          </select>
        </div>
      </div>
      <div>
        <label className="block text-xs text-gray-600 mb-1">
          Score : {score}
        </label>
        <input
          type="range"
          min={-50}
          max={50}
          value={score}
          onChange={(e) => setScore(Number(e.target.value))}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-400">
          <span>-50 (nefaste)</span>
          <span>0</span>
          <span>+50 (benefique)</span>
        </div>
      </div>
      <div>
        <label className="block text-xs text-gray-600 mb-1">Raison</label>
        <input
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          className="w-full border rounded px-2 py-1 text-sm"
        />
      </div>
      <div className="flex gap-2">
        <button type="submit" className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
          Creer
        </button>
        <button type="button" onClick={onCancel} className="text-gray-500 text-sm hover:text-gray-700">
          Annuler
        </button>
      </div>
    </form>
  );
}
