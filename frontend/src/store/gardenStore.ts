import { create } from 'zustand';
import type { GenerateResponse, Vegetable } from '../api/types';

interface GardenState {
  width: number;
  height: number;
  setDimensions: (w: number, h: number) => void;

  selectedItems: Map<number, number>; // vegetable_id -> quantity
  setQuantity: (vegId: number, qty: number) => void;
  fullRowItems: Set<number>; // vegetable_ids using "full row" mode
  setFullRow: (vegId: number, enabled: boolean) => void;
  clearSelection: () => void;

  vegetables: Vegetable[];
  setVegetables: (v: Vegetable[]) => void;

  result: GenerateResponse | null;
  setResult: (r: GenerateResponse | null) => void;

  loading: boolean;
  setLoading: (l: boolean) => void;

  error: string | null;
  setError: (e: string | null) => void;
}

export const useGardenStore = create<GardenState>((set) => ({
  width: 200,
  height: 200,
  setDimensions: (width, height) => set({ width, height }),

  selectedItems: new Map(),
  setQuantity: (vegId, qty) =>
    set((state) => {
      const next = new Map(state.selectedItems);
      if (qty <= 0) {
        next.delete(vegId);
        const nextFullRow = new Set(state.fullRowItems);
        nextFullRow.delete(vegId);
        return { selectedItems: next, fullRowItems: nextFullRow };
      }
      else next.set(vegId, qty);
      return { selectedItems: next };
    }),
  fullRowItems: new Set(),
  setFullRow: (vegId, enabled) =>
    set((state) => {
      const next = new Set(state.fullRowItems);
      if (enabled) next.add(vegId);
      else next.delete(vegId);
      return { fullRowItems: next };
    }),
  clearSelection: () => set({ selectedItems: new Map(), fullRowItems: new Set() }),

  vegetables: [],
  setVegetables: (vegetables) => set({ vegetables }),

  result: null,
  setResult: (result) => set({ result }),

  loading: false,
  setLoading: (loading) => set({ loading }),

  error: null,
  setError: (error) => set({ error }),
}));
