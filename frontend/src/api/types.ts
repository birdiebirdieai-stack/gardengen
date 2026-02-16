export interface Vegetable {
  id: number;
  name: string;
  variety: string;
  slug: string;
  grid_width: number;
  grid_height: number;
  color: string;
}

export interface VegetableCreate {
  name: string;
  variety?: string;
  slug: string;
  grid_width: number;
  grid_height: number;
  color?: string;
}

export interface Association {
  vegetable_id_main: number;
  vegetable_id_target: number;
  score: number;
  reason: string;
  main_name?: string;
  target_name?: string;
}

export interface AssociationCreate {
  vegetable_id_main: number;
  vegetable_id_target: number;
  score: number;
  reason: string;
}

export interface GenerateItem {
  vegetable_id: number;
  quantity: number;
}

export interface GenerateRequest {
  width_cm: number;
  height_cm: number;
  items: GenerateItem[];
}

export interface PlacedVegetable {
  vegetable_id: number;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface GenerateResponse {
  placed: PlacedVegetable[];
  rejected: number[];
  global_score: number;
}
