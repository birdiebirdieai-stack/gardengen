import type {
  Vegetable, VegetableCreate,
  Association, AssociationCreate,
  GenerateRequest, GenerateResponse,
} from './types';

const BASE = '/api';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // Vegetables
  getVegetables: (q = '') =>
    request<Vegetable[]>(`/vegetables${q ? `?q=${encodeURIComponent(q)}` : ''}`),

  getVegetable: (slug: string) =>
    request<Vegetable>(`/vegetables/${slug}`),

  createVegetable: (data: VegetableCreate) =>
    request<Vegetable>('/vegetables', { method: 'POST', body: JSON.stringify(data) }),

  updateVegetable: (id: number, data: Partial<VegetableCreate>) =>
    request<Vegetable>(`/vegetables/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  deleteVegetable: (id: number) =>
    request<void>(`/vegetables/${id}`, { method: 'DELETE' }),

  // Associations
  getAssociations: () =>
    request<Association[]>('/associations'),

  getAssociationsFor: (vegId: number) =>
    request<Association[]>(`/associations/${vegId}`),

  upsertAssociation: (data: AssociationCreate) =>
    request<Association>('/associations', { method: 'POST', body: JSON.stringify(data) }),

  deleteAssociation: (mainId: number, targetId: number) =>
    request<void>(`/associations/${mainId}/${targetId}`, { method: 'DELETE' }),

  // Generate
  generate: (data: GenerateRequest) =>
    request<GenerateResponse>('/generate', { method: 'POST', body: JSON.stringify(data) }),
};
